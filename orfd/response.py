#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   response.py    
@Desc    :   浏览器请求响应模块
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:48        the freer      2.1
'''
import json
from flask import Flask
from flask import render_template, request, make_response
from bert_serving.client import BertClient
import logging
import time

from crawl import crawl_main
from Core.classific import scoring
from main import main


from setting import DATE_FORMAT, LOG_FORMAT, LOG_DIR_DEBUG

app = Flask(__name__)
config = {
	"bc": BertClient(),
	"input_data": [],
	"step_1": 0,
	"step_2": 5,
	"choice": "",
	"name": ""
}

# 日志功能
def logger(log):
	date = time.strftime("%Y-%m-%d",time.localtime()).replace('\\', '-').replace('/', '-')
	fp = logging.FileHandler(LOG_DIR_DEBUG + str(date) + '.txt', encoding='utf-8')
	fs = logging.StreamHandler()
	logging.basicConfig(
		level=logging.DEBUG,
		format=LOG_FORMAT,
		datefmt=DATE_FORMAT,
		handlers=[fp, fs]
	)
	logging.info(log)

def get_data(jobDretailUrl):
	'''
	获取招聘页面信息
	:param jobDretailUrl: 招聘详情页
	:return: data
	'''
	jobDict, compDict = crawl_main(jobDretailUrl)
	data = []
	for key in jobDict.keys():
		data.append(jobDict[key])
	for key in compDict:
		data.append(compDict[key])
	data.append("")
	return data

@app.route("/query/", methods=['GET'])
def query():
	'''
	页面查询处理逻辑
	:return:
	'''
	if request.method == 'GET' and request.args.get("detail_url"):
		url = request.args.get("detail_url")
		data = get_data(url)
		config["input_data"] = data
		config["choice"] = "vec"
		config["name"] = "rf"
		vec_proba, desc = main(**config)
		
		config["choice"] = "doc"
		config["name"] = "reg"
		doc_proba, _ = main(**config)
		score = scoring(proba_v=vec_proba, proba_d=doc_proba)
		welfare = {
			"contact": str(desc[0])
		}
		# print("welfare: ", welfare)
		recruit = {
			"origin_length": desc[1][0], "process_length": desc[1][1], "content": desc[1][2],
			"requirement": desc[1][3], "salary": desc[1][4], "welfare": desc[1][5],
			"work_time": desc[1][6], "contact": desc[1][7], "email": desc[1][8], "url": desc[1][9]
		}
		# print("recruit: ", recruit)
		company = {
			"origin_length": desc[2][0], "job_content": desc[2][1], "requirement": desc[2][2],
			"salary": desc[2][3], "welfare": desc[2][4], "work_time": desc[2][5]
		}
		# print("company: ", company)
		analysis = [
			welfare,
			recruit,
			company
		]
		response = {
			"score": str(score),
			"vec_result": str(vec_proba[1]),
			"doc_result": str(doc_proba[1]),
			"analysis_result": analysis
		}
		response = json.dumps(response)
		log = "\n---------------------\n" + url + "\n== >" + response + "\n---------------------"
		logger(log)
		rst = make_response(response)
		rst.headers['Access-Control-Allow-Origin'] = '*'
		return rst, 201
	return render_template("error.html")

def run():
	app.run(host='127.0.0.1')