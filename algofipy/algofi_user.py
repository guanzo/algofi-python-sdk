# IMPORTS

# global
from concurrent.futures import ThreadPoolExecutor, as_completed
from .lending.v2.lending_user import LendingUser
from .staking.v2.staking_user import StakingUser
from .governance.v1.governance_user import GovernanceUser
from .state_utils import *


# INTERFACE


class AlgofiUser:
    def __init__(self, algofi_client, address):
        """The python representation of an algofi user

        :param algofi_client: a client for the algofi protocol
        :type algofi_client: :class:`AlgofiClient`
        :param address: user wallet address
        :type address: str
        """

        self.algofi_client = algofi_client
        self.address = address

        # lending
        self.lending = LendingUser(self.algofi_client.lending, self.address, load_state=False)

        # staking
        self.staking = StakingUser(self.algofi_client.staking, self.address)

        # governance
        #self.governance = GovernanceUser(self.algofi_client.governance, self.address)

        self.load_state()

    def load_state(self, block=None):
        """Populates state on the :class:`AlgofiUser` object

        :param block: block at which to query algofi user's state
        :type block: int, optional
        """

        indexer = (
            self.algofi_client.historical_indexer
            if block
            else self.algofi_client.indexer
        )

        with ThreadPoolExecutor() as e:
            futures = [
                e.submit(self.lending.load_state, block=block),
                e.submit(self.staking.load_state, block=block),
                #e.submit(self.governance.load_state, block=block),
            ]
            balancesFuture = e.submit(get_balances, indexer, self.address, block=block)

            for future in as_completed(futures):
                future.result()

            self.balances = balancesFuture.result()

    def is_opted_in_to_asset(self, asset_id):
        """Checks if user is opted is into a given asset

        :param asset_id: id of the asset
        :type asset_id: int
        :return: True if opted in, False otherwise
        :rtype: bool
        """

        return asset_id in self.balances
