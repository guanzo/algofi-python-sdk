# IMPORTS

# external
from concurrent.futures import ThreadPoolExecutor
from algosdk.v2client.indexer import IndexerClient

# local
from .algofi_user import AlgofiUser
from .asset_config import ASSET_CONFIGS

# lending
from .lending.v2.lending_client import LendingClient
from .staking.v2.staking_client import StakingClient
from .amm.v1.amm_client import AMMClient
from .interfaces.interface_client import InterfaceClient
from .governance.v1.governance_client import GovernanceClient


class AlgofiClient:
    def __init__(self, network, algod, indexer):
        """A client for the algofi protocol

        :param network: a network configuration key
        :type network: :class:`Network`
        :param algod: Algod client
        :type algod: :class:`AlgodClient`
        :param indexer: Algorand indexer client
        :type indexer: :class:`IndexerClient`
        """

        self.network = network
        self.algod = algod
        self.indexer = indexer
        # load AlgoExplorer historical indexer
        self.historical_indexer = IndexerClient(
            "", "https://indexer.algoexplorerapi.io/", headers={"User-Agent": "algosdk"}
        )

        # assets
        self.assets = ASSET_CONFIGS[self.network]

        with ThreadPoolExecutor() as e:
            lendingFuture = e.submit(LendingClient, self)
            stakingFuture = e.submit(StakingClient, self)
            ammFuture = e.submit(AMMClient, self)
            #governanceFuture = e.submit(GovernanceClient, self)

            # lending
            self.lending = lendingFuture.result()

            # amm
            self.amm = ammFuture.result()

            # InterfaceClient depends on lending & amm
            interfaceFuture = e.submit(InterfaceClient, self)

            # staking
            self.staking = stakingFuture.result()

            # interfaces
            self.interfaces = interfaceFuture.result()

            # governance
            #self.governance = governanceFuture.result()

    def get_user(self, address):
        """Creates an :class:`AlgofiUser` object for specific address

        :param address: string address of the user primary wallet
        :type address: str
        :return: Python representation of the algofi user
        :rtype: :class:`AlgofiUser`
        """

        return AlgofiUser(self, address)
