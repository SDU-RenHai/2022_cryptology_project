import sm3
import math
import libnum
import hashlib
import random
import binascii

#初始化参数
p=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',16)
a=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',16)
b=int('0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',16)
n_0='0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123'
n=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',16)
g='32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7''bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0'


#引入RFC6979，利用公式k = SHA256(d + HASH(mes))生成随机数k
def generate_k(mes,sk):
    Hash_m = sm3.sm3_hash(mes)
    mes_new = sk + Hash_m
    k_hex = hashlib.sha256((mes_new).encode('utf-8')).hexdigest()
    return k_hex

#Key derivation function,z为16进制表示的比特串，klen为密钥长度
def sm3_kdf(z, klen):
    ct = 0x00000001
    rounds = math.ceil(klen/32)
    Ha = ""
    for i in range(rounds):
        mes = binascii.a2b_hex(('%08x' % ct).encode('utf8')) + z
        Ha = Ha + sm3.sm3_hash(mes)
        ct += 1
    result = Ha[0: klen * 2]
    return result

#计算倍点
def double_p( p_t): 
    l = len(p_t)
    len_0 = 2 * (len(n_0)-2)
    if l < (len(n_0)-2) * 2:
        return None
    else:
        x1 = int(p_t[0:(len(n_0)-2)], 16) # x1
        y1 = int(p_t[(len(n_0)-2):len_0], 16) #y1
        if l == len_0:
            z1 = 1
        else:
            z1 = int(p_t[len_0:], 16)
        T6 = (z1 * z1) % p
        T_2 = (y1 * y1) % p
        T_3 = (x1 + T6) % p
        T_4 = (x1 - T6) % p
        T_1 = (T_3 * T_4) % p
        T_3 = (y1 * z1) % p
        T_4 = (T_2 * 8) % p
        T_5 = (x1 * T_4) % p
        T_1 = (T_1 * 3) % p
        T6 = (T6 * T6) % p
        T6 = (((a+3) % p) * T6) % p
        T_1 = (T_1 + T6) % p
        Z_3 = (T_3 + T_3) % p
        T_3 = (T_1 * T_1) % p
        T_2 = (T_2 * T_4) % p
        X_3 = (T_3 - T_5) % p
        if (T_5 % 2) == 1:
            T_4 = (T_5 + ((T_5 + p) >> 1) - T_3) % p
        else:
            T_4 = (T_5 + (T_5 >> 1) - T_3) % p
        T_1 = (T_1 * T_4) % p
        Y_3 = (T_1 - T_2) % p
        form = ('%%0%dx' % (len(n_0)-2))*3
        result = form % (X_3, Y_3, Z_3)
        return result

#计算点加，P1为Jacobian加重射影坐标，P2点为仿射坐标
def add_point( P_1, P_2):  
    len_0 = 2 * (len(n_0)-2)
    len_1 = len(P_1)
    len_2 = len(P_2)
    if (len_1 < len_0) or (len_2 < len_0):
        return None
    else:
        X_1 = int(P_1[0:(len(n_0)-2)], 16)
        Y_1 = int(P_1[(len(n_0)-2):len_0], 16)
        if (len_1 == len_0):
            Z_1 = 1
        else:
            Z_1 = int(P_1[len_0:], 16)
        X_2 = int(P_2[0:(len(n_0)-2)], 16)
        Y_2 = int(P_2[(len(n_0)-2):len_0], 16)
        T_1 = (Z_1 * Z_1) % p
        T_2 = (Y_2 * Z_1) % p
        T_3 = (X_2 * T_1) % p
        T_1 = (T_1 * T_2) % p
        T_2 = (T_3 - X_1) % p
        T_3 = (T_3 + X_1) % p
        T_4 = (T_2 * T_2) % p
        T_1 = (T_1 - Y_1) % p
        Z_3 = (Z_1 * T_2) % p
        T_2 = (T_2 * T_4) % p
        T_3 = (T_3 * T_4) % p
        T_5 = (T_1 * T_1) % p
        T_4 = (X_1 * T_4) % p
        X_3 = (T_5 - T_3) % p
        T_2 = (Y_1 * T_2) % p
        T_3 = (T_4 - X_3) % p
        T_1 = (T_1 * T_3) % p
        Y_3 = (T_1 - T_2) % p
        form = ('%%0%dx' % (len(n_0)-2))*3
        result = form % (X_3, Y_3, Z_3)
        return result

# 转换函数，将Jacobian加重射影坐标转换成仿射坐标
def jacb_to_nor( p_t):  
        len_0 = 2 * (len(n_0)-2)
        x = int(p_t[0:(len(n_0)-2)], 16)
        y = int(p_t[(len(n_0)-2):len_0], 16)
        z = int(p_t[len_0:], 16)
        z_inv = pow(z,p - 2,p)
        z_invS = (z_inv * z_inv) %p
        z_invQ = (z_invS * z_inv) %p
        x_new = (x * z_invS) %p
        y_new = (y * z_invQ) %p
        z_new = (z * z_inv) %p
        if z_new == 1:
            form =( '%%0%dx' % (len(n_0)-2))*2
            result = form % (x_new, y_new)
            return result
        else:
            return None

# kP运算
def k_p(k, p_t): 
    p_t = '%s%s' % (p_t, '1')
    fill_str = '8'
    for i in range(len(n_0) - 3):
        fill_str += '0'
    mask = int(fill_str, 16)
    temp = p_t
    flag = False
    for n in range((len(n_0)-2) * 4):
        if (flag):
            temp = double_p(temp)
        if (k & mask) != 0:
            if (flag):
                temp = add_point(temp, p_t)
            else:
                flag = True
                temp = p_t
        k = k << 1
    result = jacb_to_nor(temp)
    return result

# 加密函数,msg为明文
def Encrypt( msg,sk,pk):
        msg = bytes(msg,'UTF-8').hex()  
        k = generate_k(msg, sk)
        C1 = k_p(int(sk, 16),g)
        xy = k_p(int(sk, 16), pk)
        X_2 = xy[0:(len(n_0)-2)]
        Y_2 = xy[(len(n_0)-2):2*(len(n_0)-2)]
        len_msg = len(msg)
        t = sm3_kdf(xy.encode('utf8'),int( len_msg/2))
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % len_msg
            C2 = form % (int(msg, 16) ^ int(t, 16))
            C3 = sm3.sm3_hash(bytes.fromhex('%s%s%s' % (X_2, msg, Y_2)))
            result = ('%s%s%s' % (C1, C3, C2))
            return result

# 解密函数，此处msg为密文
def decrypt(msg,sk):
    msg = (bytes.fromhex(msg)).hex()
    len_0 = 2 * (len(n_0)-2)
    len_3 = len_0 + 64
    C1 = msg[0:len_0]
    C3 = msg[len_0:len_3]
    C2 = msg[len_3:]
    xy = k_p(int(sk, 16), C1)
    X_2 = xy[0:(len(n_0)-2)]
    Y_2 = xy[(len(n_0)-2):len_0]
    cl = len(C2)
    t = sm3_kdf(xy.encode('utf8'), int(cl/2))
    if int(t, 16) == 0:
        return None
    else:
        form = '%%0%dx' % cl
        M = form % (int(C2, 16) ^ int(t, 16))
        u = sm3.sm3_hash(bytes.fromhex('%s%s%s' % (X_2, M, Y_2)))
        result = bytes.fromhex(M).decode()
        return result

if __name__ == '__main__':
    #设置密钥sk,pk，此处所用公私钥对为在线工具生成，网站地址为:https://const.net.cn/tool/sm2/genkey/
    sk = '92EBE8E51821914F5AD6C9A48FB6E9987E61F4AEE9B97997E0593431C76DC8C7'
    pk = '95C8B3C6019B841C605D46AF1B83A24D9103CF14C7DD0D8A142000D3F243B23FD1582697112E98D9182C3DE8FBA268E488A3405CDD7006645F48C2D2B4BE4B54'
    #待加密的消息msg
    msg = 'my name is renhai'
    print('待加密的消息为：',msg)
    enc_data = Encrypt(msg,sk,pk)
    print('加密后的密文：',enc_data)
    dec_data = decrypt(enc_data,sk)
    print('密文解密后的明文:',dec_data)

"""
---------------------------------------------运行案例-------------------------------------------
待加密的消息为： my name is renhai
加密后的密文： 95c8b3c6019b841c605d46af1b83a24d9103cf14c7dd0d8a142000d3f243b23fd1582697112e98d9182c3de8fba268e488a3405cdd7006645f48c2d2b4be4b547d2e1f45bce5ea63f11ad27d9bdc83b361eba1f8b20c820acc7b351e0473ab6c1f7254cbc5ac9f2b16a63fee8d7db3457d
密文解密后的明文: my name is renhai
"""