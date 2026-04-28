from __future__ import annotations

import argparse

from blockchain_engine.api import run_api_server


def main() -> None:
    parser = argparse.ArgumentParser(description="Run simple blockchain intelligence API server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8055)
    args = parser.parse_args()
    run_api_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
