#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   feature.py    
@Desc    :   特征工程后续工作模块，此模块在2.1版本中去除
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:43        the freer      2.1
'''
import pandas as pd
import numpy as np
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.externals import joblib

def feature_main(ori_vec, step, pca_path, pca_number):
	'''
	对输入特征向量或者文本向量进行归一标准正则以及特征提取与选择
	由于本项目在具体实施此过程取得的效果不佳，故选择去除此模块
	:param ori_vec: 原始向量
	:param step: 当前处于的处理阶段：1-归一、2-标准、3-正则、4-提取、5-选择
				 输入 step 会默认继续完成所有后续处理。
	:param pca_path: 训练的PCA模型路径
	:param pca_number: PCA 提取特征数目
	:return: 处理好的向量，以及一个按照向量 shape 初始化的 pandas DataFrame 对象
	'''
	if step <= 1:
		## 归一化
		minMax = MinMaxScaler(feature_range=(0, 1))
		min_vec = minMax.fit_transform(ori_vec)
	else:
		min_vec = ori_vec
	if step <= 2:
		## 标准化
		standard = StandardScaler()
		stand_vec = standard.fit_transform(min_vec)
	else:
		stand_vec = min_vec
	if step <= 3:
		## 正则化
		normal = Normalizer(norm='l1')
		normal_vec = normal.fit_transform(stand_vec)
	else:
		normal_vec = stand_vec
	if step <= 4:
		## 特征提取
		try:
			pca = joblib.load(pca_path)
			pca_vec = pca.transform(normal_vec)
			print("pca found!!")
		except:
			pca = PCA(n_components=pca_number)
			pca_vec = pca.fit_transform(normal_vec)
			joblib.dump(pca, pca_path)
	else:
		pca_vec = normal_vec
	if step <= 5:
		X = pca_vec
		# 特征选择，已去除
		# # 去掉ID和属性列
		# x_columns = [str(x) for x in range(len(pca_vec[0])) if x not in [LABEL]]
		# # x_columns = train_data.columns[:-1]
		# X_ = pd.DataFrame(pca_vec, columns=x_columns)
		# y = labels
		# selected_feat_names = set()
		# # print(selected_feat_names)
		# # for i in range(10):  # 这里我们进行十次循环取交集
		# # 	tmp = set()
		# rfc = RandomForestClassifier(n_jobs=-1)
		# if flag == 1:
		# 	rfc.fit(X_[:-1], y)
		# else:
		# 	rfc.fit(X_, y)
		# importances = rfc.feature_importances_
		# indices = np.argsort(importances)[::-1]  # 降序排列
		# for f in range(X_.shape[1]):
		# 	if f < FEATURE_SELECT_NUMBER:  # 选出前 n 个重要的特征
		# 		selected_feat_names.add(X_.columns[indices[f]])
		# 		# print("%2d) %-*s %f" % (f + 1, 30, X_.columns[indices[f]], importances[indices[f]]))
		# 	else:
		# 		break
		# 	# if len(list(selected_feat_names)) == 0:
		# 	# 	selected_feat_names = tmp
		# 	# else:
		# 	# 	selected_feat_names = tmp & selected_feat_names
		# print(len(selected_feat_names), "features are selected")
		# # print(selected_feat_names)
		# X = []
		# for vec in np.array(X_):
		# 	X.append([vec[int(f_name)] for f_name in selected_feat_names])
	else:
		X = pca_vec
	out_df = pd.DataFrame(columns=[str(i) for i in range(len(X[0]) + 1)])
	return X, out_df