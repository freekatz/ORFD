## The Online Recruitment Fraud Detection Platform

This is our project documention of the 2019 national information security competition

## 项目论文

前往：[论文](./docs/issue/基于机器学习的在线招聘欺诈检测平台.pdf)

## 项目数据集

地址：[Excels](https://github.com/zjh567/orfd/tree/master/orfd/Core/excels)

人工标记的数据，耗费了大量的人力，这可能是**国内第一份**关于**虚假招聘**且**带标签**的数据集。

其中初始数据集来源于 58 同城以及智联招聘爬虫，智联招聘由于数据集虚假数目太少（并非是因为难爬，相反很好爬）所以在已经爬取了几万条信息的情况下转而选择了 58 同城。

不过由于网站改版，58 和智联的爬虫代码有一部分接口过时了，所以本仓库没有提供相关代码

## 项目流程图

![作品流程图](./docs/README.assets/作品流程图.png)

## 项目部署

由于本项目为同时对数据的向量和文本分类，使用了 Bert 作为文本编码服务，部署文本分类的环境比较大，故本仓库没有提供文本编码服务（只有一个文本分类的模型），如果需要部署测试文本分类效果可提 issue 或可先查看：[部署](./docs/issue/作品核心功能环境部署及使用须知.pdf)（相关文件找我自取）

**测试**：测试向量分类可在安装好环境后直接运行 tests-vec.py 查看运行结果。如果部署好了文本编码服务也可直接运行 tests.py 查看运行结果

<hr></hr>
## 成员分工

略

## 项目文档

### 项目解决方案：

[项目解决方案详细介绍](./docs/solution.md)

### 时间轴：

[项目目前为止时间历程](./docs/Timeline.md)

### 项目日程安排：

[项目日程安排](https://github.com/zjh567/orfd/tree/master/docs/schedules)

### 项目数据库建立及介绍

[58 同城数据库说明及分析](./docs/DB.md)

### 技术积累及探索

[机器学习](https://github.com/zjh567/orfd/tree/master/docs/ML)

[自然语言处理](https://github.com/zjh567/orfd/tree/master/docs/NLP)

## 文献阅读

[参考文献目录](https://github.com/zjh567/orfd/tree/master/docs/papers)

<hr></hr>

## LICENSE

[项目 License：GPL 3.0](./LICENSE)

[文档 License：Apache License 2.0](./docs/LICENSE)