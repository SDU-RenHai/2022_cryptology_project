项目说明
===
:heavy_check_mark: **project: implement SM3**   
:heavy_check_mark: **project: implement the naïve birthday attack of reduced SM3**  
:heavy_check_mark: **project: implement the Rho method of reduced SM3**  
 ## 运行指导 
 **开发环境：** 
 * Windows Visual Studio Code  
 * Python 3.7.9  
**依赖库：**    
 
 该项目由sm3的python实现、生日攻击、rho方法三部分组成，最终找到了最多前32bit的碰撞结果，如下。
 在rho方法中，以`"my name is renhai"`为初始消息，不断迭代，可找到哈希值前32位相同的两个消息：
 * 消息1：`'c563692c21e31639f127ffc500d142bae4b7a6746a69397d9eae124bc47c4527'`
 * 哈希值1：`'687fcd9eea0c49dac2714ef40d9bbcafaa614b63e40ef5092803251fc78212c5'`
 * 消息2：`'7e2a72bb73f3c68b5e585822458b2536ac5b787152dabd70c7bf8c8c7ab1512f'`
 * 哈希值2：`'687fcd9ec430f9dbc2f9d1e6f2c447dd873c88580ff325aa6586272fd669094d'`
 * 对比哈希值1与哈希值2，可知其前32位均为`'687fcd9e'`

