"""
 SM3的Python实现,用于寻找碰撞、长度扩展攻击项目,SM3的优化在另一项目中以C++的形式展现
"""

#初始向量IV
iv = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
      0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]

#填充函数，参数mes可以是字符串或者字节，返回填充后的字节形式
def padding_func(mes):
    if isinstance(mes, str)==1:
        mes_bytes = mes.encode()
    else:
        mes_bytes = mes
    lenth = len(mes_bytes)
    mes_hex = mes_bytes.hex()
    if mes_hex != '':
         mes_bin = '{:0{}b}'.format(
        int(mes_hex, 16), lenth * 8)
    else:
        mes_bin  = ''
    key = (447 - lenth * 8) % 512
    pad_bin = mes_bin + '1' + '0' * key + '{:064b}'.format(lenth * 8)
    len_bin = len(pad_bin)
    pad_hex = '{:0{}X}'.format(int(pad_bin, 2), len_bin // 4)
    padded_mes = bytes.fromhex(pad_hex)
    return padded_mes

#循环左移，输入需要左移的字节数、次数，返回操作后的结果
def circulate_left(num, times):

    return ((num << times) | (num >> (32 - times))) & 0xffffffff

#ff函数 x y z j均为int类型,j表示轮数
def ff(x, y, z, j):
    if 0 <= j <= 15:
        return x ^ y ^ z
    elif 16 <= j <= 63:
        return (x & y) | (x & z) | (y & z)


#gg函数 x y z j均为int类型,j表示轮数
def gg(x, y, z, j):
    if 0 <= j <= 15:
        return x ^ y ^ z
    elif 16 <= j <= 63:
        return (x & y) | ((~x) & z)

#置换函数p_0
def p_0(x,):
    return x ^ circulate_left(x, 9) ^ circulate_left(x, 17)

#置换函数p_1
def p_1(x):
    return x ^ circulate_left(x, 15) ^ circulate_left(x, 23)

#消息扩展
def mes_extend(mes):
    m = []
    m_l = []
    for i in range(16):
        m.append(int(mes[4 * i:4 * (i + 1)].hex(), 16))
    for i in range(16, 68):
        m.append(p_1(m[i - 16] ^ m[i - 9] ^ circulate_left(m[i - 3], 15))
                 ^ circulate_left(m[i - 13], 7) ^ m[i - 6])
    for i in range(64):
        m_l.append(m[i] ^ m[i + 4])
    return m, m_l

#cf压缩函数,v是消息扩展后的结果，mes是未扩展但已填充的消息
def cf_func(v, mes):
    a, b, c, d, e, f, g, h = v #代表8个32位变量
    m, m_l = mes_extend(mes)
    for i in range(64):
        if 0 <= i <= 15:
            t_i=0x79cc4519
        else:
            t_i=0x7a879d8a
        s_1 = circulate_left(
            (circulate_left(a, 12) + e + circulate_left(t_i, i % 32)) & 0xffffffff, 7)
        s_2 = s_1 ^ circulate_left(a, 12)
        tt_1 = (ff(a, b, c, i) + d + s_2 + m_l[i]) & 0xffffffff
        tt_2 = (gg(e, f, g, i) + h + s_1 + m[i]) & 0xffffffff
        a, b, c, d, e, f, g, h = tt_1, a, circulate_left(
            b, 9), c, p_0(tt_2), e, circulate_left(f, 19), g
    v_p = [a ^ v[0], b ^ v[1], c ^ v[2], d ^
              v[3], e ^ v[4], f ^ v[5], g ^ v[6], h ^ v[7]]
    return v_p

#SM3主函数，对消息进行哈希操作
def sm3(mes):
    mes_pad = padding_func(mes)
    rounds = len(mes_pad) // 64
    v = iv
    for i in range(rounds):
        v = cf_func(v, mes_pad[64 * i:64 * (i + 1)])
    result = ''
    for num in v:
        result += '{:08x}'.format(num)
    return result


def result_out():
    mes='bcd'
    print('消息:',mes)
    print('哈希值:',sm3(mes))


if __name__ == '__main__':
    result_out()
