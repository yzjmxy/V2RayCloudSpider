import sys

sys.path.append('/qinse/V2RaycSpider0925')

import os
import time
from datetime import datetime
import threading
import schedule
from funcBase import v2rayc_email
from MiddleKey.redis_IO import RedisClient
from config import REDIS_KEY_NAME_BASE
from spiderNest.preIntro import magic_msg


def get_debug_info(tag_info, diy_info, err_info=''):
    debug_msg = '>> [{}] {} || {} << {}'.format(tag_info, str(datetime.now()).split('.')[0], diy_info, err_info)
    if 'NICE' in tag_info.upper():
        return magic_msg(debug_msg, 'g')
    elif 'ERR' in tag_info.upper():
        return magic_msg(debug_msg, 'r')
    elif 'RUN' in tag_info.upper():
        return magic_msg(debug_msg, 'c')
    elif tag_info == '-OVER-':
        return magic_msg(debug_msg, 'm')
    else:
        return debug_msg


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
        print(get_debug_info('RUN', f'({task_class}) spider engine'))
        if 'linux' in sys.platform:
            if task_class == 'ssr':
                os.system('python3 /qinse/V2RaycSpider0925/spiderNest/action_slaver/xjcloud.py')
            if task_class == 'v2ray':
                os.system('python3 /qinse/V2RaycSpider0925/spiderNest/action_slaver/thessr.py')
                os.system('python3 /qinse/V2RaycSpider0925/spiderNest/action_slaver/ufocloud.py')
            if task_class == 'trojan':
                pass
        else:
            print(get_debug_info('-OVER-', 'Not in deployment mode.Force quit.'))
            exit()

        if rc.__len__(REDIS_KEY_NAME_BASE.format(f'{task_class}')) > rc_len[f'{task_class}']:
            print(get_debug_info('NICE', 'Collect Success({})'.format(task_class)))
        else:
            print(get_debug_info('ERR', 'length of redis list has not changed'))
    except Exception as e:
        print(get_debug_info('ERR', f'({task_class}) spider engine panic', err_info=''.format(e)))
    finally:
        print(get_debug_info('OVER', 'the cache of ({}) task list({})'.format(task_class, rc_len[f'{task_class}'])))
        print('>> {} <<'.format(''.center(50, '=')))


if __name__ == '__main__':

    schedule.every(2).minutes.do(deploy_collection_engine, 'ssr')
    schedule.every(1).minute.do(deploy_collection_engine, 'v2ray')
    # schedule.every(100).minute.do(deploy_collection_engine, 'trojan')
    try:
        ret = threading.Thread(target=rc.refresh, args=(True,))
        ret.setDaemon(True)
        ret.start()

        deploy_collection_engine('ssr')
        deploy_collection_engine('v2ray')
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as err:
        print(get_debug_info('ERR', 'deploy panic', err_info=''.format(err)))
        v2rayc_email.prepare(err='{}'.format(err), func_name='/funcBase/deploy_engine/schedule.run/')
    except KeyboardInterrupt:
        print(get_debug_info('-OVER-', 'End of collection'))
