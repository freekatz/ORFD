#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setting.py    
@Desc    :   
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:49        the freer      2.1
'''
import os

## 剔除的属性
FILTER = [
	"Company_ID", "companyBaseUrl", "companyTrade", "companyType",
	"teamTime", "entUrl", "companyDetailUrl", "Job_ID", "browserNum",
	"jobUpdateTime", "jobDetailUrl", "companyName", "estiblishDate",
	"companyAddr", "jobAddr", "regAuthority", "businessScope",
]

## 输入数据
EXCEL_DIR = "./Core/excels/"
FILE_PATHS = [EXCEL_DIR + file for file in os.listdir(EXCEL_DIR)]
ORIGIN_PATH = "./Core/dataset/origin.csv"

DOC_ALL_PATH = "./Core/dataset/doc/all.csv"
DOC_TRAIN_PATH = "./Core/dataset/doc/train.csv"
DOC_TEST_PATH = "./Core/dataset/doc/test.csv"

VEC_ALL_PATH = "./Core/dataset/vec/all.csv"
VEC_TRAIN_PATH = "./Core/dataset/vec/train.csv"
VEC_TEST_PATH = "./Core/dataset/vec/test.csv"
VEC_LARGE_PATH = "./Core/dataset/vec/large.csv"
## K-Folder, K=10
N_SPLIT = 10

## 模型路径相关
MODEL_DIR = "./Core/models/"
DOC_MODEL_NAME = "doc.m"
VEC_MODEL_NAME = "vec.m"

## PCA 模型路径
VEC_PCA_PATH = MODEL_DIR + "vec_pca.m"
DOC_PCA_PATH = MODEL_DIR + "doc_pca.m"

## 特征选择数目
FEATURE_SELECT_NUMBER = 100

## 精度，precision
VEC_PRECISION = 0.887
DOC_PRECISION = 0.738

SCORING = VEC_PRECISION + DOC_PRECISION

## keywords
KEYWORD_DIR = "./Core/keywords/"
KEYWPRDS = [KEYWORD_DIR + file for file in os.listdir(KEYWORD_DIR)]

## 正则工具
PATTERNS = {
	"segment": r'[\u3002\uff1b\uff0c\uff1a\u3001\uff1f\uff01\u201c\u201d\uff08\uff09\u300a\u300b【】\{\}\(\)?,]*',
	"digital": r'([0-9]*\.?[0-9]+)',
	"contact": r'(\d{1,11})+.?(手|call|机|号|联|联系|拨打|拨|讯|微.{1}信|薇.{1}信|威.{1}信|q|Q|QQ|Qq|qq|qQ|话|电)+.*?(\d{1,11})+',
	"email": r'([0-9a-zA-Z]+\.*)([0-9a-zA-Z]+)\@+[0-9a-zA-Z]+\.[0-9a-zA-Z]{3}(\.[0-9a-zA-Z]{2}|)',
	"url": r'([http|ftp|https])?(:\/\/)?([0-9a-zA-Z]*)?\.?([0-9a-zA-Z]+\.[0-9a-zA-Z]+)',
	"work_time": r'(2[0-4]|[0-1][0-9]|[0-9])[:：]{1}([0-5][0-9]|[0-9])',
}

## 数字 None 处理
DIGITAL_NONE = -1.0

## 段落平均长度
AVG_DOC_LENGTH = 168

## 句段平均长度
AVG_SEGMENT_LENGTH = 12

## 段落句段数目最大值
MAX_SEGMENT_NUMBER = 46

## 段落句段数目平均值，清理之后, 清理之前：8
AVG_SEGMENT_NUMBER = 168/12

## 选取福利类别数目, - 2 是因为新增的"其他类别"，以及"None"类别
WELFARE_NUMBER = 20 - 2

## Columns，列名称
COLUMNS = [
	'jobTitle', 'jobSubTitle', 'jobSalary',
	'applyNum', 'resumeReadPercent', 'jobWelfare',
	'jobRequirement', 'jobCity', 'jobDescription',
	'needNumber', 'positionTotal', 'companyCharacter',
	'feedbackRation', 'companySize', 'creditCode',
	'operatingStatus', 'regAddress', 'orgNumber',
	'regCapital', 'companyIntro', 'Real/Fake'
]

## web log
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
LOG_DIR_DEBUG = "./logs/debug/"
