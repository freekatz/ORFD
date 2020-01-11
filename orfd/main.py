#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py    
@Desc    :   主控制模块
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:46        the freer      2.1
'''
import pandas as pd
import numpy as np
from bert_serving.client import BertClient
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from Core.classific import classific, train
from Core.utils import split_dataset, split_doc
from Core.preprocess import digital, category, seg2code, xls2csv
from setting import DOC_TRAIN_PATH, COLUMNS, ORIGIN_PATH, DOC_TEST_PATH, \
	DOC_ALL_PATH, VEC_ALL_PATH, VEC_TRAIN_PATH, VEC_TEST_PATH

def doc(df, bc, step=0):
	'''
	文本编码主控制函数
	:param df: 输入待训练或待分类的 DataFrame
	:param bc: BertClient 对象
	:param step: 处理阶段
	:return: 编码结果
	'''
	if step == 0:
		job_title = df.get("jobTitle")
		job_sub_title = df.get("jobSubTitle")
		job_description = df.get("jobDescription")
		job_segments = [split_doc(doc) for doc in job_description]
		paragraph_list = []
		for j_t, j_s_t, j_s in zip(job_title, job_sub_title, job_segments):
			paragraph = j_t + j_s_t + j_s
			paragraph_list.append(paragraph)
		paragraph_vec = seg2code(bc, paragraph_list)
		ori_vec = list(paragraph_vec)
		ori_vec = np.array(ori_vec)
		labels = list(df.get('Real/Fake'))
	else:
		ori_vec = np.array([df.get(c) for c in list(df.columns)[:-1]]).T
		labels = list(df.get(list(df.columns)[-1]))
	X = ori_vec
	out_df = pd.DataFrame(columns=[str(i) for i in range(len(X[0]) + 1)])
	i = 0
	for o, label in zip(X, labels):
		if label == np.nan or pd.isna(label):
			label = 0
		o = list(o)
		o.append(label)
		out_df.at[i] = o
		i += 1
	print("Done!")
	return out_df

def vec(df, step=0, mode="all"):
	'''
	特征编码主控制函数
	:param df: 输入待训练或待分类的 DataFrame
	:param step: 处理阶段
	:param mode: 处理模式：one-处理一条、all-处理所有
	:return: 编码结果
	'''
	data_desc = []
	if step == 0:
		job_salary = df.get("jobSalary")
		job_salary_vec = digital(job_salary, mode="tda")  # 一维向量
		apply_num = df.get("applyNum")
		apply_num_vec = digital(apply_num, mode="pd")  # 一维向量
		resume_read_percent = df.get("resumeReadPercent")
		resume_read_percent_vec = digital(resume_read_percent, mode="pd")  # 一维向量
		job_welfare = df.get("jobWelfare")
		job_welfare_vec_1 = category(job_welfare, mode="kt", choice="welfare", col="jobWelfare")  # 一维向量
		job_welfare_vec_2 = category(job_welfare, mode="mt", choice="", col="jobWelfare")
		if mode == "one":
			data_desc.append(job_welfare_vec_1[0])
		job_requirement = df.get("jobRequirement")
		job_requirement_vec = category(job_requirement, mode="mt", choice="require",
		                               col="jobRequirement")  # 形如：[(array([[1., 0.]])] 2
		job_city = df.get("jobCity")
		job_city_vec = category(job_city, mode="ot", choice="", col="jobCity")  # 形如：[(array([[1.]])] 1
		job_description = df.get("jobDescription")
		job_description_vec_1 = category(job_description, mode="kt", choice="recruit", col="jobDescription")  # 二维向量，n*9
		if mode == "one":
			data_desc.append(job_description_vec_1[0])
		need_number = df.get("needNumber")
		need_number_vec = digital(need_number, mode="td")  # 一维向量
		position_total = df.get("positionTotal")
		position_total_vec = digital(position_total, mode="pd")  # 一维向量
		company_character = df.get("companyCharacter")
		company_character_vec = category(company_character, mode="ot", choice="",
		                                 col="companyCharacter")  # 形如：[(array([[1.]])] 1
		feedback_ration = df.get("feedbackRation")
		feedback_ration_vec = digital(feedback_ration, mode="pd")  # 一维向量
		company_size = df.get("companySize")
		company_size_vec = category(company_size, mode="ot", choice="", col="companySize")  # 形如：[(array([[1.]])] 1
		credit_code = df.get("creditCode")
		credit_code_vec = category(credit_code, mode="oz", choice="", col="creditCode")  # 一维向量
		operating_status = df.get("operatingStatus")
		operating_status_vec = category(operating_status, mode="ot", choice="",
		                                col="operatingStatus")  # 形如：[(array([[1.]])] 1
		reg_address = df.get("regAddress")
		reg_address_vec = category(reg_address, mode="oz", choice="", col="regAddress")  # 一维向量
		org_number = df.get("orgNumber")
		org_number_vec = category(org_number, mode="oz", choice="", col="orgNumber")  # 一维向量
		reg_capital = df.get("regCapital")
		reg_capital_vec = digital(reg_capital, mode="td")  # 一维向量
		company_intro = df.get("companyIntro")
		company_intro_vec = category(company_intro, mode="kt", choice="company", col="companyIntro")  # 二维向量，n*6
		if mode == "one":
			data_desc.append(company_intro_vec[0])
		ori_vec = []
		for i in range(0, len(df)):
			vec = []
			j_s = job_salary_vec[i]
			vec += j_s
			a_n = apply_num_vec[i]
			vec.append(a_n)
			r_r_p = resume_read_percent_vec[i]
			vec.append(r_r_p)
			j_w_1 = job_welfare_vec_1[i]
			vec.append(j_w_1)
			j_w_2 = list(job_welfare_vec_2[i][0])
			vec += list(j_w_2)
			j_r_e = list(job_requirement_vec[i][0])[0][:5]
			j_r_e = list(j_r_e)
			if len(j_r_e) < 5:
				j_r_e.append(0)
			vec += list(j_r_e)
			j_r_w = list(job_requirement_vec[i][1])[0][:5]
			j_r_w = list(j_r_w)
			if len(j_r_w) < 5:
				j_r_w.append(0)
			vec += list(j_r_w)
			j_c = job_city_vec[i][0][0]
			vec.append(j_c)
			j_d_1 = job_description_vec_1[i]
			vec += j_d_1
			n_n = need_number_vec[i]
			vec.append(n_n)
			p_t = position_total_vec[i]
			vec.append(p_t)
			c_ch = company_character_vec[i][0][0]
			vec.append(c_ch)
			f_r = feedback_ration_vec[i]
			vec.append(f_r)
			c_s = company_size_vec[i][0][0]
			vec.append(c_s)
			c_c = credit_code_vec[i]
			vec.append(c_c)
			o_s = operating_status_vec[i][0][0]
			vec.append(o_s)
			r_a = reg_address_vec[i]
			vec.append(r_a)
			o_n = org_number_vec[i]
			vec.append(o_n)
			r_c = reg_capital_vec[i]
			vec.append(r_c)
			c_i = company_intro_vec[i]
			vec += c_i
			print("工资平均值：", j_s)
			print("申请人数：", a_n)
			print("招聘信息阅读百分比：", r_r_p)
			print("福利信息关键词匹配结果：", j_w_1)
			print("福利信息独热编码：", j_w_2)
			print("职位学历需求独热编码：", j_r_e)
			print("职位经验需求独热编码：", j_r_w)
			print("工作城市独热编码：", j_c)
			print("职位描述关键词匹配结果：", j_d_1)
			print("需求人数/岗位数：", n_n)
			print("公司发布职位总数：", p_t)
			print("公司性质独热编码：", c_ch)
			print("公司简历反馈率：", f_r)
			print("公司规模独热编码：", c_s)
			print("公司信用代码有无：", c_c)
			print("公司经营状态独热编码：", o_s)
			print("公司注册地址有无：", r_a)
			print("公司组织代码有无", o_n)
			print("公司注册资本：", r_c)
			print("公司介绍关键词匹配结果：", c_i)
			print("初始特征向量总长度", len(vec))
			ori_vec.append(vec)
		ori_vec = np.array(ori_vec)
		labels = list(df.get('Real/Fake'))
	else:
		ori_vec = np.array([df.get(c) for c in list(df.columns)[:-1]]).T
		labels = list(df.get(list(df.columns)[-1]))
	X = ori_vec
	out_df = pd.DataFrame(columns=[str(i) for i in range(len(X[0]) + 1)])
	i = 0
	for o, label in zip(X, labels):
		if label == np.nan or pd.isna(label):
			label = 0
		o = list(o)
		o.append(label)
		out_df.at[i] = o
		i += 1
	print("Done!")
	return out_df, data_desc

def csv_main(bc, df, step, choice):
	'''
	模型训练主控制
	:param bc:
	:param df:
	:param step:
	:param choice:
	:return: 编码结果：DataFrame 对象
	'''
	if choice == "doc":
		out_df = doc(df, bc, step)
	else:
		out_df, _ = vec(df, step, mode="all")
	return out_df

def data_main(bc, data, step, choice):
	'''
	模型训练主控制
	:param bc:
	:param df:
	:param step:
	:param choice:
	:return: 编码结果：列表、其他分析信息
	'''
	df = pd.DataFrame(columns=COLUMNS)
	df.at[0] = data
	if choice == "doc":
		out_df = doc(df, bc, step)
		return [list(out_df.values)[0][:-1]], None
	else:
		out_df, data_desc = vec(df, step, mode="one")
		return [list(out_df.values)[0][:-1]], data_desc

def main(bc, input_data, step_1=0, step_2=5, choice="vec", clf=None, name="rf"):
	'''
	主函数
	:param bc:
	:param input_data: 可以为 df，也可以为 list
	:param step_1: 处理阶段
	:param step_2: 主函数处理阶段
	:param choice:
	:param clf:
	:param name:
	:return: 处理结果、其他描述信息
	'''
	if choice == "doc":
		all_path = DOC_ALL_PATH
		train_path = DOC_TRAIN_PATH
		test_path = DOC_TEST_PATH
	else:
		all_path = VEC_ALL_PATH
		train_path = VEC_TRAIN_PATH
		test_path = VEC_TEST_PATH
	if step_2 == 1:
		xls2csv()
		return None, None
	elif step_2 == 2:
		out_df = csv_main(bc, input_data, step=step_1, choice=choice)
		out_df.to_csv(all_path, index=False)
		return None, None
	elif step_2 == 3:
		split_dataset(all_path, train_path, test_path)
		return None, None
	elif step_2 == 4:
		train(clf, choice=choice, name=name)
		return None, None
	elif step_2 == 5:
		data, desc = data_main(bc, input_data, step=0, choice=choice)
		result = classific(data, choice=choice, name=name)
		return result[0], desc
