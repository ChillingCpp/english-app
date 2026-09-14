/**
 * SQLite dictionary helper module
 * Optimized for Vercel serverless (read-only filesystem)
 * Supports multi-language dictionary lookups
 */

import Database from 'better-sqlite3';
import path from 'path';

// POS labels
const POS_LABELS: Record<string, string> = {
    A: 'Tính từ',
    C: 'Liên từ',
    D: 'Phó từ',
    E: 'Giới từ',
    I: 'Tình thái từ',
    M: 'Lượng từ',
    N: 'Danh từ',
    O: 'Thán từ',
    P: 'Đại từ',
    R: 'Trạng từ',
    S: 'Từ đặc biệt',
    V: 'Động từ',
    X: 'Từ phụ trợ / khác',
    Z: 'Hậu tố'
};

// Sub POS labels
const SUB_POS_LABELS: Record<string, string> = {
    A: 'Tính từ nói chung',
    A0: 'Tính từ chỉ số lượng, trạng thái tổng quát',
    Ai: 'Tính từ chỉ khả năng, thuộc tính nội tại',
    Ao: 'Tính từ chỉ âm thanh, cảm giác',
    Ap: 'Tính từ phổ biến',
    Ar: 'Tính từ chỉ mức độ, cường độ',
    Ax: 'Tính từ đặc biệt',
    Vi: 'Động từ nội',
    Vm: 'Động từ phương pháp',
    Vs: 'Động từ không chuyển',
    Vt: 'Động từ chuyển',
    Vu: 'Động từ đặc biệt/thành ngữ',
    N: 'Danh từ nói chung',
    Na: 'Danh từ trừu tượng',
    Nc: 'Danh từ chỉ loại',
    Ng: 'Danh từ giống loài',
    Nl: 'Danh từ chỉ vị trí',
    Np: 'Danh từ riêng',
    Nt: 'Danh từ chỉ vật, hiện tượng',
    Nu: 'Danh từ đơn vị',
    Nx: 'Danh từ chuyên biệt',
    Pd: 'Đại từ chỉ định',
    Pi: 'Đại từ nhân xưng',
    Pp: 'Đại từ sở hữu',
    Pq: 'Đại từ nghi vấn',
    C: 'Liên từ',
    D: 'Phó từ',
    E: 'Giới từ',
    I: 'Thán từ',
    Mc: 'Lượng từ đơn vị',
    Mo: 'Lượng từ số lượng',
    O: 'Từ tình thái',
    R: 'Trạng từ',
    S: 'Từ đặc biệt',
    X: 'Tổ hợp từ đặc biệt',
    XX: 'Từ lỗi/dữ liệu không xác định',
    Z: 'Hậu tố'
};

// Relation labels
const RELATION_LABELS: Record<string, string> = {
    s: 'Đồng nghĩa',
    a: 'Trái nghĩa',
    d: 'Từ phái sinh',
    r: 'Liên quan'
};

// Language labels - auto-generated from kaikki.org-dictionary-all.jsonl
import { LANG_LABELS } from './lang_labels';




export interface DictionaryMeaning {
    definition: string;
    definition_lang: string;
    example: string | null;
    pos: string;
    sub_pos: string | null;
    source: string | null;
    links: string[];
}

export interface DictionaryPronunciation {
    ipa: string;
    region: string | null;
}

export interface DictionaryTranslation {
    lang_code: string;
    lang_name: string | null;
    translation: string;
}

export interface DictionaryRelation {
    related_word: string;
    relation_type: string;
}

// Single language result
export interface LanguageResult {
    lang_code: string;
    lang_name: string;
    audio: string;
    meanings: DictionaryMeaning[];
    pronunciations: DictionaryPronunciation[];
    translations: DictionaryTranslation[];
    relations: DictionaryRelation[];
}

// Multi-language lookup result
export interface MultiLookupResult {
    exists: boolean;
    word: string;
    results: LanguageResult[];
}

// Legacy single result (for backward compatibility)
export interface LookupResult {
    exists: boolean;
    word?: string;
    lang_code?: string;
    lang_name?: string;
    audio?: string;
    meanings?: DictionaryMeaning[];
    pronunciations?: DictionaryPronunciation[];
    translations?: DictionaryTranslation[];
    relations?: DictionaryRelation[];
}

// Singleton database instance (lazy loaded)
let db: Database.Database | null = null;

function getDb(): Database.Database {
    if (!db) {
        const dbPath = path.join(process.cwd(), 'lib', 'dictionary.db');
        db = new Database(dbPath, {
            readonly: true,
            fileMustExist: true
        });

        db.pragma('query_only = ON');
        db.pragma('journal_mode = OFF');
        db.pragma('synchronous = OFF');
        db.pragma('cache_size = -32000');
        db.pragma('mmap_size = 256000000');
        db.pragma('temp_store = MEMORY');
        db.pragma('threads = 4');
    }
    return db;
}

// Prepared statements (lazy loaded)
let lookupAllLangsStmt: Database.Statement | null = null;
let lookupByLangStmt: Database.Statement | null = null;
let getMeaningsStmt: Database.Statement | null = null;

let getPronunciationsStmt: Database.Statement | null = null;
let getTranslationsStmt: Database.Statement | null = null;
let getRelationsStmt: Database.Statement | null = null;

function getStatements() {
    const database = getDb();

    if (!lookupAllLangsStmt) {
        lookupAllLangsStmt = database.prepare(`
            SELECT id, word, lang_code FROM words WHERE word = ? ORDER BY 
            CASE lang_code 
                WHEN 'vi' THEN 1 
                WHEN 'en' THEN 2 
                ELSE 3 
            END, lang_code
        `);
    }

    if (!lookupByLangStmt) {
        lookupByLangStmt = database.prepare(`
            SELECT id, word, lang_code FROM words WHERE word = ? AND lang_code = ?
        `);
    }

    if (!getMeaningsStmt) {
        getMeaningsStmt = database.prepare(`
            SELECT d.id as definition_id, d.definition, COALESCE(d.definition_lang, 'vi') as definition_lang, wd.example, d.pos, d.sub_pos, d.links, s.name as source
            FROM word_definitions wd
            JOIN definitions d ON wd.definition_id = d.id
            LEFT JOIN sources s ON wd.source_id = s.id
            WHERE wd.word_id = ?
        `);
    }



    if (!getPronunciationsStmt) {
        getPronunciationsStmt = database.prepare(`
            SELECT ipa, region FROM pronunciations WHERE word_id = ?
        `);
    }

    if (!getTranslationsStmt) {
        getTranslationsStmt = database.prepare(`
            SELECT lang_code, translation FROM translations WHERE word_id = ?
        `);
    }

    if (!getRelationsStmt) {
        getRelationsStmt = database.prepare(`
            SELECT related_word, relation_type FROM word_relations WHERE word_id = ?
        `);
    }

    return {
        lookupAllLangsStmt,
        lookupByLangStmt,
        getMeaningsStmt,

        getPronunciationsStmt,
        getTranslationsStmt,
        getRelationsStmt
    };
}

function normalizeVietnamese(text: string): string {
    if (!text) return '';

    let result = text;

    result = result.replace(/(?<!u)([hklmst])y(?=\s|$|[.,!?])/g, '$1i')
        .replace(/(?<!u)([hklmst])ỳ(?=\s|$|[.,!?])/g, '$1ì')
        .replace(/(?<!u)([hklmst])ý(?=\s|$|[.,!?])/g, '$1í')
        .replace(/(?<!u)([hklmst])ỷ(?=\s|$|[.,!?])/g, '$1ỉ')
        .replace(/(?<!u)([hklmst])ỹ(?=\s|$|[.,!?])/g, '$1ĩ')
        .replace(/(?<!u)([hklmst])ỵ(?=\s|$|[.,!?])/g, '$1ị');

    if (result.includes('qui')) {
        result = result.replace(/qui/g, 'quy').replace(/quì/g, 'quỳ').replace(/quí/g, 'quý')
            .replace(/quỉ/g, 'quỷ').replace(/quĩ/g, 'quỹ').replace(/quị/g, 'quỵ');
    }

    if (/[ùúủũụòóỏõọ]/.test(result)) {
        result = result.replace(/ùy/g, 'uỳ').replace(/úy/g, 'uý').replace(/ủy/g, 'uỷ').replace(/ũy/g, 'uỹ').replace(/ụy/g, 'uỵ')
            .replace(/òa/g, 'oà').replace(/óa/g, 'oá').replace(/ỏa/g, 'oả').replace(/õa/g, 'oã').replace(/ọa/g, 'oạ')
            .replace(/òe/g, 'oè').replace(/óe/g, 'oé').replace(/ỏe/g, 'oẻ').replace(/õe/g, 'oẽ').replace(/ọe/g, 'oẹ');
    }

    return result;
}

function getWordData(wordId: number, wordText: string, langCode: string): LanguageResult {
    const { getMeaningsStmt, getPronunciationsStmt, getTranslationsStmt, getRelationsStmt } = getStatements();

    const meanings = getMeaningsStmt!.all(wordId) as {
        definition_id: number;
        definition: string;
        definition_lang: string;
        example: string | null;
        pos: string;
        sub_pos: string | null;
        links: string | null;
        source: string | null;
    }[];

    const updatedMeanings: DictionaryMeaning[] = meanings.map((meaning) => {
        let links: string[] = [];
        if (meaning.links) {
            try {
                links = JSON.parse(meaning.links);
            } catch (e) {
                console.error('Error parsing links JSON:', e);
            }
        }

        return {
            definition: meaning.definition,
            definition_lang: meaning.definition_lang,
            example: meaning.example,
            pos: POS_LABELS[meaning.pos] ?? meaning.pos,
            sub_pos: meaning.sub_pos ? (SUB_POS_LABELS[meaning.sub_pos] ?? meaning.sub_pos) : null,
            source: meaning.source,
            links
        };
    });

    const pronunciations = getPronunciationsStmt!.all(wordId) as DictionaryPronunciation[];
    const translations = getTranslationsStmt!.all(wordId) as DictionaryTranslation[];
    const relations = getRelationsStmt!.all(wordId) as DictionaryRelation[];

    const updatedTranslations = translations.map((t) => ({
        ...t,
        lang_name: LANG_LABELS[t.lang_code] ?? t.lang_code
    }));

    const updatedRelations = relations.map((rel) => ({
        ...rel,
        relation_type: RELATION_LABELS[rel.relation_type] ?? rel.relation_type
    }));

    return {
        lang_code: langCode,
        lang_name: LANG_LABELS[langCode] ?? langCode,
        audio: `/api/v1/tts?word=${encodeURIComponent(wordText)}&lang=${langCode}`,
        meanings: updatedMeanings,
        pronunciations,
        translations: updatedTranslations,
        relations: updatedRelations
    };
}

/**
 * Look up a word in the dictionary (multi-language)
 * @param word - The word to look up
 * @param lang - Optional language code to filter by
 * @returns MultiLookupResult with results grouped by language
 */
export function lookupWord(word: string, lang?: string): MultiLookupResult {
    const { lookupAllLangsStmt, lookupByLangStmt } = getStatements();

    const normalized = normalizeVietnamese(word.normalize('NFC').toLowerCase());

    let wordRows: { id: number; word: string; lang_code: string }[];

    if (lang) {
        // Lookup specific language
        const row = lookupByLangStmt!.get(normalized, lang) as { id: number; word: string; lang_code: string } | undefined;
        if (!row) {
            const fallback = lookupByLangStmt!.get(word, lang) as { id: number; word: string; lang_code: string } | undefined;
            wordRows = fallback ? [fallback] : [];
        } else {
            wordRows = [row];
        }
    } else {
        // Lookup all languages
        wordRows = lookupAllLangsStmt!.all(normalized) as { id: number; word: string; lang_code: string }[];
        if (wordRows.length === 0) {
            wordRows = lookupAllLangsStmt!.all(word) as { id: number; word: string; lang_code: string }[];
        }
    }

    if (wordRows.length === 0) {
        return { exists: false, word: normalized, results: [] };
    }

    const results: LanguageResult[] = wordRows.map(row =>
        getWordData(row.id, row.word, row.lang_code)
    );

    return {
        exists: true,
        word: wordRows[0].word,
        results
    };
}

// Prepared statement for suggestions (lazy loaded)
let suggestStmt: Database.Statement | null = null;

/**
 * Get word suggestions based on prefix
 * @param prefix - The prefix to search for
 * @param limit - Maximum number of suggestions to return
 * @param lang - Optional language code to filter by
 * @returns Array of suggested words
 */
export function getSuggestions(prefix: string, limit: number = 8, lang?: string): string[] {
    const database = getDb();

    const normalizedPrefix = normalizeVietnamese(prefix.normalize('NFC').toLowerCase());

    if (lang) {
        const stmt = database.prepare(`
            SELECT DISTINCT word FROM words 
            WHERE word LIKE ? || '%' AND lang_code = ?
            ORDER BY LENGTH(word), word
            LIMIT ?
        `);
        const rows = stmt.all(normalizedPrefix, lang, limit) as { word: string }[];
        return rows.map(r => r.word);
    } else {
        if (!suggestStmt) {
            suggestStmt = database.prepare(`
                SELECT DISTINCT word FROM words 
                WHERE word LIKE ? || '%' 
                ORDER BY 
                    CASE lang_code WHEN 'vi' THEN 0 ELSE 1 END,
                    LENGTH(word), word
                LIMIT ?
            `);
        }
        const rows = suggestStmt.all(normalizedPrefix, limit) as { word: string }[];
        return rows.map(r => r.word);
    }
}
