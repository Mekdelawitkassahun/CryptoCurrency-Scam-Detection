from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ScannerConfig:
    ethereum_rpc_url: str = os.getenv("ETHEREUM_RPC_URL", "https://eth.drpc.org")
    bsc_rpc_url: str = os.getenv("BSC_RPC_URL", "https://bsc.drpc.org")
    polygon_rpc_url: str = os.getenv("POLYGON_RPC_URL", "https://polygon.drpc.org")
    arbitrum_rpc_url: str = os.getenv("ARBITRUM_RPC_URL", "https://arbitrum.drpc.org")
    sepolia_rpc_url: str = os.getenv("SEPOLIA_RPC_URL", "https://sepolia.drpc.org")
    optimism_rpc_url: str = os.getenv("OPTIMISM_RPC_URL", "https://optimism.drpc.org")
    avalanche_rpc_url: str = os.getenv("AVALANCHE_RPC_URL", "https://avalanche.drpc.org")
    fantom_rpc_url: str = os.getenv("FANTOM_RPC_URL", "https://rpcapi.fantom.network")
    base_rpc_url: str = os.getenv("BASE_RPC_URL", "https://base.drpc.org")
    celo_rpc_url: str = os.getenv("CELO_RPC_URL", "https://celo.drpc.org")
    gnosis_rpc_url: str = os.getenv("GNOSIS_RPC_URL", "https://gnosis.drpc.org")
    cronos_rpc_url: str = os.getenv("CRONOS_RPC_URL", "https://cronos.drpc.org")
    moonbeam_rpc_url: str = os.getenv("MOONBEAM_RPC_URL", "https://moonbeam.drpc.org")
    metis_rpc_url: str = os.getenv("METIS_RPC_URL", "https://metis.drpc.org")
    kava_rpc_url: str = os.getenv("KAVA_RPC_URL", "https://evm.kava.io")
    solana_api_url: str = os.getenv("SOLANA_API_URL", "https://api.mainnet-beta.solana.com")
    ethereum_explorer_api_url: str = os.getenv(
        "ETHEREUM_EXPLORER_API_URL",
        "https://api.etherscan.io/v2/api",
    )
    ethereum_blockscout_api_url: str = os.getenv(
        "ETHEREUM_BLOCKSCOUT_API_URL",
        "https://eth.blockscout.com/api/v2",
    )
    bsc_explorer_api_url: str = os.getenv(
        "BSC_EXPLORER_API_URL",
        "https://api.etherscan.io/v2/api",
    )
    bsc_blockscout_api_url: str = os.getenv("BSC_BLOCKSCOUT_API_URL", "")
    polygon_explorer_api_url: str = os.getenv(
        "POLYGON_EXPLORER_API_URL",
        "https://api.etherscan.io/v2/api",
    )
    polygon_blockscout_api_url: str = os.getenv("POLYGON_BLOCKSCOUT_API_URL", "")
    arbitrum_explorer_api_url: str = os.getenv(
        "ARBITRUM_EXPLORER_API_URL",
        "https://api.etherscan.io/v2/api",
    )
    arbitrum_blockscout_api_url: str = os.getenv(
        "ARBITRUM_BLOCKSCOUT_API_URL",
        "https://arbitrum.blockscout.com/api/v2",
    )
    explorer_api_key: str = os.getenv("EXPLORER_API_KEY", os.getenv("ETHERSCAN_API_KEY", ""))
    bitcoin_api_url: str = os.getenv("BITCOIN_API_URL", "https://blockstream.info/api")
    data_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("BLOCKCHAIN_DATA_DIR", "./blockchain_engine/data")
        ).resolve()
    )
    request_timeout: int = 20
    max_rpc_scan_blocks: int = int(os.getenv("MAX_RPC_SCAN_BLOCKS", "250"))
    request_retries: int = int(os.getenv("REQUEST_RETRIES", "3"))
    request_backoff_seconds: float = float(os.getenv("REQUEST_BACKOFF_SECONDS", "1.0"))

    def ensure_data_dir(self) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir
