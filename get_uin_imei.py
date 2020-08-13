import os

import javaobj

for path, dirs, files in os.walk('./apps'):
    print(files)
    if 'systemInfo.cfg' in files:
        with open(f'{path}/systemInfo.cfg', "rb") as fd:
            pobj = javaobj.loads(fd.read())
            print(pobj[1])
        break
"""
auth_info_key_prefs.xml _auth_uin
system_config_prefs.xml default_uin
app_brand_global_sp.xml uin_set
"""
