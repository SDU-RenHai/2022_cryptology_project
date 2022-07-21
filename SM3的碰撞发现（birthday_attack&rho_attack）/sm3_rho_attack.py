import sm3


#rho攻击
def rho_attack(mes):
    mes_list=[mes]
    hash_list=[]
    for i in range(pow(2,16)):
        mes=sm3.sm3_hash(mes)
        hash_list.append(mes[0:8]) #寻找前32位相同
        mes_list.append(mes)
        for j in range(0,i):
            if hash_list[j]==mes[0:8]:
                return [mes_list[j],mes_list[i],hash_list[j],hash_list[i]]
        print('pass')
    print('Fail !')

if __name__ == '__main__':
    mes='my name is renhai' #初始消息
    print(rho_attack(mes))

"""
消息1：'c563692c21e31639f127ffc500d142bae4b7a6746a69397d9eae124bc47c4527'

哈希值1：'687fcd9eea0c49dac2714ef40d9bbcafaa614b63e40ef5092803251fc78212c5'

消息2：'7e2a72bb73f3c68b5e585822458b2536ac5b787152dabd70c7bf8c8c7ab1512f'

哈希值2：'687fcd9ec430f9dbc2f9d1e6f2c447dd873c88580ff325aa6586272fd669094d'

对比哈希值1与哈希值2，可知其前32位均为'687fcd9e'
"""
