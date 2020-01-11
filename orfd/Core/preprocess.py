#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   preprocess.py    
@Desc    :   数据预处理以及特征工程初步编码工作模块
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
import numpy as np
from sklearn import preprocessing

from Core.utils import is_fresh, split_require, split_welfare, \
	welfare_map, welfare_count, split_doc_2
from setting import PATTERNS, DIGITAL_NONE, FILE_PATHS, FILTER, \
	KEYWPRDS, ORIGIN_PATH, WELFARE_NUMBER, COLUMNS

def xls2csv(n=1):
	'''
	从原始 Excel 表格数据中提取 Fake 信息，
	并根据 Fake 信息数目生成原始数据集 origin.csv
	:param n: real_number/fake_number，默认为：1
	:return: None
	'''
	csv = pd.DataFrame(columns=COLUMNS)
	for file in FILE_PATHS: # 合并 xls
		xls = pd.read_excel(file).drop(columns=FILTER, axis=1)
		csv = pd.concat([xls, csv], axis=0, ignore_index=True, sort=False)
	csv = csv.loc[:, ~csv.columns.str.contains('^Unnamed')] # 去除冗余列
	csv = csv.drop_duplicates() # 去除重复数据
	csv.dropna(axis=0, subset=["Real/Fake"], inplace=True) # 去除标签为 nan 的数据
	labels = list(csv.get("Real/Fake"))
	for i in range(len(labels)):
		if labels[i] == 11:
			labels[i] = 1
		elif labels[i] == 0.5:
			labels[i] = 0
	csv["Real/Fake"] = labels
	fake = csv[csv["Real/Fake"] == 0]
	fake_ = csv[csv["Real/Fake"] == 2]
	fake = pd.concat([fake, fake_], axis=0, join="outer")
	real = csv[csv["Real/Fake"] == 1].sample(len(fake)*n, random_state=0, axis=0)
	fake["Real/Fake"] = [0 for i in range(len(fake))]
	real["Real/Fake"] = [1 for i in range(len(real))]
	origin = pd.concat([fake, real], axis=0, join="outer") # 合并 real 和 fake
	origin = origin.sample(frac=1) # 对原始数据集的数据顺序进行置乱
	origin.to_csv(ORIGIN_PATH, index=False)

def digital(input_list, mode):
	'''
	数字类型数据处理，包括纯数字与文本数字
	:param input_list: 输入字符串列表
	:param mode: 处理模式：pd-纯数字、td-纯文本数字、tda-文本数字范围
	:return: output_list
	'''
	output_list = []
	for inp in input_list:
		try:
			if mode == "tda":
				digital_list = re.findall(PATTERNS["digital"], inp)
				if inp == "薪资面议":
					output_list.append([DIGITAL_NONE, DIGITAL_NONE])
				else:
					output_list.append([int(d) for d in digital_list])
			elif mode == "td":
				digital_list = re.findall(PATTERNS["digital"], inp)
				if re.search(r"若干", inp):
					output_list.append(0)
				else:
					output_list.append(float(digital_list[0]))
			else:
				output_list.append(float(inp))
		except:
			output_list.append(DIGITAL_NONE)
	return output_list

def welfare_labels(train_list, welfare_list):
	'''
	对工作福利类别编码
	:param train_list: 原始数据列
	:param welfare_list: 福利列表
	:return: 编码结果
	'''
	# 对类别频率进行排序
	counts = welfare_count([split_welfare(inp) for inp in train_list])
	label_encoder = preprocessing.LabelEncoder()
	# 此步骤是由于福利类别过多，且类别分布过于集中，故选取前 18 种类别进行 Label Encoder 模型适配
	# 加上其他类别以及空类别，福利类别共 20 种
	welfare_fit = list(counts.keys())[:WELFARE_NUMBER] + ["others", "None"]
	welfare_labels = label_encoder.fit_transform(np.array(welfare_fit))
	welfare_labels = np.array([welfare_labels]).T
	# 此步骤是根据上面的 20 个类别以及 20 种分别对应的 Label 生成的字典
	# 目的是为了对 welfare_list 中的类别进行 Map 映射
	welfare_dict = {key: value for key, value in zip(welfare_fit, welfare_labels)}
	welfare_one_hot_encoder = preprocessing.OneHotEncoder(categories='auto')
	welfare_one_hot_encoder.fit(welfare_labels)
	label_list = []
	for welfare in welfare_list:
		w_map = welfare_map(welfare, welfare_dict)
		label = np.zeros((1, WELFARE_NUMBER + 2))
		for w in w_map:
			label += welfare_one_hot_encoder.transform([w]).toarray()
		label_list.append(label)
	return label_list

def category(input_list, mode, choice, col):
	'''
	处理所有类别列及添加的额外类别，包括多类别、单类别、关键词匹配类别
	:param input_list: 输入类别列表
	:param mode: 处理模式：oz-bool、ot-单文本、mt-多文本、kt-关键词匹配
	:param choice: 选项，针对不同选项进行不同的处理
	:param col: 列名称，由于 Label 编码需要适配原始数据集，故选择在这里读入
	:return: output_list
	'''
	df = pd.read_csv(ORIGIN_PATH)
	train_list = list(df.get(col))
	output_list = []
	if mode == "oz": # 即 one-zero
		if choice == "fresh": # 即公司是否接受应届生
			return [is_fresh(inp) for inp in input_list]
		else: # 通用 0/1 编码：有为 1、无为 0
			for inp in input_list:
				if inp == None or inp == np.nan or inp == "nan" or inp == "None" or inp == "":
					output_list.append(0)
				else:
					output_list.append(1)
	elif mode == "ot": # 即 one-text，所有单类别文本编码通用
		label_encoder = preprocessing.LabelEncoder()
		train_labels = label_encoder.fit_transform(np.array(train_list))
		train_labels = np.array([train_labels]).T
		labels = label_encoder.transform(np.array(input_list))
		labels = np.array([labels]).T
		one_hot_encoder = preprocessing.OneHotEncoder(categories='auto')
		one_hot_encoder.fit(train_labels)
		for label in labels:
			output_list.append(one_hot_encoder.transform([label]).toarray())
	elif mode == "mt": # 即 multi-text，根据 choice 针对性处理
		if choice == "require": # 处理职位要求
			train_edu_list, train_work_list = split_require(train_list)
			edu_list, work_list = split_require(input_list)
			edu_label_encoder = preprocessing.LabelEncoder()
			work_label_encoder = preprocessing.LabelEncoder()
			# 适配原始数据集
			edu_train_labels = edu_label_encoder.fit_transform(train_edu_list)
			work_train_labels = work_label_encoder.fit_transform(train_work_list)
			edu_train_labels = np.array([edu_train_labels]).T
			work_train_labels = np.array([work_train_labels]).T
			edu_labels = edu_label_encoder.transform(np.array(edu_list))
			work_labels = work_label_encoder.transform(np.array(work_list))
			edu_labels = np.array([edu_labels]).T
			work_labels = np.array([work_labels]).T
			edu_one_hot_encoder = preprocessing.OneHotEncoder(categories='auto')
			edu_one_hot_encoder.fit(edu_train_labels)
			work_one_hot_encoder = preprocessing.OneHotEncoder(categories='auto')
			work_one_hot_encoder.fit(work_train_labels)
			for edu_label, work_label in zip(edu_labels, work_labels):
				output_list.append((
					edu_one_hot_encoder.transform([edu_label]).toarray(),
					work_one_hot_encoder.transform([work_label]).toarray()
				))
		else: # 处理工作福利
			welfare_list = [split_welfare(inp) for inp in input_list]
			output_list = welfare_labels(train_list, welfare_list)
	else: # 关键词匹配
		if choice == "company": # 公司描述关键词匹配，result 为 []*6
			comp_intro = open(KEYWPRDS[0], "r", encoding="utf-8").readlines()
			job_intro = open(KEYWPRDS[2], "r", encoding="utf-8").readlines()
			require = open(KEYWPRDS[3], "r", encoding="utf-8").readlines()
			salary = open(KEYWPRDS[4], "r", encoding="utf-8").readlines()
			welfare = open(KEYWPRDS[5], "r", encoding="utf-8").readlines()
			work_time = open(KEYWPRDS[6], "r", encoding="utf-8").readlines()
			for inp in input_list:
				try:
					result = [0] * 6
					result[0] = len(inp)
					for c_i in comp_intro:
						if re.search(c_i.replace("\n", ""), inp):
							print("company: ", c_i)
							result[0] = 0
							break
					for j_i in job_intro:
						if re.search(j_i.replace("\n", ""), inp):
							print("company: ", j_i)
							result[1] = 1
							break
					for r in require:
						if re.search(r.replace("\n", ""), inp):
							print("company: ", r)
							result[2] = 1
							break
					for s in salary:
						if re.search(s.replace("\n", ""), inp):
							print("company: ", s)
							result[3] = 1
							break
					for w in welfare:
						if re.search(w.replace("\n", ""), inp):
							print("company: ", w)
							result[4] = 1
							break
					for w_t in work_time:
						if re.search(w_t.replace("\n", ""), inp):
							print("company: ", w_t)
							result[5] = 1
							break
					if result[5] == 0 and re.search(PATTERNS["work_time"], inp):
						print("company: ", re.findall(PATTERNS["work_time"], inp))
						result[5] = 1
					output_list.append(result)
				except:
					output_list.append([0] * 6)
		elif choice == "recruit": # 职位描述关键词匹配，result 为 []*10
			contact = open(KEYWPRDS[1], "r", encoding="utf-8").readlines()
			job_intro = open(KEYWPRDS[2], "r", encoding="utf-8").readlines()
			require = open(KEYWPRDS[3], "r", encoding="utf-8").readlines()
			salary = open(KEYWPRDS[4], "r", encoding="utf-8").readlines()
			welfare = open(KEYWPRDS[5], "r", encoding="utf-8").readlines()
			work_time = open(KEYWPRDS[6], "r", encoding="utf-8").readlines()
			for inp in input_list:
				try:
					result = [0] * 10
					result[0] = len(inp)
					result[1] = split_doc_2(inp)
					for j_i in job_intro:
						if re.search(j_i.replace("\n", ""), inp):
							print("recruit", j_i)
							result[2] = 1
							break
					for r in require:
						if re.search(r.replace("\n", ""), inp):
							print("recruit", r)
							result[3] = 1
							break
					for s in salary:
						if re.search(s.replace("\n", ""), inp):
							print("recruit", s)
							result[4] = 1
							break
					for w in welfare:
						if re.search(w.replace("\n", ""), inp):
							print("recruit", w)
							result[5] = 1
							break
					for w_t in work_time:
						if re.search(w_t.replace("\n", ""), inp) or re.search(PATTERNS["work_time"], inp):
							print("recruit", w_t)
							result[6] = 1
							break
					for c in contact:
						c = c.replace("\n", "")
						if re.search(c, inp):
							print("recruit", c)
							result[7] = 1
							break
					if result[7] == 0 and re.search(PATTERNS["contact"], inp):
						print("recruit", re.findall(PATTERNS["contact"], inp))
						result[7] = 1
					if re.search(PATTERNS["email"], inp):
						print("recruit", re.findall(PATTERNS["email"], inp))
						result[8] = 1
					if re.search(PATTERNS["url"], inp):
						print("recruit", re.findall(PATTERNS["url"], inp))
						result[9] = 1
					# print(result)
					output_list.append(result)
				except:
					output_list.append([0] * 10)
		elif choice == "welfare": # 福利关键词匹配，result 为 0/1
			contact = open(KEYWPRDS[1], "r", encoding="utf-8").readlines()
			for inp in input_list:
				result = 0
				try:
					if re.search(PATTERNS["contact"], inp):
						print("welfare", re.findall(PATTERNS["contact"], inp))
						result = 1
						output_list.append(result)
						continue
					for c in contact:
						if re.search(c.replace("\n", ""), inp):
							print("welfare", re.findall(c.replace("\n", ""), inp))
							result = 1
							break
					output_list.append(result)
				except:
					output_list.append(result)
	return output_list

def seg2code(bc, input_list):
	'''
	对输入句段列表进行句段编码
	:param bc: BertClient 对象
	:param input_list: 输入列表
	:return: 文本向量列表
	'''
	return bc.encode(list(input_list))
