def read_url(_url):#Return <str>
	import urllib.request
	import random
	import ssl
	import time
	import traceback
	import datetime
	now = datetime.datetime.now()
	_req = urllib.request.Request(_url,headers={'User-Agent': 'Smart Boy '+str(random.random())})
	try:
		res = urllib.request.urlopen(_req,context = ssl._create_unverified_context(),timeout=1)
		text = res.read().decode("utf-8", "ignore")
		res.close()
		#print(text)
		print(str(datetime.datetime.now() - now) + "\t"+ _url)
	except:
		#traceback.print_exc()
		print("Error in: "+_url)
		time.sleep(5)
		text = read_url(_url)
	return text
	
def get_xpath(html_content,x_path):
	from lxml import etree
	selector=etree.HTML(html_content)
	return selector.xpath(x_path)[0].text

def get_coins(names): #float
	global rate
	html = read_url("https://coinmarketcap.com/currencies/views/all/")
	coins = []
	for name in names:
		coin = get_xpath(html,'//*[@id="id-'+ name +'"]/td[5]/a').strip('$')
		coins.append(round(float(rate)*float(coin),6))
		percent_1.append(get_xpath(html,'//*[@id="id-'+ name +'"]/td[8]'))
		percent_2.append(get_xpath(html,'//*[@id="id-'+ name +'"]/td[9]'))
		percent_3.append(get_xpath(html,'//*[@id="id-'+ name +'"]/td[10]'))
		#[8] 1h [9]24h [10]7d
	return coins

def get_jubi_coins(names): #str 不可用
	import re
	coins = []
	html = read_url('https://www.jubi.com/coin/trades')
	for name in names:
		coins.append(re.findall(r'(?:"'+ name + '":[".+?",).+?(?:,)',html)[0])
	return coins
	
def get_time():
	import datetime
	now = datetime.datetime.now()
	return datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
	
def get_rate():
	#//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()
	from lxml import etree
	html_content = read_url("https://finance.yahoo.com/quote/USDCNY%3DX?p=USDCNY%3DX")
	x_path = '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]'
	selector=etree.HTML(html_content)
	return selector.xpath(x_path)[0].xpath('string(.)')
	
import time
coins = ["bitcoin","bitcoin-cash","ethereum","litecoin","ethereum-classic","neo","lisk","asch","bitshares","dogecoin"]
jubi_coins = ["btc","bcc","eth","ltc","etc","ans","lsk","xas","bts","doge"]
rate = 6.6695
counter = 0
interval = 60
while True:
	import datetime
	now = datetime.datetime.now()
	percent_1 = []
	percent_2 = []
	percent_3 = []
	
	if counter%10 == 0:
		newrate = float(get_rate())
		print("######")
		print("last rate: "+str(rate))
		rate = newrate
		print("current rate: "+str(rate))
		print("######")
	counter+=1
	
	prices = get_coins(coins)
	jubi_prices = get_jubi_coins(jubi_coins)
	cur_time = get_time()
	file=open('all v1.2.csv','a')
	file.write(cur_time+",")
	print("["+str(counter)+"]",end=" ")
	
	print(cur_time)
	for i in range(len(coins)):
		print("(%6s)(%6s)(%6s)%-16s%-12s%-10s"%(percent_1[i],percent_2[i],percent_3[i],coins[i],str(prices[i]),jubi_prices[i]),end='')
		marker_rate = (prices[i]/float(jubi_prices[i])-1)*100
		if marker_rate>5 or marker_rate<-5:
			print("!%.2f%%"%(marker_rate))
		else:
			print("%.2f%%"%(marker_rate))
		#file.write(str(prices[i])+","+str(jubi_prices[i])+",")
	file.write("\n")
	file.close()
	_time = (datetime.datetime.now() - now).seconds
	print("time = " + _time + "s")
	sleep_time = interval - _time
	if(sleep_time>0):
		print("sleeping... " + sleep_time +"s")
		time.sleep(sleep_time)