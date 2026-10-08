import hashlib


##dir(hashlib) — HAMMASINI KO‘RISH
# print(dir(hashlib))

##algorithms_available — Hozirgi tizimdagi hamma hash
# print(hashlib.algorithms_available)

data='iloveyou'.encode()
obj_md5=hashlib.md5(data).hexdigest()
obj_sha1=hashlib.sha1(data).hexdigest()
obj_sha256=hashlib.sha256(data).hexdigest()
print(data)
print(f"md5 | {obj_md5}	\nsha1 | {obj_sha1}\nsha256 | {obj_sha256}\n")
