##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020-10-19 09:31:00
# @Author  : Libra
# @Email   : 146232616@qq.com
# @File    : process.py

import os
import time
from hashlib import md5
from os.path import splitext
from shutil import copyfile, rmtree

import javaobj
from lxml import etree


def process():
    for a in os.listdir('.'):
        if splitext(a)[1] == '.bak':
            with open(a, 'rb') as f:
                # 如果头部为MIUI的话需要处理
                if f.read(4) == b'MIUI':
                    with open(f'{splitext(a)[0]}_process.bak', 'wb') as ff:
                        f.seek(41)
                        while True:
                            data = f.read(40960)
                            if not data:
                                break
                            ff.write(data)
            unpack(f'{splitext(a)[0]}_process.bak')
            if delete:
                os.system(f'rm {splitext(a)[0]}_process.bak')


def unpack(filename):
    os.system(f'java -jar abe-all.jar unpack {filename} {splitext(filename)[0]}_unpack.tar')
    if os.path.exists(f'{splitext(filename)[0]}_unpack.tar'):
        os.system(f'tar -xf {splitext(filename)[0]}_unpack.tar')
        if delete:
            os.system(f'rm {splitext(filename)[0]}_unpack.tar')


def compute_password(uin, imei):
    result = []
    # 如果找不到IMEI，使用默认值
    if not imei:
        imei.append('1234567890ABCDEF')
    if not uin:
        return result
    for a in uin:
        for b in imei:
            m = md5()
            m.update(b.encode() + a.encode())
            result.append(m.hexdigest()[:7])
    return result


def list_dir():
    _uin = []
    _imei = []
    for path, dirs, files in os.walk('./apps'):
        for a in files:
            if a == 'EnMicroMsg.db':
                copyfile(f'{path}/{a}', f'{int(time.time() * 1000)}-EnMicroMsg.db')
        if 'systemInfo.cfg' in files:
            with open(f'{path}/systemInfo.cfg', "rb") as fd:
                obj = javaobj.loads(fd.read())
                _uin.append(str(obj[1]))
        if 'auth_info_key_prefs.xml' in files:
            with open(f'{path}/auth_info_key_prefs.xml', "rb") as fd:
                result = etree.XML(fd.read())
                for a in result.getchildren():
                    if a.get('name') == '_auth_uin':
                        _uin.append(a.get('value'))
        if 'app_brand_global_sp.xml' in files:
            with open(f'{path}/app_brand_global_sp.xml', "rb") as fd:
                result = etree.XML(fd.read())
                for a in result.getchildren():
                    _uin.append(a.getchildren()[0].text if a.getchildren() else '')
        if 'system_config_prefs.xml' in files:
            with open(f'{path}/system_config_prefs.xml', "rb") as fd:
                result = etree.XML(fd.read())
                for a in result.getchildren():
                    if a.get('name') == 'default_uin':
                        _uin.append(a.get('value'))
        if 'DENGTA_META.xml' in files:
            with open(f'{path}/DENGTA_META.xml', "rb") as fd:
                result = etree.XML(fd.read())
                for a in result.getchildren():
                    if a.get('name') == 'IMEI_DENGTA':
                        _imei.append(a.text)
    if delete:
        rmtree('./apps')
    return list(set(compute_password(_uin, _imei)))


if __name__ == '__main__':
    delete = os.getenv('deleted') or '1'
    delete = int(delete)
    os.system('cp ./data/*.bak ./')
    process()
    password = list_dir()
    # 解密数据库
    if os.system(f'./decrypt {" ".join(password)}') != 0:
        # 解密失败删掉生成的空文件，复制出未解密的文件
        print('decrypt failed!')
        os.system('rm decrypt-*')
        os.system('cp *.db ./data')
        if delete:
            os.system('rm *.bak')
    else:
        os.system('cp decrypt-* ./data')
        if delete:
            os.system('rm *.db')
            os.system('rm *.bak')
        print('success!')
