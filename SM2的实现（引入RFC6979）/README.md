项目说明
===
:heavy_check_mark: **Project: impl sm2 with RFC6979**  
## 项目介绍 
该项目为SM2签名算法及加密算法的实现（分别对应`SM2_sign.py`、`sm2_enc.py`），同时引入`RFC6979`，以实现对`k`的确定性生成。由于随机数`k`的选取可能会导致一系列的密钥泄露（详细参见项目：Project: verify the above pitfalls with proof-of-concept code），因此在`RFC6979`中，采用确定性生成的方式，来规避这些漏洞，以公式`k=SHA256(d+Hash(msg))`，引入密钥、消息的信息，将`k`的安全性保障交给`SHA256`的抗碰撞性。
 ## 项目完成人
  * **任海（学号：201900460064）**  
 ## 运行指导 
 **开发环境：** 
 * Windows Visual Studio Code  
 * Python 3.7.9  
 
 **依赖库：**  
 * SM2_sign.py  
 ```Python
import secrets
import sm3
import libnum
import hashlib
 ```
 * sm2_enc.py  
  ```Python
import sm3
import math
import libnum
import hashlib
import random
import binascii
```

 **SM2签名算法代码的执行：**  
 * 运行`SM2_sign.py`
 * 运行案例截图：
 
 
 
 * **初始化参数**  
 该部分主要根据国密局给出的规范定义设置`p`、`a`、`b`、`n`、`Gx`、`Gy`等参数
 * **预计算**  
 计算`ZA`，由于计算过程中需要`SM3`，因此引入此前实现的`SM3`代码
 * **生成密钥**  
 生成`dA`、`k`等密钥，其中生成`k`时，引入`KFC6979`，利用公式`k=SHA256(d+Hash(msg))`，确定性计算`k`
 * **计算签名**  
 根据SM2的定义计算消息签名值
 * **验证函数**  
 根据SM2的定义编写验证函数，若验证通过，则输出`True`，若验证不通过，则输出`False`
 * **实例测试**  
 以`my name is renhai`为消息进行签名、验证
 
 
