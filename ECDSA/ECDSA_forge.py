import random
import string
import hashlib
import binascii
import libnum
from ecdsa import SigningKey, NIST256p,numbertheory, ellipticcurve, VerifyingKey

#初始化，调库生成ECDSA签名方案的各项参数
def init_():
    sk = SigningKey.generate(curve=NIST256p) #生成私钥d
    vk = sk.verifying_key  # 生成P的横纵坐标级联
    d = int(sk.to_string().hex(), 16) #d
    P = int(vk.to_string().hex(), 16) #P
    n = sk.curve.order #模数
    K = random.randint(1, n)
    mes = b'Satoshi' #待签名的消息
    sign = sk.sign(mes, k=K, hashfunc=hashlib.sha256) #获取签名值
    r = sign.hex()[:64]  #r
    s = sign.hex()[64:]  #s
    s = int(s, 16)
    r = int(r, 16)
    e = hashlib.sha256()
    e.update(mes)
    e = int(e.hexdigest(), 16)
    return sk,vk,d,P,n,K,mes,sign,r,s,e

#若验签时不需要mes，则可对任意消息进行签名伪造
def loss_mes_forge(n,sk):
    u = random.randint(1, n)
    v = random.randint(1, n)
    G = sk.curve.generator
    d = int(sk.to_string().hex(), 16)
    P = G * d
    r1 = (u * G + P * v).x()
    s1 = r1 * libnum.invmod(v, n)
    e1 = r1 * u * libnum.invmod(v, n) % n
    w = libnum.invmod(s1, n) % n
    eg = (e1 * w * G + r1 * w * P)
    if eg.x() == r1:
        print('新签名通过验证，伪造成功！','\n')
        return u,v,r1,s1,e1

if __name__ == '__main__':
    sk,vk,d,P,n,K,mes,sign,r,s,e = init_()
    print('假设Satoshi使用的公钥为:',hex(P),'\n')
    u,v,r1,s1,e1 = loss_mes_forge(n, sk)
    print('伪造中选取的u:',hex(u),'\n')
    print('伪造中选取的v:',hex(v),'\n')
    print("构造的e':",hex(e1),'\n')
    print("最终伪造的签名(r',s'):",(hex(r1),hex(s1)))


"""
--------------------------测试案例----------------------------
假设Satoshi使用的公钥为: 0x8659a0df2624168542ee78893a3afe6179d3289f1457cdc01859af15d9741bb27005eddb4f02b81db5fe8caf48fbfc47e53a7751e988da9f4836e916222c6073

新签名通过验证，伪造成功！

伪造中选取的u: 0xa6d7571fe62f045a5458555e5995d668ffe475884b3fc503470f9f5d5a209b8

伪造中选取的v: 0x1f6efce933f223eeaa279775367e07acc1ec7b6e7d31f9daf7395bb10206498c

构造的e': 0xb58eb4cfda7288afb29c3d7cf5ed07d024ac193f858d48ea45af96fe77c65bbb

最终伪造的签名(r',s'): ('0x834cd2b3dbbf7e201cc80afaa43e10b0ebcbec27f3795048b2a0bb697de9866', '0x61fd101a4831d145d12f920fe0980a3736d6b0c773aba02ef9f0f127c5963c29548350a913a8cec0d942b5cb80be69634166f7c6e32c6decfd63284b0a0c7e2')

"""

