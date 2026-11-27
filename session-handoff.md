# Bàn giao phiên – 27/11/2026

## Current Objective (mục tiêu)
Kiểm tra toàn bộ app trước khi phát hành bản "Cách đọc" (cuộn dọc, 4 ngôn ngữ); xem PDF tiếng H'Mông David gửi.

## Đã xong
- Dựng harness (harness-creator): feature_list.json, progress.md, init.sh, tests/smoke.py.
- `./init.sh` đạt 50/50 mục.

## Bằng chứng kiểm tra
| Check | Command | Result |
|---|---|---|
| Dữ liệu 5 bản Kinh Thánh cùng 66 sách / 1189 đoạn | ./init.sh | PASS |
| Cú pháp JS, VER sw.js, file trong FILES tồn tại | ./init.sh | PASS |
| 4 tab không tràn chữ (360/390/412 px) | ./init.sh | PASS |
| Lật trang ghi nhận đoạn | ./init.sh | PASS |
| Cách đọc: 4 ngôn ngữ, nhãn, cuộn dọc ghi nhận đoạn | ./init.sh | PASS |
| Khải-huyền 22 → Lần 1 (cuộn dọc) | ./init.sh | PASS |
| Đăng ký giả lập, lưu Firestore | ./init.sh | PASS |
| Ảnh báo cáo Bảng / Vòng tròn / Lịch tháng | ./init.sh | PASS |
| Không lỗi JavaScript | ./init.sh | PASS |

## Files changed
- Mới: feature_list.json, progress.md, session-handoff.md, init.sh, tests/smoke.py
- CLAUDE.md: thêm mục "Quy trình mỗi phiên"

## Blockers
- feat-009 H'Mông HWB: PDF trích từ kinhthanh.httlvn.org, văn bản Hmong Daw 1992/2000 còn bản quyền; chưa chuyển đổi.

## Next Session (bắt đầu phiên sau)
1. `cd doc-kt-hang-ngay-web && cat CLAUDE.md`
2. `./init.sh` (cần python3 + playwright chromium + node; mất khoảng 3 phút)
3. Đọc feature_list.json, `git log --oneline -5`, chọn 1 feature.

## Recommended Next Step (bước tiếp theo)
Chờ David xin phép Thánh Kinh Hội Việt Nam; có giấy phép thì làm feat-009.
