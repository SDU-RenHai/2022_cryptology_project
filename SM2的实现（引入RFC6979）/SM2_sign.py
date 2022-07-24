import secrets
import sm3
import math
import libnum
import hashlib

#初始化参数
def init_():
    p=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',16)
    a=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',16)
    b=int('0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',16)
    n=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',16)
    gx=int('0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7',16)
    gy=int('0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0',16)
    param=[p,a,b,n]
    G=[gx,gy] #G
    ID_A = '0x31323334353637383132333435363738'
    z,dA,pA = Precompute(param,ID_A,G)
    return param,G,z,dA,pA,n

def padding(a,k):             #将a（十六进制）扩充到k字节的十六进制
    temp=a[2:]
    while len(temp)<(2*k):
        temp='0'+temp
    return '0x'+temp

def double_add(P,Q,param):   #计算P+Q
    x1 = P[0];y1 = P[1]
    x2 = Q[0];y2 = Q[1]
    if x1 == '0' and y1 == '0':        
        return [x2,y2]
    if x2 == '0' and y2 == '0':
        return [x1,y1]
    if x1 != x2:
        y = y2 - y1
        x = x2 - x1
        lam = y * libnum.invmod(x,param[0]) % param[0]
        x3=(lam ** 2 - x1 - x2) % param[0]
        y3=(lam * (x1-x3) - y1) % param[0]
    elif y2 != -1*y1:
        x = 3 * (x1 ** 2) + param[1]
        y = 2 * y1
        lam = x * libnum.invmod(y,param[0]) % param[0]
        x3=(lam ** 2 - x1 - x2) % param[0]
        y3=(lam * (x1-x3) - y1) % param[0]
    else:
        x3='0';y3='0'
    return [x3,y3]

def k_add(k,P,param):     #[k]P
    PK = ['0','0']
    k = list((bin(k))[2:])
    l = len(k)            #k有l比特
    k.reverse()
    for j in range(l-1,-1,-1):
        PK = double_add(PK,PK,param)
        if (k[j] == '1'):
            PK = double_add(PK,P,param)
    return PK

#根据RFC的简化版本，k = SHA256(d + HASH(mes))，利用该公式，计算k
def generate_k(mes,d):
    Hash_m = sm3.sm3_hash(mes)
    mes_new = hex(d) + Hash_m
    k_hex = hashlib.sha256((mes_new).encode('utf-8')).hexdigest()
    k = int(k_hex,16)
    return k

#预计算
def Precompute(param,ID_A,G):
    ENTL_A = padding(hex((len(ID_A)-2)*4),2)
    x_G=hex(G[0])
    y_G=hex(G[1])
    a=hex(param[1])
    b=hex(param[2])
    dA=secrets.randbelow(param[3])
    pA=k_add(dA,G,param)
    x_A = hex(pA[0])
    y_A = hex(pA[1])
    Z = (ENTL_A+ID_A+a+b+x_G+y_G+padding(x_A,32)+padding(y_A,32)).replace('0x','')
    Z_h = sm3.sm3_hash(Z)
    return (Z_h,dA,pA)

#计算签名
def sm2_sig(mes,param,z,G,dA):
    M=z+mes
    e=int(sm3.sm3_hash(M),16)
    p,n=param[0],param[3]
    r,s,k=0,0,0
    while (r==0 or r+k==n or s==0):
        #使用RFC6979生成随机数k
        k=generate_k(mes,dA)
        x_1=(k_add(k,G,param))[0]
        r=(e+x_1)%n
        s=(((libnum.invmod(1+dA,n))%n)*((k-r*dA)%n))%n
    return (mes,hex(r),hex(s))

#验证函数
def verify(mh,rh,sh,param,z,G,pA): #其中m,r,s,z都是十六进制数
    #首先把r,s都变成数
    r=int(rh,16)
    s=int(sh,16)
    if (1<=r<=(n-1)) and (1<=s<=(n-1)):
        mm=z+mh            #其中z是十六进制数
        e=int(sm3.sm3_hash(mm),16)    #其中mm,eh都是十六进制数
        t=(r+s)%n
        if t==0:
            return 0
        a=k_add(s,G,param)
        b=k_add(t,pA,param)
        x_1=double_add(a,b,param)[0]
        R=(e+x_1)%n;
    return (R == r)

if __name__ == '__main__':
    param,G,z,dA,pA,n = init_() #生成各项参数
    mes='my name is renhai'
    print("待签名的消息为:\n",mes)
    mes,r,s = sm2_sig(mes,param,z,G,dA)
    print('签名结果:')
    print('r:',r)
    print('s:',s)
    print('验证结果:\n',verify(mes,r,s,param,z,G,pA))
"""
---------------------------------测试案例-------------------------------
待签名的消息为:
 my name is renhai
签名结果:
r: 0x92603114bf31b2d4e47ea822d498dfb5cd32336fb7e913703ee388052e04b062
s: 0x95b3780a4a04f84b73c7a90df2c0c396b78405d62b0b694122a552c4a6494211
验证结果:
 True
 """
