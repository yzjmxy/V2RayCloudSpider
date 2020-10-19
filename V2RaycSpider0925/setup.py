import webbrowser
import easygui
from setuptools import setup

TITLE_DOWNLOAD = 'V2Ray云彩姬下载器'
while True:
    try:
        usr_c = easygui.enterbox('欢迎使用v2ray云彩姬\nWindows用户请输入”v2raycs“下载最新版软件', title=TITLE_DOWNLOAD)
        if usr_c == 'v2raycs':
            webbrowser.open('https://t.qinse.top/subscribe/v2ray云彩姬.zip')
            break
        elif usr_c is None:
            break
        else:
            usr_c = easygui.ynbox('输入有误，返回重试或退出', title=TITLE_DOWNLOAD, choices=['返回', '退出'])
            if not usr_c:
                break
    except TypeError:
        break


try:
    setup(
        name='V2RaycSpider0925',
        version='4.4.0',
        packages=['Panel', 'funcBase', 'MiddleKey', 'spiderNest', 'spiderNest.action_slaver'],
        url='https://github.com/QIN2DIM/V2RayCloudSpider',
        license='https://github.com/QIN2DIM/V2RayCloudSpider/blob/master/LICENSE',
        author='QIN2DIM',
        author_email='qinse.top@foxmail.com',
        description='Get online scientifically, start from the baby!'
    )
except Exception:
    pass
