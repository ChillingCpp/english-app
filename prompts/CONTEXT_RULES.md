# Quy tắc sinh Context Labels (trích từ Content Generation Task Specification.md §7)

Mỗi sense (nghĩa) của từ cần 1–4 context label mô tả tình huống thường dùng nghĩa đó.

## Ví dụ từ guide

```
iron (resource)
contexts:
- mining
- industry
- steel production
- economy
- environment
```

## Quy tắc

1. Context label mô tả **tình huống sử dụng** của nghĩa đó, không mô tả từ.
2. KHÔNG tạo context giả tạo chỉ để tăng số tag.
3. Một từ có thể thuộc nhiều context; mỗi nghĩa thường có 1–3 label, tối đa 4.
4. Ưu tiên label phổ biến/tái sử dụng để các từ khác cùng dùng lại được.
5. Label viết thường, ngắn (1–3 từ), dạng danh từ chủ đề: `health`, `education`,
   `steel production`.
6. Chỉ thêm label mới khi thực sự cần và không có label nào phù hợp trong bộ phổ biến.

## Bộ label phổ biến (ưu tiên chọn từ đây)

general, daily life, social, time, feelings, emotions, personality, appearance,
clothing, body, health, medicine, exercise, sleep, education, work, career,
business, finance, economy, money, shopping, technology, programming, internet,
media, communication, travel, transportation, food, cooking, restaurant, family,
friendship, relationships, marriage, home, animals, plants, nature, environment,
weather, government, law, politics, crime, safety, military, science, industry,
mining, construction, engineering, farming, sports, entertainment, arts, music,
literature, photography, design, history, geography, culture, religion,
philosophy, psychology, success, management, teamwork, competition, holiday,
leisure, hobby, tourism, urban, rural, formal, informal

## Định dạng output (mỗi dòng TSV, không có prose, không markdown)

```
<word>\t<meaning_index>\t<label1>, <label2>
```

- `meaning_index` = vị trí (1-based) của nghĩa trong mảng `meanings` của từ đó
  trong file input — KHÔNG viết lại nghĩa, chỉ ghi số thứ tự.
- Tab thật phân cách 3 cột (không dùng khoảng trắng thay tab).
- Ví dụ input `{"word":"bank","meanings":["ngân hàng","bờ sông"]}` -> 2 dòng:
  `bank	1	business, finance`
  `bank	2	nature, transportation`
- Mỗi từ và mỗi nghĩa trong input phải xuất hiện **đúng một lần** trong output.
- Nếu không chắc nghĩa, vẫn phải gán label phổ quát nhất (`general` hoặc chủ đề
  tổng quát phù hợp), không được bỏ sót.
