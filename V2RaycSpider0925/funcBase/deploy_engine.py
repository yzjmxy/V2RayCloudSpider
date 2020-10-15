import sys

sys.path.append('/qinse/V2RaycSpider0925')

import os
import time
from datetime import datetime
import schedule

from funcBase import v2rayc_email
from MiddleKey.redis_IO import RedisClient
from config import REDIS_KEY_NAME_BASE


def get_debug_info(tag_info, diy_info, err_info=''):
    return '>> [{}] {} || {} << {}'.format(tag_info, str(datetime.now()).split('.')[0], diy_info, err_info)


rc = RedisClient()
rc_len = {
    'ssr': 1,
    'v2ray': 1,
    'trojan': 1,
}


def deploy_collection_engine(task_class: str):
    """
    :param task_class: v2ray,ssr,trojan
    """
    global rc_len

    # Canonical input
    if not isinstance(task_class, str):
        print(get_debug_info('ERR', f'The input type is wrong({task_class})'))
        return None
    else:
        if task_class not in ['v2ray', 'ssr', 'trojan']:
            print(get_debug_info('ERR', f'Spelling error in input({task_class}),Please choose from [v2ray,ssr,trojan]'))
            return None
        task_class = task_class.lower()
        rc_len[f'{task_class}'] = rc.__len__(REDIS_KEY_NAME_BASE.format(f'{task_class}'))

    # test the cache of redis list
    try:
        print(get_debug_info('TEST', f'Test cache of the v2rayc-spider ({task_class}) redis task list'))
        if rc_len[f'{task_class}'] >= 20:
            print(get_debug_info('SLEEP', 'Cache is full (20)'))
            return None
    finally:
        print('>> {} <<'.format(''.center(50, '=')))

    # main collect process
    try:
        print(get_debug_info('RUN', f'{task_class} spider engine'))
        os.system('python3 /qinse/V2RaycSpider0925/spiderNest/ssr_xjcloud_spider.py')
        if rc.__len__(REDIS_KEY_NAME_BASE.format(f'{task_class}')) > rc_len[f'{task_class}']:
            print(get_debug_info('NICE', 'Collect Success'))
        else:
            print(get_debug_info('ERR', 'length of redis list has not changed'))
    except Exception as e:
        print(get_debug_info('ERR', f'{task_class} spider engine panic', err_info=''.format(e)))
    finally:
        print('>> {} <<'.format(''.center(50, '=')))


if __name__ == '__main__':

    schedule.every(1).minute.do(deploy_collection_engine, 'ssr')
    # schedule.every(100).minute.do(deploy_collection_engine, 'v2ray')
    # schedule.every(100).minute.do(deploy_collection_engine, 'trojan')
    try:
        deploy_collection_engine('ssr')
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as err:
        print(get_debug_info('ERR', 'deploy panic', err_info=''.format(err)))
        v2rayc_email.prepare(err='{}'.format(err), func_name='/funcBase/deploy_engine/schedule.run/')
