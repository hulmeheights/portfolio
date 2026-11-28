"""Screenshot mockups: python m/shoot.py <slug>...  (run from repo root; serves the repo locally). Writes m/<slug>/phone.jpg (first screen) and m/<slug>/full.jpg."""
import http.server, socketserver, sys, threading, functools
from playwright.sync_api import sync_playwright
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start(); port = srv.server_address[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    for s in sys.argv[1:]:
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg.goto(f"http://127.0.0.1:{port}/m/{s}/", wait_until="networkidle"); pg.wait_for_timeout(800)
        pg.screenshot(path=f"m/{s}/phone.jpg", type="jpeg", quality=78)
        pg.add_style_tag(content=".bar{display:none!important}header{position:static!important}")
        pg.screenshot(path=f"m/{s}/full.jpg", type="jpeg", quality=70, full_page=True)
        print("shot", s, flush=True)
    b.close()
srv.shutdown()
