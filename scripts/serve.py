#!/usr/bin/env python3
"""Local dev server with caching disabled.

python3 -m http.server sends no Cache-Control header at all, only
Last-Modified — which lets browsers apply heuristic caching and silently
serve a stale copy of css/style.css or a js/*.js file after an edit, even
on a normal refresh of an already-open tab. This wrapper adds
Cache-Control: no-store to every response so what you see always matches
what's on disk.

Usage: python3 scripts/serve.py [port]  (default port: 8080)
"""
import http.server
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    http.server.test(HandlerClass=NoCacheHandler, port=port)
