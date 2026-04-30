from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import requests
from blockchain_engine.models import NormalizedTransaction
from blockchain_engine.network import RetryConfig, request_with_retry

class SolanaConnector:
    def __init__(self, api_url: str, request_timeout: int = 20, retry_config: RetryConfig | None = None) -> None:
        self.api_url = api_url.rstrip("/")
        self.request_timeout = request_timeout
        self.session = requests.Session()
        self.retry_config = retry_config or RetryConfig()

    def _rpc(self, method: str, params: list[Any]) -> Any:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        response = request_with_retry(
            self.session,
            "POST",
            self.api_url,
            json=payload,
            timeout=self.request_timeout,
            retry_config=self.retry_config,
        )
        response.raise_for_status()
        body = response.json()
        if body.get("error"):
            raise RuntimeError(f"Solana RPC error: {body['error']}")
        return body["result"]

    def get_transactions(self, address: str, limit: int = 50) -> list[NormalizedTransaction]:
        try:
            # 1. Get transaction signatures
            signatures = self._rpc("getSignaturesForAddress", [address, {"limit": limit}])
            results: list[NormalizedTransaction] = []
            
            for sig_info in signatures:
                sig = sig_info["signature"]
                # 2. Get transaction details
                tx_data = self._rpc("getTransaction", [sig, {"encoding": "json", "maxSupportedTransactionVersion": 0}])
                if not tx_data:
                    continue
                
                meta = tx_data.get("meta", {})
                tx = tx_data.get("transaction", {})
                msg = tx.get("message", {})
                account_keys = msg.get("accountKeys", [])
                
                # Basic lamport change detection
                pre_bal = meta.get("preBalances", [0])[0]
                post_bal = meta.get("postBalances", [0])[0]
                value = abs(post_bal - pre_bal) / 10**9
                
                timestamp = datetime.fromtimestamp(
                    tx_data.get("blockTime", 0) or 0,
                    tz=timezone.utc,
                )
                
                results.append(
                    NormalizedTransaction(
                        chain="solana",
                        tx_hash=sig,
                        block_number=tx_data.get("slot"),
                        timestamp=timestamp,
                        from_address=account_keys[0] if account_keys else "",
                        to_address=address,
                        value=value,
                        asset="SOL",
                        direction="in" if post_bal > pre_bal else "out",
                        raw=tx_data,
                    )
                )
            return results
        except Exception:
            return []

    def get_balance(self, address: str) -> float:
        try:
            result = self._rpc("getBalance", [address])
            return result.get("value", 0) / 10**9
        except Exception:
            return 0.0

    def get_code(self, address: str) -> str:
        return "0x" # Solana doesn't use EVM bytecode
