from hashlib import md5

import javaobj

aaa = ['1234567890ABCDEF']
bbb = ['-111111111']
c = []
for a in aaa:
    for b in bbb:
        result = md5()
        result.update(a.encode() + b.encode())
        c.append(result.hexdigest())

print(set(c))

with open("D:\\360download\\apps\\com.tencent.mm\\r\\MicroMsg\\systemInfo.cfg", "rb") as fd:
    jobj = fd.read()

pobj = javaobj.loads(jobj)
print(pobj[1])

"""
auth_info_key_prefs.xml _auth_uin
system_config_prefs.xml default_uin
app_brand_global_sp.xml uin_set
"""
