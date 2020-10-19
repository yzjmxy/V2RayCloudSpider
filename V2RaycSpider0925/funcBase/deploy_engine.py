import sys

sys.path.append('/qinse/V2RaycSpider0925')
import time
from datetime import datetime
import schedule
import logging

from concurrent.futures import ThreadPoolExecutor
from funcBase import v2rayc_email
from MiddleKey.redis_IO import RedisClient
from config import REDIS_KEY_NAME_BASE, TIME_ZONE_CN, SYS_LOG_PATH
from spiderNest.preIntro import magic_msg
from spiderNest.action_slaver import thessr, ufocloud, xjcloud, jisumax

logging.basicConfig(
    filename=SYS_LOG_PATH,
    filemode='a',
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%d-%M-%Y %H:%M:%S",
    level=logging.DEBUG
)


def get_debug_info(tag_info, diy_info, err_info=''):
    debug_msg = '>> [{}] {} || {} << {}'.format(tag_info, str(datetime.now(TIME_ZONE_CN)).split('.')[0], diy_info,
                                                err_info)
    if 'NICE' in tag_info.upper():
        logging.info(debug_msg)
        return magic_msg(debug_msg, 'g')
    elif 'ERR' in tag_info.upper():
        logging.error(debug_msg)
        return magic_msg(debug_msg, 'r')
    elif 'RUN' in tag_info.upper():
        return magic_msg(debug_msg, 'c')
    elif tag_info == '-OVER-':
        return magic_msg(debug_msg, 'm')
    elif 'WARN' in tag_info.upper():
        return magic_msg(debug_msg, 'y')
    else:
        return debug_msg


rc = RedisClient()
rc_len = {
    'ssr': 1,
    'v2ray': 1,
    'trojan': 1,
}


def do_spider_cluster(deployment_environment: str, task_name: str):
    if isinstance(task_name, str):
        if 'linux' in deployment_environment:
            if task_name == 'ssr':
                xjcloud.Action_XjCloud().run()
            elif task_name == 'v2ray':
                thessr.Action_TheSSR().run()
                ufocloud.Action_UfoCloud().run()
            elif task_name == 'trojan':
                jisumax.Action_JiSuMax().run()
            else:
                logging.warning('the task name of cluster\'s task name is error({})'.format(task_name))
        else:
            jisumax.Action_JiSuMax().run()
            print(
                get_debug_info('WARNING',
                               'Please deploy in linux environment.Not in ({})'.format(deployment_environment)))
            logging.warning('Deploy the system in this environment({})'.format(deployment_environment))
            # exit()
    else:
        logging.warning('the task name of cluster\'s task name is error({})'.format(task_name))


def deploy_collection_engine(task_name: str, cap: int = 20):
    """
    :param task_name: v2ray,ssr,trojan
    :param cap:
    """
    global rc_len

    # Canonical input
    if not isinstance(task_name, str):
        print(get_debug_info('ERR', f'The input type is wrong({task_name})'))
        return None
    else:
        if task_name not in ['v2ray', 'ssr', 'trojan']:
            print(get_debug_info('ERR', f'Spelling error in input({task_name}),Please choose from [v2ray,ssr,trojan]'))
            return None
        task_name = task_name.lower()
        rc_len[f'{task_name}'] = rc.__len__(REDIS_KEY_NAME_BASE.format(f'{task_name}'))

    # test the cache of redis list
    try:
        print(get_debug_info('TEST', f'Test cache of the v2rayc-spider ({task_name}) redis task list'))
        if rc_len[f'{task_name}'] >= cap:
            print(get_debug_info(f'SLEEP', f'Cache is full ({cap})'))
            return None
    finally:
        print('>> {} <<'.format(''.center(50, '=')))

    # main collect process
    try:
        print(get_debug_info('RUN', f'({task_name}) spider engine'))
        do_spider_cluster(sys.platform, task_name)

        if rc.__len__(REDIS_KEY_NAME_BASE.format(f'{task_name}')) > rc_len[f'{task_name}']:
            print(get_debug_info('NICE', f'Collect Success({task_name})'))
        else:
            print(get_debug_info('ERR', f'Abnormal collection task({task_name})'))
    except Exception as e:
        logging.exception('Exception occurred')
        print(get_debug_info('ERR', f'({task_name}) spider engine panic', err_info=''.format(e)))
    finally:
        print(get_debug_info('OVER', 'the cache of ({}) task list({})'.format(task_name, rc_len[f'{task_name}'])))
        print('>> {} <<'.format(''.center(50, '=')))


class VSD(object):
    """Deprecated v4.3.X+ V2raycSpiderDeployment"""

    def __init__(self):
        pass

    @staticmethod
    def quick_start():
        schedule.every(2).minutes.do(deploy_collection_engine, 'ssr')
        schedule.every(1).minute.do(deploy_collection_engine, 'v2ray')
        # schedule.every(100).minute.do(deploy_collection_engine, 'trojan')

        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def long_run():
        pass

    @staticmethod
    def checker():
        pass


if __name__ == '__main__':

    try:
        schedule.every(3).minutes.do(deploy_collection_engine, 'ssr')
        schedule.every(1).minute.do(deploy_collection_engine, 'v2ray')
        schedule.every(5).minutes.do(deploy_collection_engine, 'trojan')
        schedule.every(12).hours.do(rc.refresh, True)

        ThreadPoolExecutor(max_workers=4).map(deploy_collection_engine, ['ssr', 'v2ray', 'trojan'])

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as err:
        logging.exception('Exception occurred ||{}'.format(err))
        print(get_debug_info('ERR', 'deploy panic', err_info=''.format(err)))
        v2rayc_email.prepare(err='{}'.format(err), func_name='/funcBase/deploy_engine/schedule.run')
    except KeyboardInterrupt as err:
        logging.exception('Forced stop ||{}'.format(err))
        print(get_debug_info('-OVER-', 'End of collection'))
