#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   optimize.py    
@Desc    :   模型优化模块
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:47        the freer      2.1
'''
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn import metrics

from setting import DOC_TRAIN_PATH, COLUMNS, ORIGIN_PATH, DOC_TEST_PATH, \
	DOC_ALL_PATH, VEC_ALL_PATH, VEC_ALL_PATH, VEC_TRAIN_PATH, VEC_TEST_PATH, \
	N_SPLIT

if __name__ == '__main__':
	data = pd.read_csv(DOC_TRAIN_PATH)
	print(data.shape)
	print(pd.value_counts(data.get("768")))
	test = pd.read_csv(DOC_TEST_PATH)
	target = "768"
	# data = pd.read_csv(VEC_TRAIN_PATH)
	# print(data.shape)
	# print(pd.value_counts(data.get("62")))
	# test = pd.read_csv(VEC_TEST_PATH)
	# target = "62"
	# 去掉ID和属性列
	x_columns = [x for x in data.columns if x not in [target]]
	t_columns = [x for x in test.columns if x not in [target]]
	data_x = np.array(data[x_columns])
	data_y = np.array(data[target])
	test_x = np.array(test[t_columns])
	test_y = np.array(test[target])
	
	penaltys = ['l1', 'l2']
	Cs = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
	tuned_parameters = dict(penalty=penaltys, C=Cs)
	
	lr_penalty = LogisticRegression()
	grid = GridSearchCV(lr_penalty, tuned_parameters, cv=5, scoring='neg_log_loss')
	grid.fit(data_x, data_y)
	
	print(grid.cv_results_)
	print(-grid.best_score_)
	print(grid.best_params_)

	# clf = RandomForestClassifier(n_estimators=400)
	# param_gridrf = {
	# 	"min_samples_leaf": np.arange(1, 5, 1)
	# }
	# gridRF = GridSearchCV(estimator = clf,
	#                        param_grid = param_gridrf, scoring='accuracy',cv=N_SPLIT, n_jobs=10)
	# gridRF.fit(data_x,data_y)
	# print('best score is:', str(gridRF.best_score_))
	# print('best params are:', str(gridRF.best_params_))
