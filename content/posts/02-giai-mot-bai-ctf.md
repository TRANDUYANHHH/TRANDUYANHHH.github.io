---
title: Một writeup nhỏ: nhận ra chuỗi Base64
description: Bài tập CTF giả lập để minh họa cách ghi lại quan sát, kiểm chứng và lời giải.
date: 2026-11-06
category: Writeup
tags: ["CTF", "Python", "Base64"]
featured: false
---

Đây là một bài tập giả lập, chạy hoàn toàn trên máy cá nhân. Mục tiêu là giải một thông điệp được cung cấp sẵn và trình bày cách suy luận sao cho người khác có thể làm lại.

## Đề bài

Một tờ ghi chú chứa chuỗi sau:

```text
ZmxhZ3tyZWFkX3RoZV9jbHVlfQ==
```

Gợi ý duy nhất: “Đổi cách biểu diễn, thông điệp sẽ hiện ra.”

## Quan sát trước khi thử

Chuỗi chỉ có chữ cái, chữ số và dấu `=` ở cuối. Đây là một dấu hiệu thường gặp của Base64. Tuy vậy, nhìn giống chưa đủ để kết luận; bước tiếp theo cần kiểm chứng bằng một bộ giải mã.

| Quan sát | Giả thuyết |
| --- | --- |
| Bảng ký tự khá hẹp | Có thể là dữ liệu được mã hóa biểu diễn |
| Kết thúc bằng `==` | Có thể có phần đệm Base64 |
| Gợi ý nói đến biểu diễn | Nên thử giải mã trước khi nghĩ đến mật mã |

## Kiểm chứng bằng Python

Thư viện chuẩn của Python đã có `base64`, nên bài tập này không cần cài thêm gói:

```python
import base64

encoded = "ZmxhZ3tyZWFkX3RoZV9jbHVlfQ=="
decoded = base64.b64decode(encoded, validate=True)
print(decoded.decode("utf-8"))
```

Kết quả:

```text
flag{read_the_clue}
```

Tham số `validate=True` giúp từ chối ký tự không hợp lệ. Sau đó, dữ liệu byte được chuyển thành chuỗi UTF-8 để đọc. Nếu dữ liệu không phải văn bản UTF-8, bước chuyển đổi có thể báo lỗi; khi ấy cần kiểm tra dữ liệu thay vì đoán tiếp.

## Điều rút ra

- Ghi rõ dữ liệu đầu vào để lời giải có thể tái hiện.
- Tách quan sát khỏi kết luận; luôn kiểm chứng giả thuyết.
- Chỉ giữ những thử nghiệm giúp giải thích lời giải.

> Base64 là cách biểu diễn dữ liệu, không phải cơ chế bảo mật. Ai có chuỗi này đều có thể giải mã.

Với một writeup lớn hơn, có thể bổ sung các hướng thử chưa thành công và lý do đổi hướng. Điều quan trọng là người đọc hiểu được quyết định ở mỗi bước, thay vì chỉ nhìn thấy một lệnh và một đáp án.

*Đề bài và flag trong bài đều là dữ liệu mẫu do website cung cấp.*
