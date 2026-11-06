---
title: Viết bài đầu tiên, bắt đầu từ điều nhỏ nhất
description: Một cấu trúc đơn giản để biến ghi chú rời rạc thành bài blog hoặc writeup dễ đọc.
date: 2026-11-07
category: Blog
tags: ["Markdown", "Viết lách"]
featured: true
---

Một bài viết hữu ích không nhất thiết phải bắt đầu bằng một ý tưởng lớn. Đôi khi, nó chỉ cần trả lời một câu hỏi vừa gặp, giải thích một lỗi mất khá lâu để tìm ra, hoặc lưu lại cách làm để lần sau không phải tìm kiếm từ đầu.

## Bắt đầu bằng một câu hỏi

Trước khi viết, thử hoàn thành câu này: “Sau khi đọc, người đọc có thể…”. Nếu câu trả lời còn quá rộng, hãy thu nhỏ chủ đề. “Hiểu Git” khó viết hơn nhiều so với “Biết cách khôi phục một file vừa sửa nhầm”.

Một cấu trúc ngắn thường đã đủ:

1. Bối cảnh: đang làm gì và gặp vấn đề nào?
2. Cách tiếp cận: đã kiểm tra hoặc thử những gì?
3. Lời giải: bước nào thực sự giải quyết vấn đề?
4. Ghi nhớ: điều gì có thể dùng lại lần sau?

## Dùng Markdown để giữ nhịp viết

Markdown cho phép tập trung vào nội dung mà vẫn trình bày rõ tiêu đề, liên kết, danh sách và đoạn mã. Ví dụ:

```markdown
## Điều vừa học

Đây là một ý **quan trọng** và một từ *cần nhấn mạnh*.

- Một quan sát
- Một điều cần kiểm tra thêm
```

Khi đưa code vào bài, ghi tên ngôn ngữ sau dấu mở khối. Đừng chỉ đưa ra kết quả; hãy giải thích đầu vào, cách chạy và điều cần chú ý.

```python
def greet(name):
    return f"Xin chào, {name}!"

print(greet("người đọc"))
```

> Viết cho người đọc, nhưng cũng viết cho chính mình của vài tháng sau.

## Chỉnh một lượt trước khi đăng

Đọc lại phần mở đầu và bỏ những câu chưa giúp người đọc hiểu vấn đề. Kiểm tra xem mỗi tiêu đề có mô tả đúng phần bên dưới hay không. Nếu một đoạn quá dài, tách nó theo từng ý.

Cuối cùng, đặt một tiêu đề cụ thể và viết mô tả ngắn. Một bài nhỏ, rõ ràng và được đăng hôm nay thường hữu ích hơn một bản nháp hoàn hảo vẫn nằm trong thư mục.

*Bài mẫu để bạn thử giao diện; hãy sửa hoặc thay bằng câu chuyện của mình.*
