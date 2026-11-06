# Ghi chép

Blog cá nhân tĩnh lấy cảm hứng từ [Norrsken](https://norrsken.andersnoren.se/): nền tối, chữ monospace, điểm nhấn màu, tên blog ở giữa, bộ chọn chuyên mục và lưới bài viết có ảnh ba cột trên màn hình lớn. Bạn viết nội dung bằng Markdown; GitHub Actions tạo HTML và đăng lên GitHub Pages.

Mã nguồn của dự án được viết độc lập, không sao chép mã theme WordPress Norrsken. Bạn không cần cài WordPress, cơ sở dữ liệu hay dịch vụ máy chủ riêng.

## Đăng lên GitHub Pages

1. Tạo một repository trên GitHub. Có thể đặt tên **`USERNAME.github.io`** để web nằm ở `https://USERNAME.github.io`, hoặc đặt tên khác, ví dụ **`blog`**, để web nằm ở `https://USERNAME.github.io/blog/`. Thay `USERNAME` bằng tài khoản GitHub của bạn. Với GitHub Free, dùng repository public.
2. Đưa **toàn bộ nội dung bên trong thư mục dự án** vào gốc repository: `site.json`, `requirements.txt`, `content/`, `assets/`, `scripts/` và cả thư mục ẩn **`.github/`**. Không đưa nguyên thư mục `ghi-chep` bao ngoài vào repository. Không cần tải thư mục `dist/` lên.
3. Vào **Settings → Pages → Build and deployment → Source**, chọn **GitHub Actions**.
4. Commit lên nhánh **`main`** hoặc **`master`**. Vào tab **Actions**, chờ workflow **Publish blog to GitHub Pages** chạy xong. Nếu đã commit trước bước 3, mở workflow và chọn **Run workflow**.
5. Mở liên kết được hiển thị trong lần deploy hoặc tại **Settings → Pages**.

Workflow tự lấy tên miền và đường dẫn của repository từ GitHub Pages, nên dùng được cả web gốc lẫn web trong thư mục con. Không cần tự sửa đường dẫn khi đổi tên repository. Nếu nhánh mặc định có tên khác `main`/`master`, cập nhật `branches` trong `.github/workflows/pages.yml`.

Nếu tải mã nguồn bằng giao diện web của GitHub, nhớ kiểm tra `.github/workflows/pages.yml` đã xuất hiện. Có thể tạo file này trực tiếp bằng **Add file → Create new file**, nhập đầy đủ tên đường dẫn rồi dán nội dung từ bản gốc.

Hướng dẫn chính thức: [chọn nguồn xuất bản GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [workflow tùy chỉnh](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Cá nhân hóa

Sửa `site.json` để đổi thông tin chung. Giữ file đúng định dạng JSON, có dấu ngoặc kép và không thêm dấu phẩy sau trường cuối:

```json
{
  "title": "Ghi chép",
  "description": "Blog và writeup của mình.",
  "author": "Tên của bạn",
  "tagline": "Học, thử và ghi lại.",
  "github": "https://github.com/USERNAME",
  "email": "",
  "url": "",
  "basePath": ""
}
```

- `title`, `description`, `author`, `tagline`: thông tin blog hiển thị trên website.
- `github`: liên kết hồ sơ GitHub; để `""` nếu chưa muốn hiển thị.
- `email`: địa chỉ email liên hệ; để `""` nếu chưa muốn công khai.
- `url`, `basePath`: có thể để trống khi dùng workflow GitHub Pages, vì workflow tự cấp giá trị phù hợp.

Sửa `content/about.md` để viết trang giới thiệu. Các bài có sẵn là nội dung mẫu; hãy sửa hoặc xóa trước khi dùng blog chính thức.

## Viết bài mới

Tạo file Markdown trong `content/posts/`, ví dụ **`bai-writeup-dau-tien.md`**:

````markdown
---
title: Bài writeup đầu tiên
description: Mô tả ngắn để người đọc biết bài này nói về điều gì.
date: 2026-11-07
category: Writeup
tags: ["CTF", "Python"]
featured: false
---

Mở đầu bằng vấn đề bạn muốn giải quyết.

## Cách tiếp cận

1. Quan sát dữ liệu đầu vào.
2. Kiểm chứng một giả thuyết.
3. Giải thích kết quả.

```python
print("Hello, writeup!")
```

> Một điều đáng nhớ sau khi giải bài.
````

Phần giữa hai dòng `---` là thông tin bài viết. Giữ mỗi trường trên một dòng; `tags` là mảng JSON, `featured` là `true` hoặc `false`. Dùng ngày theo định dạng `YYYY-MM-DD`. Đặt tên file bằng chữ thường không dấu, nối từ bằng dấu `-`; tên này tạo đường dẫn bài. Tiền tố đánh số như `01-` được bỏ khỏi đường dẫn.

Markdown hỗ trợ tiêu đề, chữ đậm/nghiêng, liên kết, danh sách, bảng, trích dẫn và code block có tô màu cú pháp. Với code block, ghi tên ngôn ngữ sau ba dấu backtick, như `python`, `javascript`, `bash` hoặc `text`.

Để thêm ảnh trong bài, lưu ảnh vào `assets/images/` (tự tạo thư mục này) rồi viết `![Mô tả ảnh](assets/images/ten-anh.png)`. Build sẽ tự thêm đường dẫn repository cho ảnh. Muốn giữ một bài ở bản nháp, thêm dòng `draft: true` trong phần thông tin đầu bài; bài đó sẽ không được xuất bản.

Muốn dùng ảnh bìa riêng trên thẻ bài viết và đầu bài, thêm trường tùy chọn `cover: assets/images/my-cover.jpg` vào phần thông tin đầu bài. File ảnh phải thật sự có trong thư mục đó. Bạn cũng có thể dùng một URL ảnh bắt đầu bằng `https://`. Nếu bỏ trường `cover`, blog tự dùng ảnh SVG cực quang mặc định.

Commit file mới lên GitHub để đăng bài. Sửa bài cũ bằng cách sửa file tương ứng rồi commit lại. Xóa file Markdown để gỡ bài khỏi bản website được build tiếp theo.

## Xem thử trên máy

Cần Python 3.12 trở lên (workflow dùng Python 3.13). Trên Windows, giải nén dự án rồi **nhấp đúp `preview.cmd`**. File này sẽ kiểm tra Python, cài hai thư viện cần thiết nếu máy chưa có, tạo website và mở trình duyệt tại **http://127.0.0.1:4173/**. Lần cài thư viện đầu tiên cần mạng. Giữ cửa sổ terminal đang mở trong lúc xem; nhấn `Ctrl+C` để dừng server. Nếu trình duyệt mở trước khi server sẵn sàng, tải lại trang.

Bạn cũng có thể mở terminal ngay trong thư mục dự án và chạy thủ công:

```text
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/serve.py
```

Sau đó mở **http://localhost:4173/**. Nhấn `Ctrl+C` trong terminal để dừng server. Sau khi sửa nội dung hoặc giao diện, chạy lại `python scripts/build.py` rồi tải lại trang trong trình duyệt.

Nếu máy Windows chỉ nhận lệnh `py`, thay `python` bằng `py` trong các lệnh trên. Python chỉ dùng trong lúc tạo website; người đọc nhận các file HTML, CSS và JavaScript tĩnh.

## Cấu trúc chính

```text
.github/workflows/pages.yml  Tự build và đăng lên GitHub Pages
site.json                    Thông tin blog
content/about.md             Trang giới thiệu
content/posts/*.md           Các bài viết
assets/                      Giao diện và tài nguyên tĩnh
scripts/build.py             Tạo website
scripts/serve.py             Xem thử ở localhost
requirements.txt             Thư viện cho bước build
preview.cmd                  Nhấp đúp để xem thử trên Windows
dist/                        Website đã build, không đưa vào Git
```

## Bản quyền

Mã dự án dùng giấy phép MIT, xem `LICENSE`. Cảm hứng thiết kế: **Norrsken** của [Anders Norén](https://andersnoren.se/). Các thư viện Markdown và Pygments có giấy phép riêng của tác giả tương ứng.

Font **Geist Mono** của [Vercel](https://github.com/vercel/geist-font) được đóng gói cùng dự án theo giấy phép **SIL Open Font License 1.1**; bản đầy đủ nằm ở `assets/fonts/OFL.txt`.
