# Tiến độ – Đọc KT Hằng Ngày (web)

## Current State (hiện trạng)
- Last Updated: 27/11/2026
- Feature đang làm: không (feat-001…008 xong; feat-009, feat-010 bị chặn vì bản quyền)
- Bản đang phát hành: sw `dkt-v12`, WEB_UPDATED "26/11/2026 (bản 4)"

## Đã xong
- Cách đọc (cuộn dọc, tối đa 4 ngôn ngữ, nhãn) – commit 8acf372
- Harness: feature_list.json, progress.md, session-handoff.md, init.sh, tests/smoke.py

## What's Next (tiếp theo)
1. Khi David có giấy phép H'Mông: chuyển PDF HWB → `hwb.json` (cùng cấu trúc vie1925.json), thêm vào `LANGS`, chạy ./init.sh.
2. Đưa phần đọc sách giấy (feat-005) vào smoke test.
3. Bản APK (kho doc-kt-hang-ngay) chưa nhận các tính năng web từ 23/11.

## Blocker / rủi ro
- H'Mông HWB, Dao: bản quyền (xem feature_list.json).
- Ngôn ngữ phụ không nằm trong `FILES` của sw.js; chỉ lưu ngoại tuyến sau lần tải đầu (có chủ ý).

## Quyết định
- Chỉ dùng văn bản phạm vi công cộng hoặc có giấy phép.
- Từ 3 ngôn ngữ trở lên chỉ gợi ý cuộn dọc, không ép.

## Bằng chứng
- `./init.sh` → xem session-handoff.md (bảng kết quả).
