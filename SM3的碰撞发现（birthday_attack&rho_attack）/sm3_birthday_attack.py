import sm3
import random

#获取由n个不同整数组成的随机数列表
def get_randomint(n):
    random_list=[]
    while len(random_list) < n:
        i=random.randint(0, pow(2,64))
        if i not in random_list:
            random_list.append(i)
    return random_list
    
#生日攻击方法，参数bit为寻找哈希值前bit位相同
def birthday_attack(bit):
    list_randomint=get_randomint(pow(2,int (bit / 2)))
    list_hash=[]
    for i in range(0,pow(2,int (bit / 2))):
        hash_tmp=sm3.sm3_hash(str(list_randomint[i]))[0:int (bit / 4)]
        list_hash.append(hash_tmp)
    for j in range(0,pow(2,int (bit / 2))):
        for k in range(j+1,pow(2,int (bit / 2))):
            if list_hash[j]==list_hash[k]:
                result=[list_randomint[k],list_randomint[j],list_hash[j],list_hash[k]]
                print('发现哈希值前',bit,'位碰撞！')
                print('消息1:',list_randomint[k])
                print('哈希值1:',sm3.sm3_hash(str(list_randomint[k])))
                print('消息2:',list_randomint[j])
                print('哈希值2:',sm3.sm3_hash(str(list_randomint[j])))
                print('哈希值相等部分为:',list_hash[j])
                return
    print('本轮未能找到发现碰撞，请再次执行！')


if __name__ == '__main__':
    bit = 16 #假设找前16位相同
    birthday_attack(bit)
    
"""    
发现哈希值前 16 位碰撞！
消息1: 4526327104337290988
哈希值1: 43dc855855c11a2e70bc340f8e28cd217c99bf6215be31c589f23db5115e34c6
消息2: 4737390584541828579
哈希值2: 43dcff0de28f7d542e98c253021e88764ef70b08adf20c8abb2cca80d7628caa
哈希值相等部分为: 43dc
"""
