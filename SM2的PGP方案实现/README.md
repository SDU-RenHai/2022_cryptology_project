项目说明
===
:heavy_check_mark: **Project: Implement a PGP scheme with SM2**  
## 项目介绍  
该项目为SM2算法的PGP方案的实现，包含`sm3.py`、`sm2_enc.py`、`PGP.py`三部分，其中前两个文件分别为SM3算法、SM2加密算法的实现，作为PGP方案的依赖库导入，第三个文件为PGP方案的具体实现。在PGP方案中，通信双方先协商好一对SM2加密算法的密钥`(sk,pk)`，当需要通信时，消息发送方选取AES算法的密钥`key`，用`key`加密消息`msg`，然后用SM2算法加密密钥`key`，将消息和`key`的加密结果一并发送给消息接收方。消息接收方收到信息后，先用SM2算法解出AES算法使用的`key`，然后用AES算法解出消息信息。流程如下图所示：
![20220729231638](images/20220729231638.png)
 ## 项目完成人
 * **任海（学号：201900460064）**  
 ## 运行指导 
 **开发环境：** 
 * Windows Visual Studio Code  
 * Python 3.7.9  
 
 **依赖库：**  
 * sm2_enc.py
 ```Python
import sm3
import math
import libnum
import hashlib
import random
import binascii
 ```
 * PGP.py
 ```Python
import sm2_enc
from Crypto.Cipher import AES
import binascii
import random
import string
 ```
 
 **SM2算法代码的执行：** 
 * 将`sm3.py`、`sm2_enc.py`文件放入同一文件夹
 * 运行`sm2_enc.py`
 * 运行案例截图：
 
