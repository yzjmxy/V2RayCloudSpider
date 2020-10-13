import sys

sys.path.append('/qinse/V2RaycSpider0925')

import time
import schedule


def deploy_engine():
    from spiderNest.SSRcS_xjcloud import UFO_Spider
    UFO_Spider().start()


schedule.every(1).hour.do(deploy_engine())

while True:
    schedule.run_pending()
    time.sleep(1)
