#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tests.py    
@Desc    :   
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:49        the freer      2.1
'''
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from bert_serving.client import BertClient

from main import main
from Core.classific import cv, my_test, scoring
from setting import DOC_TRAIN_PATH, DOC_TEST_PATH,\
	VEC_TRAIN_PATH, VEC_TEST_PATH, VEC_LARGE_PATH

def doc():
	data = pd.read_csv(DOC_TRAIN_PATH)
	print(data.shape)
	print(pd.value_counts(data.get("768")))
	test = pd.read_csv(DOC_TEST_PATH)
	target = "768"
	# 去掉ID和属性列
	x_columns = [x for x in data.columns if x not in [target]]
	t_columns = [x for x in test.columns if x not in [target]]
	data_x = np.array(data[x_columns])
	data_y = np.array(data[target])
	test_x = np.array(test[t_columns])
	test_y = np.array(test[target])
	clf = joblib.load("core/models/reg_768_doc.m")
	print("平衡数据集逻辑回归模型交叉验证评估结果：")
	cv(data_x, data_y, clf)
	print("-----------------------------------")
	print("平衡数据集逻辑回归模型测试集评估结果：")
	my_test(test_x, test_y, clf)

def vec():
	data = pd.read_csv(VEC_TRAIN_PATH)
	print("训练集规模：", data.shape)
	print("训练集标签分布：\n", pd.value_counts(data.get("62")))
	test = pd.read_csv(VEC_TEST_PATH)
	print("测试集规模：", test.shape)
	print("测试集标签分布：\n", pd.value_counts(test.get("62")))
	target = "62"
	# 去掉ID和属性列
	x_columns = [x for x in data.columns if x not in [target]]
	t_columns = [x for x in test.columns if x not in [target]]
	data_x = np.array(data[x_columns])
	data_y = np.array(data[target])
	test_x = np.array(test[t_columns])
	test_y = np.array(test[target])
	clf = joblib.load("core/models/rf_62_vec.m")
	print("平衡数据集随机森林模型交叉验证评估结果：")
	cv(data_x, data_y, clf)
	print("-----------------------------------")
	
	print("平衡数据集随机森林模型测试集评估结果：")
	my_test(test_x, test_y, clf)
	print("-----------------------------------")
	
	large = pd.read_csv(VEC_LARGE_PATH)
	print("完全不平衡数据集规模：", large.shape)
	print("完全不平衡数据集标签分布：\n", pd.value_counts(large.get("62")))
	# 去掉ID和属性列
	l_columns = [x for x in large.columns if x not in [target]]
	large_x = np.array(large[l_columns])
	large_y = np.array(large[target])
	my_test(large_x, large_y, clf)
	
def predict():
	bc = BertClient()
	input_data = [' 网络销售', '月薪2万一包食宿一8小时 ', '12000-20000元/月', 511, 80, '包吃_包住_年底双薪', '学历不限_经验不限', 'bj',
	              ' 求职者注意：不要你学历，不要你经验，公司带薪培训.渡过新人期你的收入就会越来越多，只要你肯坚持，肯付出，高薪离你只有一步之遥。月薪过万只是个基本的门槛而已！高大上的办公环境，高级白领级别！公司临近地铁 上班方便【客户资源】不需要自己寻找意向客户，公司都在投大量的广告，成单率极高，轻轻松松月薪上万，我们这种模式是非常容易出单的销售。一个没有经验的人都可以，只要你愿意学习，只要你有一颗上进的心，只要你有想挣钱的心 来这里都能挣到钱，加入我们吧。加油吧！！！！【任职资格】1、年龄18--35岁，品行端正（思维活跃，熟悉用手机与客户沟通者优先）2、有无工作经验均可，会有岗前培训，让你轻松就职，轻松赚得丰厚报酬！【薪资待遇】无责底薪(3000-5000)+提成+日奖金+月奖金+活动奖金。公司根据销售业绩， 阶梯式提成， 3-10%的销售业绩提成，月薪可达8千一2万以上【岗位职责】1、公司提供客户资源，员工开发新客户并维护好客户；2、通过手机与客户进行有效沟通了解客户需求,3、寻找销售机会并完成销售业绩；欢迎渴望成功、喜爱销售的你加入我们的团队。【工作地址】丰台区丰益桥西国贸大厦 ',
	              '招50人', '4', '私营', 1, '50-99人', '91110302MA0073WQXB', '开业', '北京市北京经济技术开发区科创五街38号院3号楼13层1320',
	              'MA0073WQX', '50 万元',
	              '北京健惠恒康生物科技有限公司是一家新兴的健康管理公司，集产品的研发、推广、销售于一体的大型公司。公司以电视、报纸、网络、等多种媒体为推广手段，以计算机信息管理系统、CRM客户挂你系统为辅助工具，与国内多家知名企业良好深度合作，成功建立多媒体的商业立体推广平台。公司各项证件齐全，三证、呼叫中心资格证、卫生许可证、保健品流通许可等，让您放心无忧施展您个人才能\n公司目前业务扩展，高薪招收人才。公司本着一个以人为本原则，给每一个员工一个发展的平台，我们深知公司的发展离不开各位的努力，只要为公司付出努力汗水，福利待遇会一一跟上。公司还有各种奖金和升职制度，我们希望大家以朋友的方式相处，营造一个轻松的工作环境，让你们有足够的空间和信心同公司一起发展下去。\n【企业宗旨】 打造最专业的私人健康管家\n【企业精神】高效、务实、创新、超越、进步\n今天的最好变成明天的最低要求\n【服务理念】 一对一贴心服务，心连心高效沟通！\n【团队文化】永不言弃，拼他个朝朝暮暮；\n你我同在，拼出个无比辉煌！\n【员工工作理念】努力拼搏共奋斗！开心快乐赚大钱！\n【企业发展理念】创新是企业发展的前提；执行是企业的第一生命力；工作效率是企业执行的保障！培训是员工最大的福利！人才培养是企业发展的根本！\n【企业经营理念】公司本着“为企业创造最大商业价值”的指导思想，注重人才培养和团队培养，致力成为客户最专业的私人健康管家。']
	input_data.append("")
	step_1 = 0
	step_2 = 5
	data = input_data
	rf = joblib.load("./core/models/rf_62_vec.m")
	reg = joblib.load("./core/models/reg_768_doc.m")
	vec_proba, desc = main(bc, data, step_1, step_2, "vec", rf, "rf")
	doc_proba, _ = main(bc, data, step_1, step_2, "doc", reg, "reg")
	print("特征向量概率向量：", vec_proba, "文本向量概率向量：", doc_proba)
	score = scoring(proba_v=vec_proba, proba_d=doc_proba)
	print("得分：", score)
	
if __name__ == '__main__':
	print("开始测试特征向量分类模型性能：")
	vec()
	print("开始测试文本向量分类模型性能：")
	doc()
	print("开始测试对输入数据识别：")
	predict()