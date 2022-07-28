import sm3
import numpy as np
import libnum
import sympy

#定义参数
p=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',16)
a=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',16)
b=int('0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',16)
n=int('0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',16)
gx=int('0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7',16)
gy=int('0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0',16)
param=[p,a,b,n]
G=[gx,gy] #G

#计算P+Q
def double_add(P,Q,param):   
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
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

#对集合的哈希函数
def Muli_hash(set):  
    digest = ['0', '0']
    for item in set:
        x = int(sm3.sm3_hash(item), 16)
        tmp = np.mod(x ** 2 + a * x + b, p)
        y = sympy.ntheory.residue_ntheory.nthroot_mod(tmp,2,p) #调库计算二次剩余
        point = [x, y]
        digest = double_add(digest, point, param)
    return digest

if __name__ == '__main__':
    #设置集合
    set_a = ('1234567',)
    set_b = ('12345678',)
    set_aa = ('1234567', '1234567')
    set_ab = ('1234567', '12345678')
    set_ba = ('12345678', '1234567')

    #输出结果
    print('hash({1234567}) = ', Muli_hash(set_a),'\n')
    print('hash({12345678}) = ',Muli_hash(set_b),'\n')
    print("hash({1234567, 1234567}) = ", Muli_hash(set_aa),'\n')
    print("hash({1234567, 12345678}) = ", Muli_hash(set_ab),'\n')
    print("hash({12345678, 1234567}) = ", Muli_hash(set_ba),'\n')

"""
-----------------------------测试案例-------------------------
hash({1234567}) =  [48433913378542022636752053339868314152176581172968616380919546742918156961638, 32876399180566714638268757066496654841935220359444882423025999955950230293276]

hash({12345678}) =  [7237002178003687078550813067441783752181808363899879879347813690909161405196, 27598121479278026692308762578309930654940877522510428305506074448347293773968]

hash({1234567, 1234567}) =  [35747999416672728358810222888487473478876873744517315377646377146952879228025, 78742774518417094420951797539913818050786969161220079754820298132594191516063]

hash({1234567, 12345678}) =  [103256127117898886084507589885469957040044095057492590062958768759477037010842, 14792783818712164892493337729155119707157814680055920602630860653521973606593]

hash({12345678, 1234567}) =  [103256127117898886084507589885469957040044095057492590062958768759477037010842, 14792783818712164892493337729155119707157814680055920602630860653521973606593]
"""

