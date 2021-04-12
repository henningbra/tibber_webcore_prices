import datetime
import logging
from tibber.schema import Price
from webcore.pusher import update_piston
from tibber.queries import query_today_prices
import settings


class PriceManager:
    
    def __init__(self):
        logging.info('Tibber API queried')
        self.prices = query_today_prices()
        logging.info('Tibber API returned prices')
        self.update_webcore_piston()

    def _sort(self, reverse) -> list(Price):
        return sorted(self.prices, key=lambda x: x.total, reverse=reverse)

    def _sort_prices(self, hours, high_prices) -> list(Price):
        return self._sort(reverse=high_prices)[0:hours]

    @staticmethod
    def _now_rounded() -> datetime.date:
        return datetime.datetime.now(settings.TZ).replace(minute=0, second=0, microsecond=0)

    def get_expensive_energy_hours(self, hours) -> list(Price):
        return self._sort_prices(hours=hours, high_prices=True)

    def get_cheap_energy_hours(self, hours) -> list(Price):
        return self._sort_prices(hours=hours, high_prices=False)

    def _get_energy_price_now(self, prices: Price) -> Price:
        result = None
        for price in prices:
            if self._now_rounded() == price.starts_at:
                result = price
        return result

    def get_power_price(self) -> Price:

        cheap_price = self._get_energy_price_now(self.get_cheap_energy_hours(hours=6))
        if cheap_price:
            cheap_price.level = "CHEAP"
            return cheap_price

        expensive_price = self._get_energy_price_now(self.get_expensive_energy_hours(hours=3))
        if expensive_price:
            expensive_price.level = "EXPENSIVE"
            return expensive_price

        moderate_price = self._get_energy_price_now(self.get_expensive_energy_hours(hours=24))
        if moderate_price:
            moderate_price.level = "MODERATE"
            return moderate_price

    def update_webcore_piston(self):
        price = self.get_power_price()
        data = dict(
            total=price.total,
            level=price.level
        )
        return update_piston(data)

    """
    To update the PriceManager instance daily with prices from Tibber 
    """
    def get_tibber_daily_prices(self):
        self.prices = []
        self.prices = query_today_prices()


if __name__ == "__main__":

    manager = PriceManager()
    print(manager.get_power_price())

