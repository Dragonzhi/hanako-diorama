#!/usr/bin/env python3
"""Hanako 箱庭站点服务：静态文件 + 灵感碎片 API"""
import json
import os
import secrets
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
IDEAS_FILE = os.path.join(DATA_DIR, "ideas.json")
TOKEN = "zk-diorama-8f3a"  # 防随手乱写的简单防线


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)

    # ---------- 工具 ----------
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _load_ideas(self):
        if not os.path.exists(IDEAS_FILE):
            return []
        try:
            with open(IDEAS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_ideas(self, items):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(IDEAS_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    # ---------- 路由 ----------
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/ideas":
            items = self._load_ideas()
            items.reverse()  # 新的在前
            self._json(200, {"ideas": items})
            return
        super().do_GET()

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/api/ideas":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length) if length else b"{}"
                data = json.loads(raw or b"{}")
                if data.get("token") != TOKEN:
                    self._json(403, {"error": "token 无效"})
                    return
                content = (data.get("content") or "").strip()
                tag = (data.get("tag") or "其他").strip()[:20]
                if not content:
                    self._json(400, {"error": "内容为空"})
                    return
                items = self._load_ideas()
                item = {
                    "id": secrets.token_hex(4),
                    "content": content[:600],
                    "tag": tag,
                    "date": time.strftime("%Y-%m-%d"),
                    "time": time.strftime("%H:%M"),
                }
                items.append(item)
                self._save_ideas(items)
                self._json(200, {"ok": True, "item": item})
            except Exception as e:
                self._json(400, {"error": str(e)})
            return
        self._json(404, {"error": "not found"})

    def do_DELETE(self):
        path = self.path.split("?")[0]
        if path.startswith("/api/ideas/"):
            iid = path.rsplit("/", 1)[-1]
            items = [i for i in self._load_ideas() if i["id"] != iid]
            self._save_ideas(items)
            self._json(200, {"ok": True})
            return
        self._json(404, {"error": "not found"})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8421
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Hanako diorama server on :{port}", flush=True)
    server.serve_forever()
