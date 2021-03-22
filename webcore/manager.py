import datetime
import logging
from tibber.schema import Price
from webcore.pusher import update_piston
from tibber.queries import query_today_prices


class PriceManager:
    
    def __init__(self):
        logging.info('Tibber API queried')
        self.prices = query_today_prices()
        logging.info('Tibber API returned prices')
        self.update_webcore_piston()

    def _sort(self, reverse=False) -> list(Price):
        return sorted(self.prices, key=lambda x: x.total, reverse=reverse)

    def _sort_prices(self, high_prices=True, hours=4) -> list(Price):
        return self._sort(reverse=high_prices)[0:hours]

    @staticmethod
    def _now_rounded() -> datetime.date:
        return datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    def is_energy_price(self, hours, high_prices=False) -> bool:
        for price in self._sort_prices(high_prices, hours):
            if self._now_rounded() is price.starts_at:
                return price

    def power_price(self):
        if self.is_energy_price(high_prices=False, hours=6):
            level = "CHEAP"
        elif self.is_energy_price(high_prices=True, hours=3):
            level = "EXPENSIVE"
        else:
            level = "MODERATE"

        logging.info(f'Prices are now at {level} level')
        return level

    def get_price_level_now(self):
        return self.power_price()

    def update_webcore_piston(self):
        return update_piston(level=self.get_price_level_now())

    """
    To update the PriceManager instance daily with prices from Tibber 
    """
    def get_tibber_daily_prices(self):
        self.prices = []
        self.prices = query_today_prices()


if __name__ == "__main__":

    manager = PriceManager()
    print(manager.is_energy_price(hours=4))
    print(manager.get_price_level_now())

