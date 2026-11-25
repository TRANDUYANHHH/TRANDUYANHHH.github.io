---
title: Đọc ba dòng log của một lượt tải lại
description: "Ghép các lần thử theo cùng mã công việc để biết lượt tải đã kết thúc ra sao."
date: 2026-11-13 08:15:00 +0700
categories: [Writeup]
tags: [log, http, phan-tich-du-lieu]
---

Đây là ba dòng log minh họa của một ứng dụng tải báo cáo. Dòng đầu ghi lỗi HTTP 503. Lượt tải cuối cùng ra sao?

```text
09:00:01 job=R72 attempt=1 status=503
09:00:02 job=R73 attempt=1 status=200
09:00:04 job=R72 attempt=2 status=200
```

## Nhóm theo công việc

Hai dòng có cùng `job=R72` ghi hai lần thử của cùng một công việc. Dòng ở giữa thuộc `R73`, một công việc khác diễn ra trong lúc `R72` chờ thử lại.

## Đọc kết quả cuối

Lần tải đầu của `R72` nhận 503, mã cho biết dịch vụ tạm thời không thể xử lý yêu cầu. Lần tải thứ hai nhận 200 sau ba giây. Theo dữ liệu mẫu, yêu cầu đã thành công ở lần thử thứ hai. Nếu cần kiểm tra báo cáo đã được lưu xuống đĩa, hãy tìm thêm dòng xác nhận thao tác ghi tệp của ứng dụng.
