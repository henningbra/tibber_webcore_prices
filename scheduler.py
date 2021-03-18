import time
import schedule
from webcore.manager import PriceManager


class PriceScheduler:

    daily = "00:00:05"
    hourly = ":1"

    def __init__(self):
        self.scheduler = schedule
        self.manager = PriceManager()
        self._schedules()

    def _schedules(self):
        # update today prices
        self.scheduler.every().day.at(self.daily).do(lambda: self.manager.update_prices())
        # run boiler scheduler
        self.scheduler.every().hour.at(self.hourly).do(lambda: self.manager.power_price())

    def run(self):
        while True:
            # run_pending
            self.scheduler.run_pending()
            time.sleep(1)


if __name__ == "__main__":

    PriceScheduler().run()
