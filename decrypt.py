import os
import sys
from hashlib import md5

from pysqlcipher import dbapi2 as sqlite


def decrypt(key):
    if not key:
        print('evn key is empty!!!')
    uin = sys.argv[1] if len(sys.argv) >= 2 else ''
    if uin:
        print('uin is {}!'.format(uin))
        m = md5()
        m.update('1234567890ABCDEF'.encode() + uin.encode())
        key = m.hexdigest()[:7]
    if not uin:
        print('uin is empty!')
        sys.exit(-1)
    print('password is {}!'.format(key))
    for name in os.listdir('.'):
        if os.path.splitext(name)[1] == '.db':
            conn = sqlite.connect(name)
            c = conn.cursor()
            try:
                c.execute("PRAGMA key = '{}';".format(key))
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
            except Exception as e:
                print(repr(e))
                print('An error occurred!!!')
                print('The possible reason is the wrong password?')
                sys.exit(-1)
            finally:
                c.close()


if __name__ == '__main__':
    decrypt(os.getenv('password'))
