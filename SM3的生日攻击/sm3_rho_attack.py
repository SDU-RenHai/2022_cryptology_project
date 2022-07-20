import sm3


#rho攻击
def rho_attack(mes):
    mes_list=[mes]
    hash_list=[]
    for i in range(pow(2,32)):
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


