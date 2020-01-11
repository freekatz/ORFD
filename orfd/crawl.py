#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   crawl.py    
@Desc    :   58 同城链接信息解析爬虫模块
@Project :   orfd-platform
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2019/05/29 0:46        the freer      2.1
'''
import requests
import re
import json
from bs4 import BeautifulSoup

## 声明：由于版权保护，故不提供详细注释

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
	
}

def getAjaxData1(jobId, companyId):
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	url = "http://statisticszp.58.com/position/totalcount/?infoId=%s&userId=%s" \
	      % (jobId, companyId)
	resp = requests.get(url=url, headers=headers)
	html = resp.text[9:-2]
	js = json.loads(html)
	applyNum = js["deliveryCount"]
	resumeReadPercent = js["resumeReadPercent"]  # 简历阅读百分比
	positionTotal = js["infoCount"]
	if applyNum == "" or applyNum == None:
		applyNum = 0
	if resumeReadPercent == "-1" or resumeReadPercent == None or resumeReadPercent == -1:
		resumeReadPercent = 0
	
	return applyNum, resumeReadPercent, positionTotal

def getAjaxData2(companyId):
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	url = "http://jianli.58.com/ajax/getefrate/%s" % companyId
	resp = requests.get(url=url, headers=headers)
	html = resp.text
	js = json.loads(html)
	feedbackRation = js["entity"]["efrate"]
	if feedbackRation == "-1" or feedbackRation == None or feedbackRation == -1:
		feedbackRation = 0
	return feedbackRation

def parseJobDetail(jobDetailUrl, jobDetailId, companyId):
	# print(jobDetailUrl)
	# print(jobDetailId)
	jobDetailUrl = jobDetailUrl.replace("https:", "http:")
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	resp = requests.get(url=jobDetailUrl, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	# 职位名字
	title = soup.select_one("span.pos_title").text
	# 子标题，一般为对职位的一些概括或者是说明职位的部分信息，如薪资
	subTitle = soup.select_one("span.pos_name").text
	# 职位薪资
	salary = soup.select_one("span.pos_salary").text
	# 申请人数、反馈率、公司共发布职位数
	applyNum, resumeReadPercent, _ = getAjaxData1(jobDetailId, companyId)
	browserNum = soup.select_one("span.pos_base_browser").text  # 浏览数目
	# 更新时间
	# updateTime = soup.select_one("span.pos_base_update").text.replace(" ", "")
	# 福利列表，类似于：['包住', '加班补助', '饭补']
	welfareItems = [w.text for w in soup.select("span.pos_welfare_item")]
	# welfare = json.dumps({"items": welfareItems})
	welfare = "_".join(welfareItems)
	# 类似于：['招1人', '学历不限', '经验不限']
	conditionItems = [c.text.replace(" ", "") for c in soup.select("span.item_condition")]
	needNum = conditionItems[0]  # 职位需要人数
	# condition = json.dumps({"items": conditionItems[1:]})
	condition = "_".join(conditionItems[1:])
	areaTemp = [a for a in re.split(r" ", soup.select_one("div.pos-area").text)]
	areaItems = []  # 地域信息，很详细
	for at in areaTemp:
		if at != " " and at != "-" and at != "" and at != "查看地图":
			areaItems.append(at)
	# area = json.dumps({"items": areaItems})
	area = "_".join(areaItems)
	# print(area)
	if re.search(r"北京", area):
		jobCity = "bj"
	elif re.search(r"上海", area):
		jobCity = "sh"
	elif re.search(r"广州", area):
		jobCity = "gz"
	elif re.search(r"深圳", area):
		jobCity = "sz"
	else:
		jobCity = "None"
	description = soup.select_one("div.des").text  # 职位描述，一般包括职位要求
	# requirements = soup.select_one("div.requirements").text # 职位要求，一般为空
	InfoList = [
		title, subTitle, salary, applyNum,
		resumeReadPercent, jobCity,
		welfare, condition, description,
		needNum
	]  # 10
	return InfoList

def getCompanyJobTotal(companyId):
	url = "http://qy.58.com/ent/infolist/%s/1" % companyId
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	resp = requests.get(url, headers=headers)
	js = json.loads(resp.text)
	positionTotal = js["data"]["total"]
	return positionTotal

def parseComDetail1(companyBaseUrl, companyId):
	companyBaseUrl = companyBaseUrl.replace("https:", "http:")
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	resp = requests.get(url=companyBaseUrl, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	baseMsg = soup.select_one("div.basicMsg").text
	positionTotal = getCompanyJobTotal(companyId)
	companyName = soup.select_one("a.businessName").text  # 公司名字
	try:
		tradeItems = [t.replace(" ", "") for t in re.search(r"公司行业：(.*?)、(.*?)\n", baseMsg).groups()]
	except:
		tradeItems = ["其他行业"]  # 公司行业
	# companyTrade = json.dumps({"items": tradeItems})
	companyTrade = "_".join(tradeItems)
	# 公司性质：私营、国企等
	companyCharacter = re.sub(r" |\t|\r|\n", "", re.search(r"公司性质：(.*?)\n", baseMsg).groups()[0])
	if companyCharacter == None or companyCharacter == "":
		companyCharacter = "无性质"
	companySize = re.search(r"公司规模：(.*?)人", baseMsg).groups()[0]  # 公司规模
	companyAddr = re.search(r"公司地址：(.*?)查看地图", baseMsg, re.DOTALL).groups()[0]  # 公司地址
	# 公司详情网址，可能和简要网址一样
	companyDetailUrl = re.search(r"企业网址：(.*?)\n", baseMsg).groups()[0]
	companyIntro = soup.select_one("div.compIntro").text.replace(" ", "")  # 公司介绍
	postData = {
		"userName": companyName,
	}
	comJsonUrl = "http://qy.58.com/ajax/getBusinessInfo"
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	cresp = requests.post(url=comJsonUrl, headers=headers, data=postData)
	chtml = cresp.text
	js = json.loads(chtml)
	businessScope = js["businessScope"]  # 经营范围
	companyType = js["companyType"]  # 公司类型：有限责任公司等等
	creditCode = js["creditCode"]  # 统一社会信用代码
	estiblishDate = js["estiblishDate"]  # 成立日期
	if estiblishDate == None or estiblishDate == "":
		estiblishDate = "1800-12-31"
	operatingStatus = js["operatingStatus"]  # 经营状态
	orgNumber = js["orgNumber"]  # 组织机构代码
	regAddress = js["regAddress"]  # 注册地址
	regAuthority = js["regAuthority"]  # 重庆市工商行政管理局南岸区分局
	regCapital = js["regCapital"]  # 注册资本
	teamTime = js["termStart"] + "_" + js["teamEnd"]  # 经营期限
	entUrl = js["entUrl"]  # 天眼查网址
	feedbackRation = getAjaxData2(companyId)
	infoList = [
		positionTotal, companyCharacter,
		feedbackRation, companySize,
		creditCode, operatingStatus, regAddress,
		orgNumber, regCapital,
		companyIntro,
	]  # 10
	return infoList

def parseComDetail2(companyId):
	url = "http://qy.58.com/ent/detail/%s" % companyId
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	resp = requests.get(url=url, headers=headers)
	html = resp.text
	js = json.loads(html)
	detail = js["data"]["entDetail"]
	positionTotal = getCompanyJobTotal(companyId)
	companyName = detail["entName"]  # 公司名字
	companySize = detail["sizeText"]  # 公司行业
	companyIntro = detail["introduction"]
	companyCharacter = detail["typeText"]  # 公司性质：私营、国企等
	if companyCharacter == None or companyCharacter == "":
		companyCharacter = "无性质"
	bussiness = detail["bussiness"]
	regCapital = bussiness["regCapital"]  # 注册资本
	businessScope = bussiness["businessScope"]  # 经营范围
	creditCode = bussiness["creditCode"]  # 统一社会信用代码
	orgNumber = bussiness["orgNumber"]  # 组织机构代码
	regAddress = bussiness["regLocation"]  # 注册地址
	operatingStatus = bussiness["regStatus"]  # 经营状态
	estiblishDate = bussiness["createTime"]  # 成立日期
	if estiblishDate == None:
		estiblishDate = "1800-12-31"
	companyAddr = detail["address"]  # 公司地址
	teamTime = "_"  # 经营期限
	regAuthority = "未知"  # 重庆市工商行政管理局南岸区分局
	companyTrade = "未知"  # 公司行业
	companyType = "未知"  # 公司类型：有限责任公司等等
	entUrl = "未知"  # 天眼查网址
	companyDetailUrl = "未知"  # 公司详情网址，可能和简要网址一样
	feedbackRation = getAjaxData2(companyId)
	infoList = [
		positionTotal, companyCharacter,
		feedbackRation, companySize,
		creditCode, operatingStatus, regAddress,
		orgNumber, regCapital,
		companyIntro,
	]  # 10
	return infoList

def getCompanyBaseUrl(jobDetailUrl):
	jobDetailUrl = jobDetailUrl.replace("https:", "http:")
	#proxy = get_proxy()
	#proxies = {"http": "http://{}".format(proxy)}
	resp = requests.get(url=jobDetailUrl, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	try:
		companyBaseUrl = soup.select_one("div.baseInfo_link").a["href"].replace("https", "http")
	except:
		companyBaseUrl = soup.select_one("a.baseInfo_daipei")["href"].replace("https", "http")
	return companyBaseUrl

def crawl_main(jobDetailUrl):
	companyBaseUrl = getCompanyBaseUrl(jobDetailUrl)
	companyId = re.search(r"(.*)/(\d*)/", companyBaseUrl).groups()[1]
	try:
		comInfoList = parseComDetail1(companyBaseUrl, companyId)
	except:
		try:
			comInfoList = parseComDetail2(companyId)
		except:
			return False
	if comInfoList == []:
		return False
	# 公司信息表
	companyInfoDict = {
		"positionTotal": "-1", "companyCharacter": "",
		"feedbackRation": "-1", "companySize": "",
		"creditCode": "", "operatingStatus": "",
		"regAddress": "", "orgNumber": "", "regCapital": "",
		"companyIntro": "",
	}
	# infoList = [
	# 	positionTotal, companyCharacter,
	# 	feedbackRation, companySize,
	# 	creditCode, operatingStatus, regAddress,
	# 	orgNumber, regCapital,
	# 	companyIntro,
	# ]#10
	companyInfoDict["positionTotal"] = comInfoList[0]
	companyInfoDict["companyCharacter"] = comInfoList[1]
	companyInfoDict["feedbackRation"] = comInfoList[2]
	companyInfoDict["companySize"] = comInfoList[3]
	companyInfoDict["creditCode"] = comInfoList[4]
	companyInfoDict["operatingStatus"] = comInfoList[5]
	companyInfoDict["regAddress"] = comInfoList[6]
	companyInfoDict["orgNumber"] = comInfoList[7]
	companyInfoDict["regCapital"] = comInfoList[8]
	companyInfoDict["companyIntro"] = comInfoList[9]
	
	jobDetailId = re.search(r"(.*)/(\d*)", jobDetailUrl).groups()[1]
	try:
		jobInfoList = parseJobDetail(jobDetailUrl, jobDetailId, companyId)
	except:
		return False
	# 招聘表
	jobInfoDict = {
		"jobTitle": "", "jobSubTitle": "", "jobSalary": "",
		"applyNum": "-1", "resumeReadPercent": "-1",
		"jobWelfare": "", "jobRequirement": "", "jobCity": "",
		"jobDescription": "", "needNumber": "",
	}
	# InfoList = [
	# 	title, subTitle, salary, applyNum,
	# 	resumeReadPercent, jobCity,
	# 	welfare, condition, description,
	# 	needNum
	# ]#11
	jobInfoDict["jobTitle"] = jobInfoList[0]
	jobInfoDict["jobSubTitle"] = jobInfoList[1]
	jobInfoDict["jobSalary"] = jobInfoList[2]
	jobInfoDict["applyNum"] = jobInfoList[3]
	jobInfoDict["resumeReadPercent"] = jobInfoList[4]
	jobInfoDict["jobCity"] = jobInfoList[5]
	jobInfoDict["jobWelfare"] = jobInfoList[6]
	jobInfoDict["jobRequirement"] = jobInfoList[7]
	
	jobInfoDict["jobDescription"] = jobInfoList[8]
	jobInfoDict["needNumber"] = jobInfoList[9]
	
	return jobInfoDict, companyInfoDict

if __name__ == '__main__':
	jurl = "https://bj.58.com/yewu/32094004833208x.shtml?end=end&psid=139368975204303447577397484&entinfo=32094004833208_z&ytdzwdetaildj=0&finalCp=000001240000000000070000000000000000_139368975204303447577397484&tjfrom=pc_list_left_zd__139368975204303447577397484__30794603687084032__zd&iuType=z_2&PGTID=0d30364d-0000-1cdc-5a4b-108a764e30e1&ClickID=4"
	j, c = crawl_main(jurl)
	print(j)
	print(c)