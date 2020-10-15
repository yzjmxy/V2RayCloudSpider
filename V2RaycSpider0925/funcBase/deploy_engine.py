import sys

sys.path.append('/qinse/V2RaycSpider0925')

import time
import schedule

from spiderNest.SSRcS_xjcloud import UFO_Spider


def deploy_engine():
    UFO_Spider().start()


schedule.every(30).minutes.do(deploy_engine)

while True:
    schedule.run_pending()
    time.sleep(1)
