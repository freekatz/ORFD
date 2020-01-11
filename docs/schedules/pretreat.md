## 预处理过程

### e. 处理过程

- 直接使用
  1. regCapital 
     - 文本数字：float

     - 类别很多

     - 大类别分为两种：有和None

       处理为浮点数，none为-1
  2. jobSalary
     - 文本数字范围：int

     - 类别很多

     - 大类别分为两种：详细和薪资面议

       拆分为两个或者求平均值（平均值更好一点），面议为-1
  3. needNumber
     - 文本数字：int

     - 类别很多

     - 大类别分为两种：有和None

       处理为整数，none为-1
  4. positionTotal
     - 数字：int

     - 类别很多

     - 大类别分为两种：有和None

       处理为整数，none为-1
  5. feedbackRation
     - 数字：int

     - 类别很多

     - 全有

       处理为整数
  6. applyNum

     - int

       处理为整数
  7. resumeReadPercent 

     - 与 feed 一样

       处理为整数
  8. jobDescription
     - 长文本
     - 都有

- 剔除

  1. companyName
  2. companyAddr
  3. jobAddr 
  4. regAuthority
  5. businessScope

- 结合

  1. jobTitle、jobSubTitle、jobDescription 
     - 短文本及长文本-相似度：float 这个应该去掉，因为计算相似度也要从句向量或其他向量计算得到，而我又要输入向量计算，所以这样不太好，去掉

- 转化

  1. 0/1编码：
     - creditCode：有或None - 1/0
     - orgNumber：有或None - 1/0
     - regAddress：有或None - 1/0
  2. 类别编码：一般为先编码，然后one-hot，这个后期改为表格
     - companyCharacter ：单文本类别，不存在等级关系，类别较少，one-hot
     - companySize：单文本数字类别，存在等级关系，类别较少，one-hot
     - operatingStatus：单文本类别，不存在，且有一些含义相近需要合并，类别较少，one-hot
     - jobWelfare：多文本类别 - 种类太多，离群情况严重，故选择去掉
     - jobRequirement：多文本类别，不存在，类别较少，one-hot
     - jobCity：单文本类别，不存在，类别较少，one-hot

- 分割

  1. companyIntro

     - 描述长度：int，无描述 长度为0
     - 公司描述是否里提及招聘：boolean（也是按照五大要素匹配，分为多个 bool） - 1/0 
  2. jobDescription

     - 描述长度，未处理之前 ：int
     - 描述是否提到联系方式或网页链接：boolean（关键词，我们提供关键词库或正则匹配） - 1/0
     - 描述是否出现职业名称和标准描述五大要素（人工/关键词）：分为 5 个特征，全为 bool （需要 5 个关键词库）- 1/0
  3. jobWelfare
     - 描述是否出现联系方式关键词：关键词匹配，可以考虑更换为直接匹配关键词，这个关键词是多方面的 - 1/0

## 函数

### 1、

文本数字或者纯数字处理数字函数：整型与浮点通用——

### 2、

0/1 编码类别函数：输入之前可能要对输入进行一番特定的处理，多类别特征，可以采用 one-hot 结合其他方法

### 3、

预处理文本的模块：1. 关键词提取；2. 分词；3. 停用词过滤，不同输入使用不同的停用词；4. 相似度计算函数，关键词列表计算相似度；5. 判断一个文本是否在另一个文本中出现，包括关键词匹配，段落匹配；6. 其他需要的函数，如文本经营状态类别归一化函数

经过以上步骤之后，除了文本向量化之外，所有特征构建工作完成

### 4、

文本向量化模块：可以选择 BERT 微调或者直接使用生成文本向量

### 5、

归一、标准、正则模块





​		