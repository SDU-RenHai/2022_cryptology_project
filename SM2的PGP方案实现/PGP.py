import sm2_enc
from Crypto.Cipher import AES
import binascii
import random
import string


#消息发送方的加密函数
def PGP_enc(mes,key,pk,sk):
    cryptor = AES.new(key.encode('utf-8'), AES.MODE_OFB , b'0000000000000000')
    len_mes = len(mes)
    if len_mes % 16 != 0 :
        add = 16 - (len_mes % 16)
    else:
        add = 0
    mes = mes +('0' *add)
    ciphertext = cryptor.encrypt(mes.encode('UTF-8')) 
    AES_mes = binascii.b2a_hex(ciphertext).decode('UTF-8') #使用AES加密消息后的密文
    sm2_key = sm2_enc.Encrypt(key, sk, pk) #使用sm2算法加密AES使用的密钥key
    return AES_mes,sm2_key

#消息接收方的解密函数
def PGP_dec(AES_mes,sm2_key,sk):
    key = sm2_enc.decrypt(sm2_key, sk) #解密由sm2算法加密的key
    cryptor = AES.new(key.encode('utf-8'), AES.MODE_OFB , b'0000000000000000')
    plain_text = cryptor.decrypt(binascii.a2b_hex(AES_mes)) 
    mes = plain_text.decode('utf-8').rstrip('0') #解密消息
    return key,mes


if __name__ == '__main__':
    print('--------------------------测试案例----------------------------')
    #sk,pk为消息发送、接收方提前协商好的sm2公私钥对，这里用固定的值模拟
    sk = '92EBE8E51821914F5AD6C9A48FB6E9987E61F4AEE9B97997E0593431C76DC8C7'
    pk = '95C8B3C6019B841C605D46AF1B83A24D9103CF14C7DD0D8A142000D3F243B23FD1582697112E98D9182C3DE8FBA268E488A3405CDD7006645F48C2D2B4BE4B54'
    #key为AES的密钥，随机产生24bit字符串，编码后作为密钥
    key = ''.join(random.sample(string.ascii_letters, 24))

    #消息发送方拟发送的消息
    mes_enc = 'my name is renhai'
    print('消息加密方准备使用的AES密钥:',key)
    print('消息发送方准备发送的消息:',mes_enc,'\n')

    #消息发送方加密后的结果，包括用AES加密消息后的密文AES_mes和用sm2加密密钥key后的结果sm2_key
    AES_mes,sm2_key = PGP_enc(mes_enc,key,pk,sk)
    print('消息加密后的结果为:',AES_mes)
    print('密钥加密后的结果为:',sm2_key,'\n')

    #消息接收方接到两个加密信息后，先用sm2算法解密密钥信息，再用密钥解密消息信息
    key_dec, mes_dec = PGP_dec(AES_mes,sm2_key,sk)
    print('消息接收方解密的AES密钥信息:',key_dec)
    print('消息接收方解密的消息:',mes_dec)

"""
--------------------------测试案例----------------------------
消息加密方准备使用的AES密钥: bmEXkncDgINCpQvoJYAFhiWK
消息发送方准备发送的消息: my name is renhai

消息加密后的结果为: bee7f7a1fb1a302771d38a2f51960954d927bcfbc2bbe963174f2f8fa63cad3a
密钥加密后的结果为: 95c8b3c6019b841c605d46af1b83a24d9103cf14c7dd0d8a142000d3f243b23fd1582697112e98d9182c3de8fba268e488a3405cdd7006645f48c2d2b4be4b54c584892c0a910ea51d2c3cd4947207a586c3ffdf289f03e6ac90fc1e06769b14106631fdcfaf994f189c51df9842ad4b5e3db369f195c442

消息接收方解密的AES密钥信息: bmEXkncDgINCpQvoJYAFhiWK
消息接收方解密的消息: my name is renhai

"""




