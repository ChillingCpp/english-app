# -*- coding: utf-8 -*-
"""
test_dictionary_query.py — Test case cho dictionary_query.py + verify_batch.py
Chạy:  python -m unittest test_dictionary_query -v
"""
import json
import os
import unittest

from dictionary_query import (
    connect, normalize_vi, pos_to_name, get_word_id, lookup_en, lookup_vi,
    format_result, DB_PATH,
)
from verify_batch import verify_batch, verify_word

BATCH_001 = os.path.join("batches", "batch_001.json")


class TestNormalizeVi(unittest.TestCase):
    def test_keeps_normal_text(self):
        self.assertEqual(normalize_vi("duy trì"), "duy trì")

    def test_y_to_i_after_hklmst(self):
        self.assertEqual(normalize_vi("ký"), "kí")
        self.assertEqual(normalize_vi("kỳ"), "kì")
        self.assertEqual(normalize_vi("sy"), "si")

    def test_does_not_touch_uy(self):
        # 'uy' sau nguyên âm không đổi (quy tắc (?<!u))
        self.assertEqual(normalize_vi("tuy"), "tuy")

    def test_qui_to_quy(self):
        self.assertEqual(normalize_vi("qui định"), "quy định")
        # theo sql_query_example.ts: chỉ thay biến quí/quý... khi chuỗi chứa "qui"
        self.assertEqual(normalize_vi("quí"), "quí")  # không chứa 'qui' -> giữ nguyên
        self.assertEqual(normalize_vi("qui quí"), "quy quý")  # chứa 'qui' -> quí cũng được thay

    def test_oa_to_oa_grave(self):
        self.assertEqual(normalize_vi("hòa"), "hoà")

    def test_empty(self):
        self.assertEqual(normalize_vi(""), "")


class TestDb(unittest.TestCase):
    def test_db_exists(self):
        self.assertTrue(os.path.exists(DB_PATH), f"thiếu DB: {DB_PATH}")

    def test_connect_readonly(self):
        con = connect()
        try:
            # readonly: ghi phải thất bại
            with self.assertRaises(Exception):
                con.execute("CREATE TABLE _t(x)")
        finally:
            con.close()

    def test_get_word_id(self):
        con = connect()
        try:
            wid, word = get_word_id(con, "iron", "en")
            self.assertIsNotNone(wid)
            self.assertEqual(word, "iron")
            wid2, _ = get_word_id(con, "duy trì", "vi")
            self.assertIsNotNone(wid2)
            self.assertIsNone(get_word_id(con, "zzznotexistzzz", "en")[0])
        finally:
            con.close()

class TestLookupEn(unittest.TestCase):
    def test_iron_found(self):
        res = lookup_en("iron")
        self.assertTrue(res["exists"])
        self.assertEqual(res["word"], "iron")
        self.assertGreater(len(res["meanings"]), 0)
        defs = " ".join(m["definition"] for m in res["meanings"])
        self.assertIn("Sắt", defs)
        poss = {m["pos"] for m in res["meanings"]}
        self.assertIn("noun", poss)
        self.assertIn("verb", poss)

    def test_pronunciation(self):
        res = lookup_en("maintain")
        self.assertTrue(res["exists"])
        self.assertTrue(any("meɪn" in ipa for ipa, _ in res["pronunciations"]))

    def test_maintain_duy_tri(self):
        res = lookup_en("maintain")
        defs = " ".join(m["definition"] for m in res["meanings"]).lower()
        self.assertIn("duy trì", defs)

    def test_example_field(self):
        res = lookup_en("maintain")
        examples = [m["example"] for m in res["meanings"] if m["example"]]
        self.assertTrue(any("maintain" in e for e in examples))

    def test_relations(self):
        res = lookup_en("iron")
        self.assertTrue(res["exists"])
        self.assertGreater(len(res["relations"]), 0)
        labels = {r["relation_label"] for r in res["relations"]}
        self.assertTrue(labels & {"đồng nghĩa", "liên quan", "phái sinh", "trái nghĩa"})

    def test_not_found(self):
        res = lookup_en("zzznotexistzzz")
        self.assertFalse(res["exists"])
        self.assertEqual(res["meanings"], [])

    def test_pos_mapping(self):
        res = lookup_en("bank")
        self.assertTrue(res["exists"])
        poss = {m["pos"] for m in res["meanings"]}
        self.assertIn("noun", poss)
        self.assertEqual(pos_to_name("N"), "noun")
        self.assertEqual(pos_to_name("V"), "verb")
        self.assertIsNone(pos_to_name(None))

    def test_homograph_data(self):
        # 'mall' có cả nghĩa "Búa nặng" (homograph maul) -> dữ liệu kiểm thử cờ review
        res = lookup_en("mall")
        self.assertTrue(res["exists"])
        defs = [m["definition"] for m in res["meanings"]]
        self.assertTrue(any("Búa" in d for d in defs))
        self.assertTrue(any("buôn bán" in d for d in defs))


class TestLookupVi(unittest.TestCase):
    def test_duy_tri(self):
        res = lookup_vi("duy trì")
        self.assertTrue(res["exists"])
        self.assertGreater(len(res["meanings"]), 0)
        joined = " ".join(m["definition"] for m in res["meanings"])
        self.assertIn("maintain", joined)

    def test_not_found(self):
        self.assertFalse(lookup_vi("zzznotexistzzz")["exists"])


class TestFormat(unittest.TestCase):
    def test_format_found(self):
        txt = format_result(lookup_en("iron"))
        self.assertIn("== iron ==", txt)
        self.assertIn("Sắt", txt)

    def test_format_not_found(self):
        txt = format_result({"exists": False, "word": "abc", "meanings": [],
                             "pronunciations": [], "relations": []})
        self.assertIn("KHÔNG TÌM THẤY", txt)


class TestVerifyBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(BATCH_001):
            raise unittest.SkipTest(f"thiếu {BATCH_001}")
        cls.summary, cls.results = verify_batch(BATCH_001)

    def test_total_words(self):
        self.assertEqual(self.summary["total_words"], 50)

    def test_most_words_found_in_db(self):
        self.assertGreaterEqual(self.summary["found_in_db"], 45,
                                f"not_found={self.summary['not_found']}")

    def test_result_structure(self):
        r = self.results[0]
        for key in ("word", "found", "n_senses_batch", "n_defs_db",
                    "senses", "suggested_relations", "flags"):
            self.assertIn(key, r)

    def test_verify_word_senses(self):
        out = verify_word("maintain", {"senses": [
            {"id": "maintain-keep", "meaning_vi": "Giữ, duy trì, bảo vệ, bảo quản.",
             "pos": ["verb"]}]})
        self.assertTrue(out["found"])
        self.assertEqual(len(out["senses"]), 1)
        s = out["senses"][0]
        self.assertGreater(s["similarity"], 0.8)
        self.assertNotIn("no_db_def_for_pos", s.get("flag", ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
