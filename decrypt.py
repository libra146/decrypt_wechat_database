##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020-10-19 09:31:00
# @Author  : Libra
# @Email   : 146232616@qq.com
# @File    : decrypt.py

import os
import sys

from pysqlcipher import dbapi2 as sqlite


def decrypt(evn_key):
    compute_key = sys.argv[1:] if len(sys.argv) >= 2 else []
    if not compute_key and not evn_key:
        print('no password found!!!')
        sys.exit(-1)
    if not evn_key:
        print('evn_key is empty!!!')
    if not compute_key:
        print('compute_key is empty!')
    if evn_key:
        compute_key.append(evn_key)
    print('password is {}!'.format(compute_key))
    for name in os.listdir('.'):
        if os.path.splitext(name)[1] == '.db':
            for password in compute_key:
                conn = sqlite.connect(name)
                c = conn.cursor()
                try:
                    c.execute("PRAGMA key = '{}';".format(password))
                    c.execute("PRAGMA cipher_page_size = 1024;")
                    c.execute("PRAGMA kdf_iter = 4000;")
                    c.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1;")
                    c.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1;")
                    c.execute("PRAGMA cipher_use_hmac = OFF;")
                    c.execute("ATTACH DATABASE '{}' AS plaintext KEY '';".format('decrypt-' + name))
                    c.execute("SELECT sqlcipher_export('plaintext');")
                    c.execute("DETACH DATABASE plaintext;")
                    conn.commit()
                    c.close()
                    break
                except Exception as e:
                    print(repr(e))
                    print('An error occurred!!!')
                    print('The possible reason is the wrong password?')
                    sys.exit(-1)
                finally:
                    c.close()


if __name__ == '__main__':
    decrypt(os.getenv('password'))
