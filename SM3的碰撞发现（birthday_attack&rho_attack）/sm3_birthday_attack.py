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