import os
import sys

# ---------------------------------------------------
# 云彩姬版本号,版本号必须与工程版本(文件名)号一致
# ---------------------------------------------------
verNum = '0925'
# ---------------------------------------------------
# PC(链接获取)进程锁死的冷却时间
# 进程锁死时长(min)，建议type：float∈(0,1]
# ---------------------------------------------------
BAND_BATCH = 0.25

"""********************************* Action set/PATH->Service ********************"""

# Chromedriver 路径,咱不支持MAC环境的云服务器
# Linux Google Chrome v85.0.4183.102
if 'win' in sys.platform:
    CHROMEDRIVER_PATH = os.path.dirname(__file__) + '/MiddleKey/chromedriver.exe'
elif 'linux' in sys.platform:
    CHROMEDRIVER_PATH = os.path.dirname(__file__) + '/MiddleKey/chromedriver'

# CHROMEDRIVER_PATH_for_LINUX = os.path.dirname(__file__) + '/MiddleKey/chromedriver'
# CHROMEDRIVER_PATH_for_WIN32 = os.path.dirname(__file__) + '/MiddleKey/chromedriver.exe'

# 项目驱动版本||被准驱动verNum：0925
SYS_PATH = f'/qinse/V2RaycSpider{verNum}'

# ROOT DATABASE
ROOT_DATABASE = os.path.join(os.path.dirname(__file__), 'dataBase')

# LOG_CSV文件路径
SERVER_LOG_PATH = ROOT_DATABASE + '/log_information.csv'
# ---------------------------------------------------
# Cloud server configuration(SSH)
# ---------------------------------------------------
ECS_HOSTNAME: str = '107.182.21.117'
ECS_PORT: int = 27203
ECS_USERNAME: str = 'root'
ECS_PASSWORD: str = 'gZ25eWNDK3Kb'

# 文件路径:查询可用订阅连接
CLOUD_PATH_BASE = '/qinse/V2RaycSpider{}/funcBase/{}.py'
CLOUD_PATH_AviLINK = CLOUD_PATH_BASE.format(verNum, 'func_avi_num')
# 文件路径:ssr链接抓取接口
CLOUD_PATH_SSR = CLOUD_PATH_BASE.format(verNum, 'get_ssr_link')
# 文件路径:v2ray链接抓取接口
CLOUD_PATH_V2RAY = CLOUD_PATH_BASE.format(verNum, 'get_v2ray_link')

# Nginx映射路径
NGINX_RES_PATH = '/usr/share/nginx/html'
NGINX_SSR_PATH = os.path.join(NGINX_RES_PATH, 'ssr.txt')
NGINX_V2RAY_PATH = os.path.join(NGINX_RES_PATH, 'v2ray.txt')

# ---------------------------------------------------
# Redis server configuration(SSH)
# ---------------------------------------------------
REDIS_DB: int = 0
REDIS_KEY_NAME_BASE: str = 'v2rayc_spider:{}'

REDIS_HOST: str = '107.182.21.117'
REDIS_PORT: int = 6379
REDIS_PASSWORD: str = '663836'
REDIS_DECODE_RESPONSES = True
"""********************************* Action set/PATH->Local ********************************"""
# TODO: 当前版本不提供安装导航，不支持diy安装目录，若想更改缓存路径(默认当前文件夹)，请改动源代码
# 工程目录
ROOT_PROJECT_PATH = os.path.dirname(__file__)
# 软件本地根目录
SYS_LOCAL_fPATH = os.path.join(ROOT_PROJECT_PATH, 'dataBase')
# 访问记录(系统核心文件，请勿删改)
SYS_LOCAL_vPATH = SYS_LOCAL_fPATH + '/log_VMess.txt'
SYS_AIRPORT_INFO_PATH = SYS_LOCAL_fPATH + '/log_information.csv'
# 采集模式，若服务器设置有误 则本机启动
START_MODE = 'local' if ECS_HOSTNAME == '' else 'cloud'

"""********************************* The core set ********************************"""

# 我就是云彩姬!
TITLE = f'V2Ray云彩姬_v{verNum}'
