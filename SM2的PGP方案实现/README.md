项目说明
===
:heavy_check_mark: **Project: Implement a PGP scheme with SM2**  
## 项目介绍  
该项目为SM2算法的PGP方案的实现，包含`sm3.py`、`sm2_enc.py`、`PGP.py`三部分，其中前两个文件分别为SM3算法、SM2加密算法的实现，作为PGP方案的依赖库导入，第三个文件为PGP方案的具体实现。在PGP方案中，通信双方先协商好一对SM2加密算法的密钥`(sk,pk)`，当需要通信时，消息发送方选取AES算法的密钥`key`，用`key`加密消息`msg`，然后用SM2算法加密密钥`key`，将消息和`key`的加密结果一并发送给消息接收方。消息接收方收到信息后，先用SM2算法解出AES算法使用的`key`，然后用AES算法解出消息信息。流程如下图所示：
