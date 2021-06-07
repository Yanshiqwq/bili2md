#!/usr/bin/python
# coding=utf-8

# 引入库
try:
	import logging, sys
except ModuleNotFoundError as e:
	print("")
	print("    #==================================#")
	print("    |   bili2md v1.0 By @延时qwq       |")
	print("    #==================================#")
	print("")
	print("需要的库: sys, urllib3, logging, html2text, bs4")
	print("错误信息: " + str(e))
	sys.exit()
else:
	try:
		level = sys.argv[2]
		level = level.upper()
		eval("logging.basicConfig(level = logging." + level + ",format = '[PID #%(process)d] [%(levelname)s] %(message)s')")
	except IndexError:
		logging.basicConfig(level = logging.INFO,format = '[PID #%(process)d] [%(levelname)s] %(message)s')
	logger = logging.getLogger(__name__)
try:
	import urllib3
	import html2text as h2t
	from bs4 import BeautifulSoup as bs4
except ModuleNotFoundError as e:
	logging.info("")
	logging.info("    #==================================#")
	logging.info("    |   bili2md v1.0 By @延时qwq       |")
	logging.info("    #==================================#")
	logging.info("")
	logging.error("需要的库: sys, urllib3, logging, html2text, bs4")
	logging.error("错误信息: " + str(e))
	sys.exit()

# 初始化
text_maker = h2t.HTML2Text()
http = urllib3.PoolManager()
logging.debug("")
logging.debug("    #==================================#")
logging.debug("    |   bili2md v1.0 By @延时qwq       |")
logging.debug("    #==================================#")
logging.debug("")
try:
	if sys.argv[1] == "--help" or sys.argv[1] == "/help" or sys.argv[1] == "-?" or sys.argv[1] == "/?" or sys.argv[1] == "-h" or sys.argv[1] == "/h":
		logging.info("bili2md - 把B站专栏转换成Markdown")
		logging.info("用法: python bili2md.py [cv号] <日志级别>")
		sys.exit()
except IndexError:
	logging.info("bili2md - 把B站专栏转换成Markdown")
	logging.info("用法: python bili2md.py [cv号] <日志级别>")
	logging.error("请输入cv号!")
	sys.exit()

# 下载页面
try:
	http_req = http.request('GET', 'https://www.bilibili.com/read/' + sys.argv[1])
except IndexError:
	logging.info("bili2md - 把B站专栏转换成Markdown")
	logging.info("用法: python bili2md.py [cv号] <日志级别>")
	logging.error("请输入cv号!")
	sys.exit()
if http_req.status != 200:
	logging.error("页面读取失败!请检查你的输入.")
	sys.exit()

# 解析页面
data = http_req.data
file_decode = bs4(data,'lxml')
body = file_decode.html.body
text = ""
try:
	for line in body.find('div', class_='page-container').find('div', class_='article-holder').children:
		text = text + str(line)
except AttributeError:
	logging.error("页面解析失败!请检查cv号是否有误.")
	sys.exit()
	
# 转换页面
markdown = text_maker.handle(text)

# 输出结果
print(markdown)

# with open("./" + sys.argv[1] + ".md", 'w') as f:
#	f.write(markdown)