# V2Ray云彩姬

科学上网，从娃娃抓起！

## :carousel_horse: Intro

- 运行`V2Ray云采姬.exe` 或压缩文件中的`main.exe`本即可启动**通用版本云彩姬**获取订阅连接

## :eagle: Quick Start

- 【win10软件+源代码】下载项目并解压（约42.9 MB）

  ![1](https://i.loli.net/2020/10/06/1OPUtIfZSi3wq5R.png)

- **运行脚本**||**开箱即用**（直接下载软件；约17MB）

  - [云彩姬使用说明](https://github.com/QIN2DIM/V2RayCloudSpider/blob/master/V2Ray云彩姬使用说明.md)![2](https://i.loli.net/2020/10/06/gKIZAPLd9JY8HQz.png)



## :video_game: Advanced Gameplay

> 该脚本未在macOS测试运行，可能存在非常多的bug，欢迎感兴趣的小伙伴来跑一下程序- -

- `/V2RaySpider0925`中存放该项目通用版本的源代码
- 运行`main.py`启动程序

```
# V2RaycSpider0925
 ├── dataBase
 │   ├── AirportURL.csv
 │   ├── fake_useragent_0.1.11.json
 │   ├── log_information.csv
 │   ├── log_VMess.txt
 │   ├── ssr机场.txt
 │   └── v2ray机场.txt
 ├── funcBase
 │   ├── func_avi_num.py
 │   ├── get_ssr_link.py
 │   ├── get_v2ray_link.py
 │   └── __init__.py
 ├── MiddleKey
 │   ├── chromedriver
 │   ├── chromedriver.exe
 │   ├── VMes_IO.py
 │   └── __init__.py
 ├── Panel
 │   ├── master_panel.py
 │   └── __init__.py
 ├── spiderNest
 │   ├── IA_spider.py
 │   ├── preIntro.py
 │   ├── SNIF_dog.py
 │   ├── SSRcS_xjcloud.py
 │   ├── STAFF sAirport.txt
 │   ├── V2Ray_vms.py
 │   └── __init__.py
 ├── main.py
 ├── requirements.txt
 ├── config.py
 ├── 1.ico
 └── V2Ray云彩姬使用说明.md
```

### :balance_scale: Configure project parameters

- 请在此正确填写你的服务器信息，并将整个项目文件`V2RaycSpider0925`上传至linux服务器的`/qinse`文件夹下，没有就新建一个 - -

```python
# file_name = '/V2RaycSpider0925/config.py'
# SYS_PATH = f'/qinse/V2RaycSpider{verNum}'

# ---------------------------------------------------
# Cloud server configuration(SSH)
# ---------------------------------------------------
ECS_HOSTNAME: str = 'your ip'
ECS_PORT: int = 29710
ECS_USERNAME: str = 'root'
ECS_PASSWORD: str = 'KYU77wh7vpRK'
```

- 若`ECS_HOSTNAME`参数为空(默认为空)，则会启动**本地采集程序**，`local version`会丧失部分功能权限；其他参数大可不必改动- -

- 设置驱动执行权限

  给`chromedriver`设置可执行权限，如果用`Finalshell`l或`Xshell`的同学，直接右键目标文件即可设置文件权限；项目预装的驱动是最新版本的[2020.10]所以linux中要下载`v85.0.4183.102`或更新版本的Chrome

  ```python
  CHROMEDRIVER_PATH = os.path.dirname(__file__) + '/MiddleKey/chromedriver'
  ```

### :zap:Other

## :grey_question: Q&A

- **防火墙警告**

  - 首次运行可能会弹出提示

    ![3](https://i.loli.net/2020/10/06/MhwiZfOz3VdDPU5.png)

    ![3](https://i.loli.net/2020/10/06/gmLksO3HCtyWu9r.png)

## :world_map: TODO

- [ ] 支持Trojan-go、Trojan-gfw机场的采集
- [ ] 融合网络代理核心，形成自洽的科学上网模块
- [ ] 添加{邮件发送模块}，支持开发者账号群发订阅链接
- [ ] 合并V2ray和SSR的订阅链接消息队列，PC端可查看最新可用的3条链接，并择一获取
  - [x] 合并队列
  - [x] 查看链接
  - [ ] 择一获取
- [ ] 逐渐停用easyGUI前端模块，移植web操作平台，兼容跨平台访问(手机，电脑，嵌入式系统)