## 数据分析结果

- [x] a. [每一个属性的详细含义](#a. 烂熟于心)
- [x] b. [对属性进行分类](#b. 分类)
- [x] c. [找出所有相互之间具有相关性的属性](#c. 相关性属性)
- [x] d. [进行数学分析或者可视化分析](#c. 相关性属性)
- [x] e. [属性剔除、结合、分割](#e. 最终结果)
- [x] f. [文本属性分析](#e. 最终结果)

### a. 烂熟于心

### b. 分类

- 短文本
  - 描述
    - 可编码
      1. creditCode 1
      2. orgNumber 1
      3. regAddress 1
      4. regAuthority 
    - 不可编码：
      1. companyName
      2. companyAddr 
      3. jobTitle 3
      4. jobSubTitle 3
      5. jobAddr 
  - 类别
    1. companyCharacter 1
    2. companySize 1
    3. operatingStatus 1
    4. jobWelfare 1
    5. jobRequirement 1
    6. jobCity 1
  - 带数字
    1. companySize 1
    2. regCapital 1
    3. jobSalary 1
    4. needNumber 1 
- 数字
  - 独立数字
    1. regCapital 1
    2. jobSalary 1
  - 疑似相关数字
    1. positionTotal1
    2. feedbackRation 1
    3. companySize1
    4. applyNum1
    5. resumeReadPercent 1
    6. needNumber 1
  - 范围
    1. jobSalary（处理之后）1
- 长文本
  1. companyIntro 6
  2. businessScope 6
  3. jobDescription 3 7

### c. 相关性属性

- 数学公式相关

  1. resumeReadPercent、applyNum
  2. feedbackRation、applyNum

- 关系不明

  > 属于相关数字的 6 个属性，需要一一进行数学分析及可视化分析

### d. 可视化分析及数学分析

可视化分析猜测

> 取 sh_0.xls 表格的数据进行测试，共 720 条

- 可视化

  暂略，经过热力图分析，发现并没有相关性很强的属性，所以——可喜可贺

数学分析验证，无需

### e. 最终结果

- 直接使用
  1. regCapital 
  2. jobSalary
  3. needNumber
  4. positionTotal
  5. feedbackRation
  6. applyNum
  7. resumeReadPercent 
  8. jobDescription

- 剔除

  1. companyName
  2. companyAddr
  3. jobAddr 
  4. regAuthority

- 结合

  1. jobTitle、jobSubTitle、jobDescription 

     职位描述与职位标题、子标题匹配度 —— 循环比对相似度，一定的算法计算统计数值作为相似度

  2. companyIntro、businessScope

     公司描述是否直接复制公司经营范围

- 转化

  1. 0/1编码：
     - creditCode
     - orgNumber
     - regAddress
  2. 类别编码：
     - companyCharacter 
     - companySize
     - operatingStatus
     - jobWelfare
     - jobRequirement
     - jobCity

- 分割

  1. companyIntro

     - 有无

     - 是否过短（描述长度统计值）
     - 公司描述是否里提及招聘 **
  2. jobDescription

     - 是否过短（描述长度统计值）
     - 无用信息是否过多（各种处理之前长度 - 各种处理之后长度）
     - 描述是否提到联系方式 **
     - 感叹号及其他特殊元素数目
     - 描述是否出现职业名称和标准描述五大要素（人工）
  3. jobWelfare
     - 描述是否出现联系方式关键词

  