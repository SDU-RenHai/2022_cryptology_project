import sm3


#rho攻击
def rho_attack(mes,bit):
    mes_list=[mes]
    hash_list=[]
    for i in range(pow(2,int(bit /2))):
        mes=sm3.sm3_hash(mes)
        hash_list.append(mes[0:int(bit / 4)]) #寻找前bit位相同
        mes_list.append(mes)
        for j in range(0,i):
            if hash_list[j]==mes[0:int(bit / 4)]:
                print('发现前',bit,'位碰撞！')
                print('消息1:',mes_list[j])
                print('哈希值1:',sm3.sm3_hash(mes_list[j]))
                print('消息2:',mes_list[i])
                print('哈希值2:',sm3.sm3_hash(mes_list[i]))
                print('哈希值相等部分为:',hash_list[j])
                return 
    print('本轮未能发现碰撞，请再次执行代码!')

if __name__ == '__main__':
    mes='my name is renhai' #初始消息
    bit = 16 #寻找前bit位碰撞，为了便于助教检验代码，此处将参数设置为16，实际上最终找到了前32位相等的碰撞，附在代码后，请助教查阅。
    rho_attack(mes,bit)


"""
消息1：'c563692c21e31639f127ffc500d142bae4b7a6746a69397d9eae124bc47c4527'

哈希值1：'687fcd9eea0c49dac2714ef40d9bbcafaa614b63e40ef5092803251fc78212c5'

消息2：'7e2a72bb73f3c68b5e585822458b2536ac5b787152dabd70c7bf8c8c7ab1512f'

哈希值2：'687fcd9ec430f9dbc2f9d1e6f2c447dd873c88580ff325aa6586272fd669094d'

对比哈希值1与哈希值2，可知其前32位均为'687fcd9e'
"""
