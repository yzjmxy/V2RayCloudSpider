import sys

sys.path.append('/qinse/V2RaycSpider0925')
import redis
from config import REDIS_PORT, REDIS_HOST, REDIS_PASSWORD, REDIS_DB, REDIS_KEY_NAME_BASE

REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2.')


class RedisClient(object):
    """redis connection client of v2rayc_spider"""

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, **kwargs):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True, db=db, **kwargs, )
        self.__prepare__()

    def get(self, key_name, retry=0):
        attention_link = self.db.rpop(key_name)
        if attention_link:
            return attention_link
        else:
            if retry >= 3:
                return None
            retry += 1
            self.get(key_name, retry)

    def add(self, key_name, value_of_link_attr, link_life_cycle=0):
        self.db.lpush(key_name, value_of_link_attr)

    def __prepare__(self, ):
        """初始化环境，当前版本默认弃用，未来将用于分布式锁设计"""

        for x in ['ssr', 'v2ray', 'trojan']:
            if self.db.llen(REDIS_KEY_NAME_BASE.format(x)) == 0:
                self.db.lpush(REDIS_KEY_NAME_BASE.format(x), '')

    def test(self):
        return self.db.ping()

    def kill(self):
        self.db.close()



if __name__ == '__main__':
    RedisClient().test()