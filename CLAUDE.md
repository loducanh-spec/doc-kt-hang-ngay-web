# Bàn giao: Đọc KT Hằng Ngày – bản web (iPhone, Android, máy tính)

Cập nhật: 24/11/2026.

## Là gì
App đọc Kinh Thánh 1925 theo kế hoạch hằng ngày, chạy trên trình duyệt (GitHub Pages: https://loducanh-spec.github.io/doc-kt-hang-ngay-web/). iPhone: mở bằng Safari → Chia sẻ → Thêm vào MH chính.
Có **tài khoản thành viên** (email/mật khẩu): mỗi người một kế hoạch riêng, lưu lên mạng, đăng nhập máy khác đọc tiếp được.

## Nguồn mã
- Bộ đọc lấy nguyên từ bản web Kinh Thánh 1925 **v1.0.22** (kho `loducanh-spec/kinh-thanh-web`, commit 59dea0d "Mục lục: chọn Sách → Đoạn → Câu"): theme "Óc chó & Đất nung", 4 nền, chọn kiểu chữ, đọc thành tiếng, service worker.
- Mô-đun kế hoạch lấy từ app Android `loducanh-spec/doc-kt-hang-ngay` (xem CLAUDE.md ở đó, mục 2 và 4 cho các quyết định và cách tính lộ trình).
- Cập nhật bộ đọc từ bản 1925 mới hơn: chép `index.html` mới của kinh-thanh-web rồi chạy lại các thay đổi như trong commit đầu tiên của kho này (đổi tiền tố localStorage, chèn `#pHome`, `trackMove()` trong `afterMove()`, `endBible()`, tài khoản ở `dkt/<uid>`, mô-đun kế hoạch trước `fetch('vie1925.json')`).

## Khác với bản 1925
- **localStorage tiền tố `dkt.`** (bản 1925 dùng `kt.`): hai app cùng tên miền loducanh-spec.github.io nên phải tách, không được đổi lại.
- **Tài khoản:** dùng chung dự án Firebase `kinh-thanh-1925-cb877` (một tài khoản dùng được cả hai app), nhưng dữ liệu lưu ở **`dkt/<uid>`** (field `data` = JSON `{...payload(), app:'doc-kt-hang-ngay', plan}`), không đụng `users/<uid>` của bản 1925. Cần quy tắc Firestore `match /dkt/{uid} { allow read, write: if request.auth != null && request.auth.uid == uid; }`.
- Gộp kế hoạch giữa các máy: `mergePlan()`. Nhật ký theo ngày lấy bản đọc nhiều hơn; `plans` thêm ngày còn thiếu; `rounds` hợp nhất; `goal/start/pos/speed` lấy theo `tp` (giờ người dùng đổi tiến độ hoặc mục tiêu) mới hơn; vừa đăng nhập (`force`) thì lấy của tài khoản.
- Đăng xuất xóa sạch dữ liệu trên máy (kể cả kế hoạch), dữ liệu vẫn còn trong tài khoản.
- Thẻ tài khoản `#rowAcct` nằm ở màn hình chính: tab Kế hoạch; tab Hôm nay (đặt lên đầu) khi chưa đăng nhập (`placeAcct()`).
- Tô màu, ghi chú, tìm kiếm, Drive đang ẩn bằng CSS; `toggleSel()` trả về ngay.
- Công cụ thử (dữ liệu mẫu, sang ngày mai, tới Khải-huyền 22, xóa dữ liệu): mở link có `#thu`.
- Ảnh báo cáo: hiện ảnh để nhấn giữ lưu; nếu trình duyệt hỗ trợ chia sẻ file (iPhone Safari có) thì có nút "Chia sẻ…".
- **Hồ sơ cá nhân** (`PL.prof={name,group,t}`, tab Kế hoạch): họ tên thật (bắt buộc trước khi lưu ảnh báo cáo) và hội thánh/nhóm. Đồng bộ trong `plan`; Firestore còn ghi thêm field thường `name`, `group`, `email` ở `dkt/<uid>` để sau này làm trang quản lý cho mục sư. Đăng nhập/tạo tài khoản mà chưa có tên thì app nhắc khai.
- **Vòng tròn tiến độ** (`ringCard()`, `ringSVG()`): % lần đọc hiện tại (`roundPct()`, dưới 10% hiện 1 chữ số thập phân), chữ cam ở giữa; có ở tab Hôm nay và Báo cáo. `dayInfo(k)` mô tả tình trạng một ngày (đã đọc xong / đọc dở x/n chương / chưa đọc).
- **Ảnh báo cáo** (`shareImg()`, rộng 1080, cao theo số hàng lịch): đầu ảnh có họ tên, nhóm, email tài khoản, giờ tạo ảnh; vòng tiến độ; tình trạng hôm nay; lịch tháng; chú thích 5 màu ở cuối.
- **Ảnh báo cáo dạng sách** (`shareGrid()`, phương án C David chốt 24/11/2026, là nút chính "Lưu ảnh báo cáo · Chia sẻ"): 66 sách 2 cột (24 sách bên trái), ô tên sách bo góc xanh đậm/cam/tối theo sách đã xong/đang đọc/chưa đọc, mỗi đoạn một vòng tròn 24 đoạn/hàng (xanh lá đã đọc, cam là đoạn kế tiếp `PL.pos`, chỉ viền là chưa đọc); đầu ảnh có tên, nhóm, email, giờ, tình trạng hôm nay, thanh % lần đọc. Ảnh dạng lịch tháng cũ (`shareImg()`) vẫn giữ ở nút phụ. Cả hai dùng `deliverImg()` để hiện/lưu/chia sẻ.
- **Số liệu năm** (`PL.yb[năm]={r,c,t}`, tab Kế hoạch): khai báo số lần đã đọc trọn trong năm trước khi dùng app (r) + đoạn của lần đang đọc (c = vị trí lúc lưu, trừ phần đã đọc trong app). Năm có khai báo: `yearTarget()` = mục tiêu cả năm (goal × toàn văn) trừ phần đã khai báo, không chia tỉ lệ; số lần đếm tiếp từ r+1 (`curRound()`, thông báo Lần N). `yearCh(y)` = tổng đoạn đã đọc trong năm (khai báo + trong app), dùng cho báo cáo cuối năm.
- **Sách đang đọc** (`bookInfo()`, `bookCard()`): lưới đoạn của sách hiện tại (xanh đã đọc, cam đọc hôm nay, viền là đoạn kế tiếp) + thanh tiến độ; **Cả năm** (`yearCard()`): đoạn đã đọc / mục tiêu. Ảnh báo cáo có 2 thanh: sách đang đọc, cả năm.
- Từ ngữ: Kinh Thánh 1925 gọi chương là **đoạn**; giao diện kế hoạch dùng "đoạn".
- Biểu tượng: phương án C (vòng tiến độ quanh thánh giá), `icon-180/192/512.png`.

## Phát hành
- Sửa xong: đổi `VER` trong `sw.js` (dkt-vN) và `WEB_UPDATED` trong `index.html`, push lên `main`; GitHub Pages tự cập nhật sau khoảng 1 phút.
- Thử bằng Playwright ở 360/390/412 px; giả lập Firebase bằng `page.route` (identitytoolkit, firestore) để thử đăng ký/đăng nhập/đăng xuất mà không tạo tài khoản thật.

## Cách làm việc với David
- Tiếng Việt có dấu, ngắn gọn; nêu rõ sự thật và giả định.
- Commit kết thúc bằng hai dòng `Co-Authored-By` và `Claude-Session` theo quy định của phiên.
