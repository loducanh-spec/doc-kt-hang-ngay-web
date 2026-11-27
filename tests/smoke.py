#!/usr/bin/env python3
"""Kiểm tra nhanh trước khi phát hành (chạy qua ./init.sh).
Tự bật máy chủ tĩnh, giả lập Firebase bằng page.route, thử ở 360/390/412 px.
Thoát mã khác 0 nếu có lỗi. Cần: python3, playwright (chromium), node."""
import json, os, re, subprocess, sys, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []
def check(ok, name, info=''):
    print(('  PASS ' if ok else '  FAIL ') + name + (' — ' + str(info) if info else ''))
    if not ok: FAIL.append(name)

# 1. Dữ liệu Kinh Thánh: 66 sách, 1.189 đoạn, khớp số đoạn với bản 1925
print('== Dữ liệu')
ref = json.load(open(os.path.join(ROOT, 'vie1925.json'), encoding='utf-8'))
shape = [len(b[2]) for b in ref]
check(len(ref) == 66 and sum(shape) == 1189, 'vie1925.json 66 sách / 1189 đoạn')
for f in ['kjv.json', 'krv1961.json', 'lsg1910.json', 'cuvs1919.json']:
    d = json.load(open(os.path.join(ROOT, f), encoding='utf-8'))
    check([len(b[2]) for b in d] == shape, f + ' cùng cấu trúc đoạn')

# 2. Cú pháp JS, phiên bản
print('== Mã nguồn')
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = '\n'.join(re.findall(r'<script>([\s\S]*?)</script>', html))
open('/tmp/_dkt_check.js', 'w', encoding='utf-8').write('new Function(' + json.dumps(js) + ')')
r = subprocess.run(['node', '/tmp/_dkt_check.js'], capture_output=True, text=True)
check(r.returncode == 0, 'JS trong index.html đúng cú pháp', r.stderr[:200])
sw = open(os.path.join(ROOT, 'sw.js'), encoding='utf-8').read()
check(re.search(r"VER='dkt-v\d+'", sw) is not None, 'sw.js có VER dkt-vN')
files = json.loads(re.search(r'const FILES=(\[.*?\]);', sw).group(1))
missing = [f for f in files if f != './' and not os.path.exists(os.path.join(ROOT, f))]
check(not missing, 'mọi file trong sw.js FILES đều tồn tại', missing)

# 3. Chạy thử trên trình duyệt
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT))
PORT = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{PORT}/index.html'
DB = {}
def route(r):
    u = r.request.url
    if 'identitytoolkit' in u or 'securetoken' in u:
        return r.fulfill(status=200, content_type='application/json', body=json.dumps({'localId': 'U1', 'email': 'an@gmail.com', 'idToken': 'T', 'refreshToken': 'R', 'expiresIn': '3600'}))
    if 'firestore' in u:
        if r.request.method == 'GET':
            return r.fulfill(status=200, content_type='application/json', body=json.dumps(DB['U1'])) if 'U1' in DB else r.fulfill(status=404, body='{}')
        DB['U1'] = json.loads(r.request.post_data or '{}'); return r.fulfill(status=200, content_type='application/json', body='{}')
    return r.continue_()

LS = lambda pg, k: pg.evaluate(f"localStorage.getItem('dkt.{k}')")
PLAN = lambda pg: json.loads(LS(pg, 'plan') or '{}')
def overflow(pg, sel):
    return pg.evaluate(f"""[...document.querySelectorAll('{sel}')].filter(e=>e.offsetParent&&e.scrollWidth>e.clientWidth+1).map(e=>e.id||e.className).slice(0,5)""")
def swipe(pg, W, H):
    y = H // 2; pg.mouse.move(W - 30, y); pg.mouse.down()
    for x in range(W - 30, 40, -30): pg.mouse.move(x, y)
    pg.mouse.up(); pg.wait_for_timeout(500)
def home_tab(pg, t): pg.click(f'[data-h={t}]'); pg.wait_for_timeout(300)

with sync_playwright() as p:
    br = p.chromium.launch()
    for W, H in [(360, 760), (390, 844), (412, 880)]:
        print(f'== Màn hình {W}x{H}')
        pg = br.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.route('**/*', route)
        pg.goto(URL + '#thu'); pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(2500)
        for t in ['today', 'report', 'plan', 'acct']:
            home_tab(pg, t); ov = overflow(pg, '#pHome button,#pHome .card')
            check(not ov, f'tab {t}: không tràn chữ', ov)
        # Lật trang: vuốt qua hết Sáng-thế Ký 1 → ghi nhận 1 đoạn
        home_tab(pg, 'today'); pg.click('#hGo'); pg.wait_for_timeout(800)
        for _ in range(25):
            if json.loads(LS(pg, 'pos'))['c'] >= 1: break
            swipe(pg, W, H)
        check(PLAN(pg).get('pos') == 1, 'lật trang: đọc xong Sáng-thế Ký 1 được ghi nhận', PLAN(pg).get('pos'))
        # Cài đặt đọc: 4 ngôn ngữ, cuộn dọc
        pg.click('#stMenu'); pg.wait_for_timeout(300); pg.click('#bSet'); pg.wait_for_timeout(400)
        for k in ['en', 'ko', 'zh']: pg.click(f'.lchip[data-l={k}]'); pg.wait_for_timeout(1500)
        pg.click('.lchip[data-l=fr]'); pg.wait_for_timeout(300)
        st = json.loads(LS(pg, 'set'))
        check(st['langs'] == ['vi', 'en', 'ko', 'zh'], 'chọn tối đa 4 ngôn ngữ theo thứ tự', st['langs'])
        ov = overflow(pg, '#shSet .btn,#shSet .lchip'); check(not ov, 'bảng Cài đặt đọc không tràn chữ', ov)
        pg.click('#segMode [data-v=scroll]'); pg.wait_for_timeout(800); pg.click('[data-shclose]'); pg.wait_for_timeout(300)
        n_lt = pg.evaluate("document.querySelectorAll('#scr .sch:first-child b.lt').length")
        check(n_lt > 0, 'cuộn dọc hiện nhãn ngôn ngữ', n_lt)
        p0 = PLAN(pg)['pos']
        for _ in range(80):
            pg.evaluate("document.getElementById('scr').scrollBy(0,500)"); pg.wait_for_timeout(40)
            if PLAN(pg)['pos'] > p0: break
        check(PLAN(pg)['pos'] == p0 + 1, 'cuộn dọc: cuộn qua hết đoạn được ghi nhận', (p0, PLAN(pg)['pos']))
        # Khải-huyền 22 ở chế độ cuộn dọc → Lần 1
        pg.click('#stMenu'); pg.wait_for_timeout(300); pg.click('#bHome'); pg.wait_for_timeout(400)
        home_tab(pg, 'plan'); pg.evaluate("document.getElementById('hEnd').click()"); pg.wait_for_timeout(300); home_tab(pg, 'today'); pg.click('#hGo'); pg.wait_for_timeout(1000)
        for _ in range(40): pg.evaluate("document.getElementById('scr').scrollBy(0,800)"); pg.wait_for_timeout(60)
        pg.wait_for_timeout(500)
        check(len(PLAN(pg).get('rounds', [])) == 1 and pg.evaluate("document.getElementById('hModal').classList.contains('on')"),
              'đọc hết Khải-huyền 22: thông báo Lần 1')
        pg.evaluate("document.getElementById('hModal').classList.remove('on')")
        # Đăng ký (giả lập), khai tên, tạo ảnh báo cáo 3 kiểu
        pg.click('#stMenu'); pg.wait_for_timeout(300); pg.click('#bHome'); pg.wait_for_timeout(400)
        home_tab(pg, 'acct'); pg.fill('#acEmail', 'an@gmail.com'); pg.fill('#acPass', '123456'); pg.click('#acUp'); pg.wait_for_timeout(2500)
        if pg.query_selector('#hName'): pg.fill('#hName', 'Nguyễn Văn An'); pg.click('#hPfSave'); pg.wait_for_timeout(500)
        check('U1' in DB, 'tài khoản: lưu kế hoạch lên Firestore (giả lập)')
        for stl in ['table', 'grid', 'cal']:
            home_tab(pg, 'report'); pg.click('#hShareAll'); pg.wait_for_timeout(300)
            pg.click(f'#hModal [data-st={stl}]'); pg.click('#hModal [data-a=ok]'); pg.wait_for_timeout(1800)
            ok = pg.evaluate("(()=>{const i=document.querySelector('#hModal img');return !!(i&&i.naturalWidth>=1000)})()")
            check(ok, f'ảnh báo cáo kiểu {stl} tạo được')
            pg.evaluate("document.getElementById('hModal').classList.remove('on')")
        # Tải lại: giữ cài đặt, lật trang vẫn chạy với 4 ngôn ngữ
        pg.evaluate("localStorage.setItem('dkt.set',JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('dkt.set')),{mode:'page'})))")
        pg.reload(); pg.wait_for_timeout(3500); home_tab(pg, 'today'); pg.click('#hGo'); pg.wait_for_timeout(800)
        check(pg.evaluate("document.querySelectorAll('#pgT em.s2').length") > 0, 'tải lại: lật trang hiện bản phụ')
        check(not errs, 'không có lỗi JavaScript', errs[:3])
        pg.close()
    br.close()
srv.shutdown()
print('\nKẾT QUẢ:', 'ĐẠT' if not FAIL else f'{len(FAIL)} mục lỗi: ' + '; '.join(FAIL))
sys.exit(1 if FAIL else 0)
