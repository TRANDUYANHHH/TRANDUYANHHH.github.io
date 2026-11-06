"""Local preview. Run build.py first; Ctrl+C stops the server."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse
import webbrowser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preview the built blog locally.")
    parser.add_argument("--open", action="store_true", dest="open_browser", help="Open the default browser when the server is ready")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "dist"
    if not (root / "index.html").exists():
        raise SystemExit("Run python scripts/build.py first.")
    server = ThreadingHTTPServer(("127.0.0.1", 4173), partial(SimpleHTTPRequestHandler, directory=str(root)))
    print("Local: http://127.0.0.1:4173", flush=True)
    if options.open_browser:
        webbrowser.open("http://127.0.0.1:4173/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
