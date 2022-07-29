import sm3

#初始向量
iv = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
      0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]


#求Hash(m1||padding||m2)，记为H2
def sm3_hash(mes,mes_add):
    mes_pad = sm3.padding_func(mes)+sm3.padding_func(mes_add)
    rounds = len(mes_pad) // 64
    v = iv
    for i in range(rounds):
        v = sm3.cf_func(v, mes_pad[64 * i:64 * (i + 1)])
    result = ''
    for num in v:
        result += '{:08x}'.format(num)
    return result

#已知Hash(m1),记为H1,利用长度扩展攻击，以H1为初始向量，求Hash(m2),记为H3
def sm3_length_attack(mes,mes_add):
    v,hash_1=sm3.sm3_hash(mes)
    mes_pad=sm3.padding_func(mes_add)
    rounds = len(mes_pad) // 64
    for i in range(rounds):
        v = sm3.cf_func(v, mes_pad[64 * i:64 * (i + 1)])
    hash_2 = ''
    for num in v:
        hash_2 += '{:08x}'.format(num)
    return hash_2

#对比H2和H3，若二者相等，则成功构造出对消息m1||padding||m2的伪造散列值H3
def compare(mes,mes_add):
    H2=sm3_hash(mes, mes_add)
    H3=sm3_length_attack(mes, mes_add)
    if H2==H3:
        print('成功伪造散列值:',H2)
    else:
        print('Fail !')

if __name__ == '__main__':
    #随机消息m1
    mes='my name is renhai'
    #我们希望添加的内容m2
    mes_add='I like cryptology'
    print('随机选取消息m1:',mes)
    print('需要添加在其后的内容:',mes_add)
    compare(mes, mes_add)

"""
在该项目中，随机选取的消息为'my name is renhai'，需要在其后添加的内容为'I like cryptology'，最终伪造出的散列为'5957b4e3394553c1839a70d64b0f15ec3bb39265b3ee7d78af4fd623e9664ae8'
"""
