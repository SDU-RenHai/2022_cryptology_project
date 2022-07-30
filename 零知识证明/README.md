项目方案及说明
===
:heavy_check_mark: **Project : Write a circuit to prove that your CET6 grade is larger than 425**
## 前置知识  
零知识证明可使得证明提供方在不透露任何与声明本身相关的信息的情况下向验证方证明其声明的正确性。零知识证明主要具备完备性、可靠性、零知识性等特点，在该项目中，构造交互式零知识证明方案来完成验证。
## 方案构造  
* **已知条件**  
:one:由题可知，$MoE$提供的成绩格式为$Grade = (cn_id,grade,year,sig_{moe})$；  
:two:令$g = grade$。  

* **成绩构造**  
:one:借助于离散对数的单向性，可据此构造交互式零知识证明方案；  
:two:确定ECC曲线参数（`P`：大素数，`G`：基点）。  
:three:选择随机数`k`，面试者计算并保存$k* G$，再计算$(k+g)* G$，面试者可据此计算出$k* G$、$(k+1)* G$ ··· $(k+g)* G$；  
:four:使用$MoE$的私钥进行签名，得到$sig_{moe}=signature_{sk}(cn_id||year||(k+g)* G)$；


