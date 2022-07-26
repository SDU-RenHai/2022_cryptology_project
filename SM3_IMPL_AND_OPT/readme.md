# SIMD的朴素（Naive）实现以及SIMD加速实现

## Run

### Run on Windows

**`Windows_VS2022Project`中的工程用于在Windows上运行。双击文件夹中的`VS_project.sln`即可打开工程，直接运行**。

**环境：**

- 在Windows上运行应该拥有2022 Community版本以上的Visual Studio。

- C++版本应该被设置为C++ 17（或者更高）。

  ![image-20220726214831340](images/image-20220726214831340.png)

- 支持如下的SIMD函数（**否则会抛出异常**）：

  ```C++
  _mm256_set1_epi32();
  _mm256_loadu_epi32();
  _mm256_storeu_epi32();
  _mm256_add_epi32();
  _mm256_or_epi32();
  _mm256_xor_epi32();
  _mm256_and_epi32();
  _mm256_andnot_epi32();
  _mm256_slli_epi32();
  ```

### Run on Linux

**Linux上的工程使用Makefile。如果环境支持，打开shell，使用`make`命令即可生成名为`linux_run`的可执行文件**。

**环境：**

- 使用的GCC应该满足如下的编译命令：

  ```
  g++ -O2 -std=c++17 -mavx2 -mavx -mavx512f -mavx512vl
  ```

- 支持如下的SIMD函数（与Windows上不同，**如果出现不支持的函数会提示`Illegal Instruction`**）：

  ```c++
  _mm256_set1_epi32();
  _mm256_store_epi64();
  _mm256_load_si256();
  _mm256_add_epi32();
  _mm256_slli_epi32();
  _mm256_or_si256();
  _mm256_xor_si256();
  _mm256_and_si256();
  _mm256_andnot_si256();
  ```



## 结果展示

在Windows上的运行截图如下所示：

![image-20220726215632004](images/image-20220726215632004.png)

### 正确性

首先，程序对`abc`和`abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd`进行加密，分别得到Hash值为

```
66c7f0f4 62eeedd9 d1f2d46b dc10e4e2 4167c487 5cf2f7a2 297da02b 8f4ba8e0
debe9ff9 2275b8a1 38604889 c18e5a4d 6fdb70e5 387e5765 293dcba3 9c0c5732
```

这和国家密码管理局颁布的《SM3密码杂凑算法》（https://www.oscca.gov.cn/sca/xxgk/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf）中的“附录A 运算示例”是一致的。

![image-20220726215904268](images/image-20220726215904268.png)

![image-20220726215918140](images/image-20220726215918140.png)

![image-20220726215931961](images/image-20220726215931961.png)

![image-20220726215943421](images/image-20220726215943421.png)

### SIMD

从上面的运行结果可以看出，SIMD的运行时间是Naive的运行时间的20.9%、24.8%和26.9%，即**分别加速了4.78、4.03和2.71倍**。