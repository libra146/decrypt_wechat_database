import os
import time
from os.path import splitext
from shutil import copyfile, rmtree


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
            os.system(f'rm {splitext(a)[0]}_process.bak')


def unpack(filename):
    os.system(f'java -jar abe-all.jar unpack {filename} {splitext(filename)[0]}_unpack.tar')
    if os.path.exists(f'{splitext(filename)[0]}_unpack.tar'):
        os.system(f'tar -xf {splitext(filename)[0]}_unpack.tar')
        os.system(f'rm {splitext(filename)[0]}_unpack.tar')


def list_dir():
    for path, dirs, files in os.walk('./apps'):
        for a in files:
            if a == 'EnMicroMsg.db':
                copyfile(f'{path}/{a}', f'{int(time.time() * 1000)}-EnMicroMsg.db')
                rmtree('./apps')


if __name__ == '__main__':
    os.system('cp ./data/*.bak ./')
    process()
    list_dir()
    # 解密数据库
    if os.system('./decrypt') != 0:
        # 解密失败删掉生成的空文件，复制出未解密的文件
        print('decrypt failed!')
        os.system('rm decrypt-*')
        os.system('cp *.db ./data')
        os.system('rm *.bak')
    else:
        os.system('cp decrypt-* ./data')
        os.system('rm *.db')
        os.system('rm *.bak')
        print('success!')
