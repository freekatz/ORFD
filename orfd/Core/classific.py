#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   classific.py    
@Desc    :   模型分类模块：模型训练评估及使用
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:41        the freer      2.1
'''
import time
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.externals import joblib
from sklearn.metrics.scorer import make_scorer

from setting import DOC_TRAIN_PATH, DOC_MODEL_NAME, VEC_MODEL_NAME, \
	VEC_TRAIN_PATH, N_SPLIT, MODEL_DIR, VEC_PRECISION, DOC_PRECISION,\
	SCORING

def classific(input_data, choice, name):
	'''
	输入特征向量或文本向量，反馈分类结果
	:param input_data: 输入的特征向量或者文本向量
	:param choice: 输入选项：doc-文本向量分类、vec-特征向量分类
	:param name: 模型名称（简称）：rf-随机森林、reg-逻辑回归
	:return: 分类结果向量：形如 [1]
	'''
	if choice == "doc":
		model = DOC_MODEL_NAME # doc.m
		length = '768'
	else:
		model = VEC_MODEL_NAME # vec.m
		length = '62'
	# MODEL_DIR + name + "_" + length + "_" + model，形如：./core/models/rf_62_vec.m
	clf = joblib.load(MODEL_DIR + name + "_" + length + "_" + model)
	# result = clf.predict(input_data)
	proba = clf.predict_proba(input_data)
	return proba

def scoring(proba_v, proba_d):
	'''
	对预测结果计算得分
	:param proba_*: 分类结果的概率，形如[0.59789263 0.40210737]则结果为0
	:return: score
	'''
	score = np.array([p*VEC_PRECISION for p in proba_v])\
	        +np.array([p*DOC_PRECISION for p in proba_d])
	return abs(score[1]/SCORING)*100

def train(clf, choice, name):
	'''
	对输入的分类器模型进行训练，并将模型保存
	:param clf: 输入的分类器模型
	:param choice: 输入选项：doc-文本向量分类、vec-特征向量分类
	:param name: 模型名称（简称）：rf-随机森林、reg-逻辑回归
	:return: 训练好的模型
	'''
	if choice == "doc":
		path = DOC_TRAIN_PATH
		model = DOC_MODEL_NAME
		Label = "768"
	else:
		path = VEC_TRAIN_PATH
		model = VEC_MODEL_NAME
		Label = "62"
	fit = pd.read_csv(path)
	# 去掉ID和属性列
	x_columns = [x for x in fit.columns if x not in [Label]]
	fit_x = np.array(fit[x_columns])
	fit_y = np.array(fit[Label])
	clf.fit(fit_x, fit_y)
	joblib.dump(clf, MODEL_DIR + name + "_" + Label + "_" + model)
	return clf

def cv(data_x, data_y, clf):
	'''
	对输入模型进行 K-Folder 交叉验证，返回验证结果
	:param data_x: 训练向量
	:param data_y: 训练标签
	:param clf: 分类器模型
	:return: 验证结果：各种评估得分
	'''
	scoring = {
		'precision_macro': 'precision_macro',
		'recall_macro': make_scorer(metrics.recall_score, average='macro'),
		'roc_auc_macro': make_scorer(metrics.roc_auc_score, average='macro'),
		'f1_macro': make_scorer(metrics.f1_score, average="macro"),
		'accuracy': make_scorer(metrics.accuracy_score),
	}
	cv_results = cross_validate(clf, data_x, data_y, scoring=scoring,
	                            n_jobs=4, cv=N_SPLIT, return_train_score=False, )
	for key in cv_results.keys():
		print(f"{key}:\t{np.mean(cv_results[key])}")
		# print("----------")
	return cv_results

def my_test(test_x, test_y, clf):
	start = time.time()
	y_pred = clf.predict(test_x)
	end = time.time()
	print("运行时间:%.5f秒" % (end - start))
	s1 = metrics.recall_score(test_y, y_pred)
	s2 = metrics.roc_auc_score(test_y, y_pred)
	s3 = metrics.f1_score(test_y, y_pred)
	s4 = metrics.accuracy_score(test_y, y_pred)
	s5 = metrics.precision_score(test_y, y_pred)
	s6 = metrics.confusion_matrix(test_y, y_pred)
	tn, fp, fn, tp = s6.ravel()
	print(f"recall: {s1}")
	print(f"roc_auc: {s2}")
	print(f"f1: {s3}")
	print(f"准确率: {s4}")
	print(f"精确度: {s5}")
	print(f"混淆矩阵: {s6}")
	print("tn, fp, fn, tp = ", (tn, fp, fn, tp))