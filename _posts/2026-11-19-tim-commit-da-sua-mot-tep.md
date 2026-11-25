---
title: Tìm commit đã sửa một tệp
description: "Dùng git log và git show để đi từ lịch sử của một tệp đến đúng phần thay đổi cần xem."
date: 2026-11-19 19:30:00 +0700
categories: [Blog]
tags: [git, terminal]
---

Một dòng trong `README.md` đã đổi, và bạn muốn biết thay đổi đó đến từ commit nào. Git có thể lọc lịch sử theo tệp, giúp rút ngắn danh sách cần xem.

## Lọc lịch sử theo đường dẫn

```bash
git log --oneline -- README.md
```

Mỗi dòng kết quả cho biết mã commit rút gọn và tiêu đề commit. Dấu `--` phân cách tùy chọn của lệnh với đường dẫn `README.md`.

## Đọc thay đổi trong commit

Giả sử mã commit cần xem là `a1b2c3d`. Thay mã này bằng kết quả trên máy bạn.

```bash
git show a1b2c3d -- README.md
```

Trong phần diff, dòng bắt đầu bằng `-` là nội dung cũ và dòng bắt đầu bằng `+` là nội dung được thêm. Nếu tệp từng được đổi tên, chạy `git log --follow -- README.md` để xem tiếp lịch sử qua lần đổi tên.
