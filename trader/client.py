"""

T212 Client

"""


from trader.account import AccountClient
from trader.historical import HistoricalClient
from trader.instruments import InstrumentsClient
from trader.orders import OrdersClient
from trader.pies import PiesClient
from trader.portfolio import PortfolioClient
from trader.types import T212Server


class T212Client:  # pylint: disable=too-few-public-methods
    def __init__(self, server: T212Server) -> None:
        self.account: AccountClient = AccountClient(server=server)
        self.historical: HistoricalClient = HistoricalClient(server=server)
        self.instruments: InstrumentsClient = InstrumentsClient(server=server)
        self.orders: OrdersClient = OrdersClient(server=server)
        self.pies: PiesClient = PiesClient(server=server)
        self.portfolio: PortfolioClient = PortfolioClient(server=server)
