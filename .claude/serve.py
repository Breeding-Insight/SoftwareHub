"""Serve the rendered site on localhost:8097 without browser caching, so re-renders show up on reload."""
import functools
import http.server
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "_site"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        super().end_headers()


handler = functools.partial(NoCacheHandler, directory=str(SITE))
http.server.ThreadingHTTPServer(("127.0.0.1", 8097), handler).serve_forever()
