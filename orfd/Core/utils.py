#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py    
@Desc    :   工具模块
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:44        the freer      2.1
'''
import re
import pandas as pd
from collections import Counter

from setting import PATTERNS, AVG_SEGMENT_LENGTH, AVG_SEGMENT_NUMBER, AVG_DOC_LENGTH

# def is_valid_email(string):
# 	if re.match(PATTERNS["email"], string):
# 		return 1
# 	return 0
#
# def is_valid_contact(string):
# 	if re.match(PATTERNS["contact"], string):
# 		return 1
# 	return 0
#
# def is_valid_url(string):
# 	if re.match(PATTERNS["url"], string):
# 		return 1
# 	return 0
#
# def is_valid_time(string):
# 	if re.match(PATTERNS["work_time"], string):
# 		return 1
# 	return 0
#

def is_fresh(string):
	'''
	判断输入工作要求是否包括："接受应届生"
	:param string:
	:return:
	'''
	if len(re.split(",", string)) > 1:
		return 1
	return 0

def split_require(input_list):
	'''
	分割工作要求
	:param input_list: 输入要求列表
	:return: 分割结果列表
	'''
	edu_requires = []
	work_requires = []
	for inp in input_list:
		try:
			inp = re.sub(r",.*", "", inp)
			r_list = re.split("_", inp)
			edu_requires.append(r_list[0])
			work_requires.append(r_list[1])
		except:
			edu_requires.append(inp)
			work_requires.append(inp)
	return edu_requires, work_requires

def split_welfare(string):
	'''
	将福利文本分割，数据采集结果福利信息被保存为统一格式：w1_w2_w3
	:param string: 输入福利
	:return: 福利列表
	'''
	try:
		tmp_list = re.split(",", string)
		welfare = re.split(r"_", tmp_list[0])
	except:
		welfare = ["None"]
	return welfare

def welfare_map(w_list, dic):
	'''
	对输入福利类别进行映射
	:param w_list: 类别列表
	:param dic: 类别:Label 字典
	:return: 编码结果列表
	'''
	new_welfare = []
	for w in w_list:
		if w in dic.keys():
			new_welfare.append(dic[w])
		else:
			new_welfare.append(dic["others"])
	return new_welfare

def welfare_count(input_list):
	'''
	统计输入类别列表的类别频率
	:param input_list: 输入类别列表
	:return: Counter 对象，保存了类别频率排序结果
	'''
	welfare_list = []
	for inp in input_list:
		welfare_list += inp
	return Counter(welfare_list)

def split_doc(doc):
	'''
	处理输入段落文本，输出长度 < 168的句段
	:param doc: 输入段落
	:return: 句段
	'''
	seg_list = re.split(PATTERNS["segment"], doc)
	segment = ""
	for seg in seg_list:
		if len(seg) > AVG_SEGMENT_LENGTH:
			segment += seg
	if len(segment) > AVG_DOC_LENGTH:
		segment = segment[:AVG_DOC_LENGTH]
	if len(segment) < AVG_DOC_LENGTH and len(seg_list) < AVG_SEGMENT_NUMBER:
		segment = "".join(seg_list)
	if len(segment) < AVG_SEGMENT_LENGTH:
		segment = "".join(seg_list)
	print(len(segment))
	return segment

def split_doc_2(doc):
	'''
	返回对输入段落分段及过滤处理之后的长度
	:param doc: 输入段落
	:return: 处理之后的长度
	'''
	seg_list = re.split(PATTERNS["segment"], doc)
	segment = ""
	for seg in seg_list:
		if len(seg) > AVG_SEGMENT_LENGTH:
			segment += seg
	return len(segment)

def split_dataset(ori, tri, tes, frac=0.9216):
	'''
	划分原始数据集为训练集和测试集
	:param ori: 原始数据集路径
	:param tri: 输出测试集路径
	:param tes: 输出测试集路径
	:param frac: 划分比例：tes:tri
	:return:
	'''
	origin_data = pd.read_csv(ori)  # frac=0.9216
	fake = origin_data[origin_data[list(origin_data.columns)[-1]] == 0].sample(frac=frac, random_state=0, axis=0)
	real = origin_data[origin_data[list(origin_data.columns)[-1]] == 1].sample(len(fake), random_state=0, axis=0)
	train_data = pd.concat([fake, real], axis=0, join="outer")
	train_data = train_data.sample(frac=1)
	test_data = origin_data[~origin_data.index.isin(train_data.index)]
	print(len(origin_data))
	print(len(train_data))
	print(len(test_data))
	train_data.to_csv(tri, index=False)
	test_data.to_csv(tes, index=False)
