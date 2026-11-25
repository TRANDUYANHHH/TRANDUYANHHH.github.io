Tài khoản root của hệ thống linux cho phép truy cập đầy đủ vào hệ điều hành. Trong quá trình truy cập, bạn có thể có quyền thấp khi truy cập hệ thống và leo thang lên đặc quyền cho người dùng root. Việc có quyền xâm nhập hoàn toàn vào máy chủ giúp chúng ta có thể thu thập lưu lượng truy cập và truy cập vào các tệp có nội dung nhạy cảm, từ đó có thể sử dụng với những truy cập sâu hơn vào môi trường. Hơn nữa, nếu máy Linux bị tấn công đã join vào domain thì có thể sự dụng nó để lấy NTLM hash và bắt đầu tấn công Active Directory.

**Enumeration**

Enumeration là chìa khóa cho leo thang đặc quyền. Một vài các công cụ có thể giúp bạn enum hệ thống, tuy nhiên quan trọng nhất là bạn phải hiểu được những thông tin mình thu thập được là gì và có thể sử dụng nó để làm được những gì. Khi bạn có được inital shell để truy cập vào hệ thống, việc cần thiết tiếp theo là bạn phải kiểm tra một vài chi tiết quan trọng
- OS version: Biết được bản phân phối, cho bạn thông tin để bạn có thể sử dụng các công cụ có sẵn phù hợp. Tiếp đến là phiên bản hệ điều hành, vì có thể đã có một cách khai thác lỗ hổng được công khai.
- Kernel Version: giống như os version, có thể đã có một bản khai thác được công khai. Việc khai thác kernel có thể khiến cho hệ thống bị mất ổn định hoặc hoàn toàn sập. Hãy cẩn thận khi khai thác kernel, phải hiểu việc khai thác như thế nào và nó gây ảnh hưởng như thế nào đến hệ thống
- Running Service: Việc biết được các dịch vụ đang chạy trên hệ thống là cực kì quan trọng, đặc biệt là các dịch vụ đang chạy với quyền root. Khi dịch vụ đang chạy với quyền root bị lỗi cấu hình hoặc chứa lỗ hổng, có thể dễ dàng tận dụng nó để leo thang đặc quyền. Rất nhiều lỗ hổng được phát hiện mà chạy rất nhiều dịch vụ phổ biến. 

**Liệt kê các tiến trình đang được chạy**

```
tranDuyAnh10@htb[/htb]$ ps aux | grep root 
root 1 1.3 0.1 37656 5664 ? Ss 23:26 0:01 /sbin/init root 2 0.0 0.0 0 0 ? S 23:26 0:00 [kthreadd] root 3 0.0 0.0 0 0 ? S 23:26 0:00 [ksoftirqd/0] root 4 0.0 0.0 0 0 ? S 23:26 0:00 [kworker/0:0] root 5 0.0 0.0 0 0 ? S< 23:26 0:00 [kworker/0:0H] root 6 0.0 0.0 0 0 ? S 23:26 0:00 [kworker/u8:0] root 7 0.0 0.0 0 0 ? S 23:26 0:00 [rcu_sched] root 8 0.0 0.0 0 0 ? S 23:26 0:00 [rcu_bh] root 9 0.0 0.0 0 0 ? S 23:26 0:00 [migration/0]
```

- Installed Packages and Versions: Tương tự như các dịch vụ thì những package đã out-of-date cũng có thể được tận dụng để leo thang đặc quyền
- Logged in Users: Biết được các người dùng có trong hệ thống và những gì hộ có thể làm có thể cho biết được khả năng tiềm tàng nếu leo thang đặc quyền ngang hoặc lên trên

**List Current Terminal-Attached Processes** 
```
tranDuyAnh10@htb[/htb]$ ps au 
USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND root 1256 0.0 0.1 65832 3364 tty1 Ss 23:26 0:00 /bin/login -- cliff.moore 1322 0.0 0.1 22600 5160 tty1 S 23:26 0:00 -bash shared 1367 0.0 0.1 22568 5116 pts/0 Ss 23:27 0:00 -bash root 1384 0.0 0.1 52700 3812 tty1 S 23:29 0:00 sudo su root 1385 0.0 0.1 52284 3448 tty1 S 23:29 0:00 su root 1386 0.0 0.1 21224 3764 tty1 S+ 23:29 0:00 bash shared 1397 0.0 0.1 37364 3428 pts/0 R+ 23:30 0:00 ps au
```

- User Home Directories: Nếu thư mục home của các người dùng khác có thể truy cập được, ta có thể tìm được SSH key ở trong đó, có thể dùng nó để truy cập, hoặc file cấu hình có chứ thông tin đăng nhập. Không ít khi chúng ta tìm thấy được thông tin đăng nhập dùng để truy nhập vào hệ thống hoặc thậm chí là xâm nhập vào môi trường Active Directory
**Home directory contents**
```
tranDuyAnh10@htb[/htb]$ ls /home 
backupsvc bob.jones cliff.moore logger mrb3n shared stacey.jenkins
```

- Chúng ta có thể check xem có thể đọc được file .bash_history không, từ đó có thể biết được các câu lệnh đang sử dụng hoặc có thể nhìn vào các file cấu hình để xem có tìm được khóa SSH không.
```
tranDuyAnh10@htb[/htb]$ ls -la /home/stacey.jenkins/ 
total 32 
drwxr-xr-x 3 stacey.jenkins stacey.jenkins 4096 Aug 30 23:37 . 
drwxr-xr-x 9 root root 4096 Aug 30 23:33 .. 
-rw------- 1 stacey.jenkins stacey.jenkins 41 Aug 30 23:35 .bash_history 
-rw-r--r-- 1 stacey.jenkins stacey.jenkins 220 Sep 1 2015 .bash_logout 
-rw-r--r-- 1 stacey.jenkins stacey.jenkins 3771 Sep 1 2015 .bashrc 
-rw-r--r-- 1 stacey.jenkins stacey.jenkins 97 Aug 30 23:37 config.json 
-rw-r--r-- 1 stacey.jenkins stacey.jenkins 655 May 16 2017 .profile 
drwx------ 2 stacey.jenkins stacey.jenkins 4096 Aug 30 23:35 .ssh
```
- Nếu bạn có thể tìm được SSH key, bạn có thể khởi tại một phiên SSH đến máy chủ vào có thể giao tiếp ổn định tới máy chủ. Khóa SSH cũng có thể được sử dụng để truy nhập vào các hệ thống khác trong mạng. Ít nhất, hãy kiểm tra bộ nhớ đệm ARP để xem các máy nào đang truy cập và đối chiếu chúng với bất kì SSH private key nào có thể sử dụng được
**SSH Directory Contents**
```
tranDuyAnh10@htb[/htb]$ ls -l ~/.ssh 
total 8 
-rw------- 1 mrb3n mrb3n 1679 Aug 30 23:37 id_rsa 
-rw-r--r-- 1 mrb3n mrb3n 393 Aug 30 23:37 id_rsa.pub
```
- Một điều cũng quan trọng nữa là check xem trong .bash_history xem có thể có mật khẩu được đưa vào như các tham số cho một số tác vụ như git repos, cron jobs, ... Xem xem người dùng đã làm những gì để cho bạn biết thêm thông tin về server mà bạn đang ở trong và có ý tương để leo thang đặc quyền
- Đặc quyền sudo: Sudo có thể giúp bạn chạy lệnh với quyền của người khác. Thông thường bạn phải cần thông tin đăng nhập của người khác để chạy được quyền đó. Tuy nhiên, một số lệnh được đặt với đặc quyền là NOPASSWD tức là có thể chạy với tư cách của người dùng khác mà không cần mật khẩu. Không phải tất cả các lệnh, kể cả khi được chạy với quyền root mà chúng ta có thể leo thang đặc quyền. 
- File cấu hình: Có thể chứa thông tin nhạy cảm, rất đáng để chúng ta kiểm tra những file có đuôi conf, hoặc config nơi có thể chưa một vài thông tin nào đó, may mắn có thể là tài khoản mật khẩu, ...
- Readable Shadow files: nếu file này mà đọc được, ta có thể lấy được hash mật khẩu người dùng, tuy không thể truy nhập trực tiếp với thông tin này nhưng có thể brute-force để tìm ra mật khẩu dựa vào mã hash.
- Password hashes trong /etc/passwd: Ta cũng có thể tìm thấy hash trong file /etc/passwd, file mà có thể đọc được bởi mọi người. Nhưng hiếm khi có thể tìm thấy trong này.
- Cron jobs: Cron jobs trong linux giống như lập lịch cho các tác vụ trên windows. Thường thiết lập cho các công việc backup và bảo trì. Nếu bị lỗi cấu hình như đường dẫn tương đối hoặc quyền truy cập yếu, có thể dẫn đến leo thang đặc quyền.
- Unmounted File Systems and Additional Drives: Nếu bạn khám phá ra các drive khác hoặc mount được các hệ thống file chưa được mount thì bạn có thể tìm thêm được những thông tin từ nó và dùng nó để leo thang đặc quyền.
- SETUID và SETGUID permission: Tệp thực thi có thể chạy với quyền của người dùng khác mà không cần lấy được quyền của người dùng khác. Việc này có thể được tận dụng để leo thang đặc quyền.
- Writeable Directories: Nếu một thư mục cho bạn quyền để ghi, bạn có thể tải các công cụ về thư mục đó, hoặc nếu như thư mục đó có chưa file được chạy bởi cronjobs, bạn có thể sử dụng nó để leo thang đặc quyền.
- Writeable files: Một file có thể được chỉnh sửa, giả sử là file đó được cronjob gọi, thì bạn có thể chỉnh sửa để thực hiện theo ý của bạn - leo thang đặc quyền chẳng hạn.