项目说明
===
:heavy_check_mark: **Project: verify the above pitfalls with proof-of-concept code**  
:heavy_check_mark: **Project: forge a signature to pretend that you are Satoshi**  

## 项目介绍  
该项目包含上述两个项目（分别对应`ECDSA.py`和`ECDSA_forge.py`，是以ECDSA算法为例，对ECDSA、Schnorr、SM2-sig算法共同存在的部分缺陷的实现，同时完成签名伪造任务。

 ## 项目完成人
 * **任海（学号：201900460064）**  
 
 ## 运行指导 
 **开发环境：** 
 * Windows Visual Studio Code  
 * Python 3.7.9  
 
 **依赖库：** 
 ```Python
import random
import string
import hashlib
import binascii
import libnum
from ecdsa import SigningKey, NIST256p,numbertheory, ellipticcurve, VerifyingKey
 ```
 
 **ECDSA缺陷代码实现的执行：**  
 * 运行`ECDSA.py`
 * 运行案例截图：
 

 该项目主要是对ESCDA、Schnorr、SM2-sig算法共同存在的部分缺陷的实现，主要包含以下内容：  
 * 若`K`泄露，则可计算出私钥`d`，即私钥`d`也泄露（以ECDSA为例）  
 * 若重复使用`K`，则可计算出私钥`d`，即私钥`d`也泄露（以ECDSA为例）  
 * 两个用户，使用相同的`K`，则可以相互推断对方的私钥`d`（以ECDSA为例） 
 * 若`（r，s）`是有效签名，则`（r，-s）`也是有效签名（以ECDSA为例）
 * 若验签时无需消息，则可对任意消息进行签名伪造（以ECDSA为例）  
 * 在CEDSA和Schnorr算法中，使用相同的私钥`d`和`K`，导致私钥`d`泄露
