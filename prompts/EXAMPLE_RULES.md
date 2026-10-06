# Quy tắc sinh Examples/Senses (trích từ Content Generation Task Specification.md)

Bạn nhận batch ~75 từ, mỗi từ có sẵn các sense (meaning_vi), pos, context_labels.
Nhiệm vụ: sinh example sentences cho MỖI sense, xuất JSON đúng schema.

## 5. Sense

- Sense đã cho = một nghĩa riêng biệt. GIỮ nguyên meaning_vi (không diễn dịch lại).
- Chỉ được gộp hai sense khi chúng là **cùng một khái niệm học tập** (cùng nghĩa,
  chỉ khác cách diễn đạt). Khi gộp: giữ meaning_vi đầy đủ hơn, gộp lại
  context_labels của hai sense (bỏ trùng).
- Không tạo sense mới.

## 6. Ý nghĩa tiếng Việt

- meaning_vi đã có: không sửa, không rút gọn.

## 8. Example sentence requirements (mỗi câu phải)

1. thể hiện rõ sense intended
2. dùng đúng từ loại (pos)
3. tự nhiên (natural English)
4. đúng ngữ pháp
5. dễ hiểu cho người học
6. đủ ngữ cảnh để suy ra intended meaning
7. không phức tạp thừa
8. tránh diễn giải mơ hồ

Cấm câu kiểu "The iron was iron because iron is iron." Ưu tiên ngôn ngữ thực tế.

## 9. Số lượng example / sense

- sense phổ biến/simple: 2–3 example
- sense có nhiều context quan trọng: 3–5 example
- KHÔNG sinh 5 biến thể hời hợt của cùng một câu.
- Với sense hiếm/technical (word hiếm, nghĩa hẹp): 1–2 câu cũng được, nhưng phải đúng.
- Example phải phân bố theo các context_labels khác nhau của sense (ví dụ sense
  `maintain`: 1 câu health, 1 câu relationships, 1 câu quality).

## 10. Fill-in-the-blank

Mỗi example sinh thêm blank_sentence: thay đúng target word bằng ____ (4 dấu gạch).

```
Regular exercise helps maintain good health.
→ Regular exercise helps ____ good health.
```

- Blank không được loại bỏ quá nhiều thông tin đến mức mơ hồ.
- blank_sentence KHÔNG được chứa nguyên từ target (không leak đáp án).
- Target word là answer (đúng dạng: nếu câu ở thì quá khứ mà target là động từ
  bất quy tắc thì answer vẫn là từ gốc theo dạng đã blank — nếu không thể blank
    tự nhiên thì viết câu khác để dạng từ phẳng xuất hiện).

## 11–12. Accepted answers

- Mỗi exercise: 1 answer (primary) + 0 hoặc nhiều accepted_answers.
- Chỉ thêm accepted answer nếu thay thế đúng câu đó, đúng sense, KHÔNG làm đổi
  nghĩa — phải là synonym dùng được trong câu cụ thể này.
- Nếu không chắc: KHÔNG thêm (false positive tệ hơn missing).
- answer = target word đúng như trong sentence.
- accepted_answers không được trùng answer.

## 16. Difficulty

- Câu dễ (A1/A2): ngữ pháp đơn giản, tình huống quen thuộc, từ vựng quanh target.
- Câu B1/B2+: ngữ cảnh thực tế kiểu IELTS/general English, cấu trúc tự nhiên.
- KHÔNG làm câu khó giả tạo.

## 18. Ưu tiên khi chọn example

naturalness > đúng sense > ngữ cảnh rõ > hữu ích thực tế > tần suất dùng >
phù hợp người học > đa dạng chủ đề. Chất lượng hơn số lượng.

## 21. Không bịa

- Không bịa CEFR, không bịa nguồn, không bịa synonym.
- Nếu nghĩa quá hiếm khiến không nghĩ ra câu tự nhiên: sinh 1 câu đơn giản trung
  thực vẫn tốt hơn bịa câu hay nhưng sai.

## Output JSON (đúng schema này, không prose)

```json
{
  "batch": 1,
  "words": [
    {
      "word": "maintain",
      "pronunciation": "/meɪnˈteɪn/",
      "part_of_speech": ["V"],
      "senses": [
        {
          "meaning_vi": "duy trì, giữ nguyên",
          "pos": "V",
          "source": "dictionary.db",
          "context_labels": ["health", "relationships", "work"],
          "examples": [
            {
              "sentence": "Regular exercise helps maintain good health.",
              "blank_sentence": "Regular exercise helps ____ good health.",
              "answer": "maintain",
              "accepted_answers": []
            }
          ]
        }
      ]
    }
  ]
}
```

- `word`, `pronunciation`, `part_of_speech`, sense `meaning_vi`/`pos`/`source`/
  `context_labels`: copy nguyên văn từ input (sense chỉ đổi khi gộp theo mục 5).
- Mỗi sense ít nhất 1 example (mục tiêu 2–3).
- Tự validate trước khi ghi file: câu đúng ngữ pháp, answer có trong sentence,
  blank không leak answer, blank có ____ , không có accepted_answer trùng answer.
