import time
import schedule
from webcore.manager import PriceManager


class PriceScheduler:

    daily = "00:00"
    hourly = ":01"

    def __init__(self):
        self.scheduler = schedule
        self.manager = PriceManager()
        self._schedules()

    def _schedules(self):
        # update today prices
        self.scheduler.every().day.at(self.daily).do(lambda: self.manager.get_tibber_daily_prices())
        # run boiler scheduler
        self.scheduler.every().hour.at(self.hourly).do(lambda: self.manager.update_webcore_piston())

    def run(self):
        while True:
            # run_pending
            self.scheduler.run_pending()
            time.sleep(1)


if __name__ == "__main__":

    PriceScheduler().run()
