# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
import time
this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
long_description="""

这里是说明
用于自动标记文本内容
使用albert

自动标记文本
自动会下载模型

可自己训练


~~~
# 安装
pip install tkitMarker  -i https://pypi.org/simple




from tkitMarker import *
content="柯基犬性格活泼可爱，但是饲养柯基犬会有着六个坏处，你还敢饲养柯基犬吗？"
P=Pre()
result=P.pre([content])
print(result)










"""
setup(
    name='tkitMarker',
    version='0.0.1.9.9',
    description='Terry Auto Marker',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    url='https://github.com/napoler/AlBert-BiLSTM-CRF-pytorch',
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'transformers==2.3.0',
        'torch==1.3.1',
        'ipdb==0.12.2',
        # 'requests==2.22.0',
        'tkitFile==0.0.1.2',
        'tkitWeb==0.0.1.0',
        'fire==0.2.1'

    ],
    # package_dir=[],
    packages=['tkitMarker','tkitMarker/model'])
    # install_requires=[
    #     # asn1crypto==0.24.0
    #     # beautifulsoup4==4.7.1
    #     # bs4==0.0.1
    #     # certifi==2019.3.9
    #     # chardet==3.0.4
    #     # cryptography==2.1.4
    #     # cycler==0.10.0
    #     # docopt==0.6.2
    #     # idna==2.6
    #     # jieba==0.39
    #     # keyring==10.6.0
    #     # keyrings.alt==3.0
    #     # kiwisolver==1.0.1
    #     # matplotlib==3.0.3
    #     # numpy==1.16.2
    #     # pandas==0.24.2
    #     # pipreqs==0.4.9
    #     # PyAudio==0.2.11
    #     # pycrypto==2.6.1
    #     # pygobject==3.26.1
    #     # pyparsing==2.4.0
    #     # python-dateutil==2.8.0
    #     # pytz==2019.1
    #     # pyxdg==0.25
    #     # requests==2.21.0
    #     # scipy==1.2.1
    #     # SecretStorage==2.3.1
    #     # six==1.11.0
    #     # soupsieve==1.9.1
    #     # urllib3==1.24.1
    #     # yarg==0.1.9

    # ],

    #install_requires=['jieba'])
"""
pip freeze > requirements.txt
python3 setup.py sdist
#python3 setup.py install
python3 setup.py sdist upload
"""