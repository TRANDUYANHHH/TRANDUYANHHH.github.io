---
title: Ghi chép để lần sau không bắt đầu lại
description: Một cách lưu kiến thức kỹ thuật ngắn gọn, có ví dụ và đủ ngữ cảnh để tìm lại.
date: 2026-11-05
category: Ghi chép
tags: ["Học tập", "Developer", "Workflow"]
featured: false
---

Đọc một hướng dẫn và hiểu ngay lúc đó là một chuyện. Vài tuần sau, khi cần áp dụng lại, nhớ được chi tiết là chuyện khác. Một ghi chú tốt tạo ra cầu nối giữa hai thời điểm ấy.

## Lưu cả câu hỏi lẫn câu trả lời

Thay vì chép nguyên một tài liệu, hãy ghi lại vấn đề đã khiến mình mở tài liệu đó. Câu hỏi cụ thể sẽ giúp việc tìm lại dễ hơn: “Vì sao đường dẫn ảnh bị lỗi khi website nằm trong thư mục con?” có nhiều ngữ cảnh hơn tiêu đề “Đường dẫn”.

Mỗi ghi chú có thể chỉ cần bốn phần:

- **Câu hỏi:** điều chưa hiểu hoặc việc cần làm.
- **Giải thích:** viết lại bằng lời của mình.
- **Ví dụ:** một trường hợp nhỏ có thể chạy lại.
- **Giới hạn:** khi nào cách này không còn đúng?

## Chọn ví dụ nhỏ nhất

Một ví dụ ngắn dễ kiểm tra và ít bị nhiễu bởi phần còn lại của dự án. Chẳng hạn, khi học về biến đổi mảng trong JavaScript:

```javascript
const notes = ["Markdown", "Git", "JavaScript"];
const labels = notes.map((note) => `#${note}`);

console.log(labels);
// ["#Markdown", "#Git", "#JavaScript"]
```

Ghi thêm một câu: `map()` tạo mảng mới bằng cách áp dụng hàm lên từng phần tử. Mảng `notes` không bị thay thế trong ví dụ này. Câu giải thích nhỏ ấy thường hữu ích hơn một đoạn code đứng riêng.

## Dành chỗ cho điều chưa biết

Một ghi chú không cần tỏ ra hoàn chỉnh. Có thể thêm mục “Cần kiểm tra” cho câu hỏi chưa giải quyết được, hoặc ghi rõ phiên bản công cụ đã dùng khi hành vi phụ thuộc vào môi trường.

> Ghi chú có thể thay đổi. Khi hiểu thêm, hãy sửa lời giải thích cũ và giữ lại ví dụ tốt hơn.

Trước khi kết thúc một buổi học, dành vài phút viết lại điều quan trọng nhất mà không nhìn tài liệu. Chỗ nào khó diễn đạt thường cũng là chỗ cần tìm hiểu thêm. Sau đó, chọn một ghi chú có ích để phát triển thành bài blog.

Không phải mọi ghi chú đều cần xuất bản. Nhưng những điều đã được kiểm tra, giải thích rõ và đặt đúng ngữ cảnh sẽ trở thành nền tảng tốt cho một bài chia sẻ.

*Đây là bài mẫu. Bạn có thể thay bằng những ghi chú học tập thực tế của mình.*
