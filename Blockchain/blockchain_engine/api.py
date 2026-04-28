from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from blockchain_engine.config import ScannerConfig
from blockchain_engine.scanner import BlockchainScanner


def run_api_server(host: str = "127.0.0.1", port: int = 8055) -> None:
    scanner = BlockchainScanner(ScannerConfig())

    class ApiHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)

            try:
                if parsed.path == "/health":
                    self._send_json({"status": "ok"})
                    return
                if parsed.path == "/screen":
                    payload = scanner.screen_address(
                        chain=_single(query, "chain"),
                        address=_single(query, "address"),
                    )
                    self._send_json(payload, dataclass_like=True)
                    return
                if parsed.path == "/explore/address":
                    payload = scanner.explore_address(
                        chain=_single(query, "chain"),
                        address=_single(query, "address"),
                        limit=int(query.get("limit", ["10"])[0]),
                    )
                    self._send_json(payload)
                    return
                if parsed.path == "/explore/tx":
                    payload = scanner.explore_transaction(_single(query, "tx_hash"))
                    self._send_json(payload or {"message": "not found"}, status=200 if payload else 404)
                    return
                if parsed.path == "/graph":
                    payload = scanner.build_graph(
                        chain=_single(query, "chain"),
                        address=_single(query, "address"),
                        limit=int(query.get("limit", ["10"])[0]),
                    )
                    self._send_json(payload)
                    return
                if parsed.path == "/cluster":
                    payload = scanner.cluster_address(
                        chain=_single(query, "chain"),
                        address=_single(query, "address"),
                        limit=int(query.get("limit", ["10"])[0]),
                    )
                    self._send_json(payload)
                    return
                if parsed.path == "/risk":
                    payload = scanner.scan_address(
                        chain=_single(query, "chain"),
                        address=_single(query, "address"),
                        limit=int(query.get("limit", ["10"])[0]),
                    )
                    self._send_json(payload, dataclass_like=True)
                    return
                if parsed.path == "/alerts":
                    payload = scanner.evaluate_alerts(
                        chain=_single(query, "chain"),
                        address=_single(query, "address"),
                        limit=int(query.get("limit", ["10"])[0]),
                    )
                    self._send_json(payload)
                    return
                if parsed.path == "/watchlist":
                    payload = scanner.watchlist.list_entries()
                    self._send_json(payload)
                    return
                self._send_json({"error": "not found"}, status=404)
            except Exception as exc:  # pragma: no cover
                self._send_json({"error": str(exc)}, status=500)

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send_json(self, payload: object, *, status: int = 200, dataclass_like: bool = False) -> None:
            if dataclass_like:
                body = json.dumps(
                    payload,
                    default=lambda obj: asdict(obj) if is_dataclass(obj) else str(obj),
                    indent=2,
                )
            else:
                body = json.dumps(payload, indent=2)
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    server = ThreadingHTTPServer((host, port), ApiHandler)
    print(f"API server running on http://{host}:{port}")
    server.serve_forever()


def _single(query: dict[str, list[str]], key: str) -> str:
    value = query.get(key, [""])[0]
    if not value:
        raise ValueError(f"Missing query parameter: {key}")
    return value
