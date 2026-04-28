from __future__ import annotations

from typing import Any

from blockchain_engine.indexer import SqliteIndexer
from blockchain_engine.models import NormalizedTransaction


class ExplorerService:
    def __init__(self, indexer: SqliteIndexer) -> None:
        self.indexer = indexer

    def get_address_transactions(self, chain: str, address: str, limit: int = 25) -> list[dict[str, Any]]:
        return self.indexer.read_by_address(chain=chain, address=address, limit=limit)

    def get_transaction(self, tx_hash: str) -> dict[str, Any] | None:
        return self.indexer.read_by_tx_hash(tx_hash)

    @staticmethod
    def summarize_address(balance: dict[str, Any], transactions: list[dict[str, Any]]) -> dict[str, Any]:
        incoming = sum(tx["value"] for tx in transactions if tx["direction"] == "in")
        outgoing = sum(tx["value"] for tx in transactions if tx["direction"] == "out")
        return {
            "balance": balance,
            "transaction_count": len(transactions),
            "incoming_total": incoming,
            "outgoing_total": outgoing,
            "transactions": transactions,
        }
