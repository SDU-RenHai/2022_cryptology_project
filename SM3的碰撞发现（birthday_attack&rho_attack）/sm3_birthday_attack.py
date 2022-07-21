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
    
#生日攻击方法
def birthday_attack():
    list_randomint=get_randomint(pow(2,16))
    print('Random list ready')
    list_hash=[]
    for i in range(0,pow(2,16)):
        hash_tmp=sm3.sm3_hash(str(list_randomint[i]))[0:8]
        list_hash.append(hash_tmp)
    for j in range(0,pow(2,16)):
        for k in range(j+1,pow(2,16)):
            if list_hash[j]==list_hash[k]:
                result=[list_randomint[k],list_randomint[j],list_hash[j],list_hash[k]]
                return result
            else:
                print('pass')
    print('Fail!')


if __name__ == '__main__':
    print(birthday_attack())
    
"""    
消息1：'1380803642756806850'

哈希值1：'1fe5f161fc1861a829c77e12ccc699b7c160187288ba2d2d5ed246a71abac7ff'

消息2：'9545009096257695477'

哈希值2：'1fe5ea8e8fd0084449ac6fccabb6cad9a618b586942af0131d35e1af198cac0d'

对比哈希值1与哈希值2，可知其前16位均为'1fe5'
"""
