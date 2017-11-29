def read_url(_url):#Return <str>
	import urllib.request
	import random
	import ssl
	import time
	import traceback
	_req = urllib.request.Request(_url) #headers={'User-Agent': 'Smart Boy '+str(random.random())}
	try:
		res = urllib.request.urlopen(_req,context = ssl._create_unverified_context())
		text = res.read().decode("utf-8", "ignore")
		res.close()
		#print(text)
	except:
		traceback.print_exc()
		print("Error in: "+_url)
		time.sleep(5)
		text = read_url(_url)
	return text
	
def get_xpath(html_content,x_path):
	from lxml import etree
	selector=etree.HTML(html_content)
	return selector.xpath(x_path)[0].text

def get_coins(names):
	html = read_url("https://coinmarketcap.com/currencies/views/all/")
	coins = []
	for name in names:
		coin = get_xpath(html,'//*[@id="id-'+ name +'"]/td[5]/a').strip('$')
		coins.append(float(rate)*float(coin))
	return coins

def get_jubi_bitcoin():
	import re
	html = read_url('https://www.jubi.com/coin/btc/order')
	return re.findall(r"(?:\",)(.+?)(?:,)",html)[0]
	

def get_bull_bitcoin():
	import re
	html = read_url('https://www.bullbtc.com/mar/ticker.json?currency=0')
	return re.findall(r"(?:\"priceLast\" : )(.+?)(?:,)",html)[0]
	
def get_time():
	import datetime
	now = datetime.datetime.now()
	return datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
	
def get_rate():
	return get_xpath(read_url("https://finance.yahoo.com/quote/USDCNY%3DX?p=USDCNY%3DX"),'//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')
	
import time
rate = 0
counter = 0
while True:
	if counter == 0:
		rate = float(get_rate())
		counter +=1
	elif counter == 20:
		counter = 0
	else:
		counter+=1
	file=open('btc_new.csv','a')
	cur_time = get_time()
	btc = str(get_coins(["bitcoin"])[0])
	bull = get_bull_bitcoin()
	jubi = get_jubi_bitcoin()
	print(cur_time)
	print(btc)
	print(bull)
	print(jubi)
	file.write(",".join([cur_time,btc,bull,jubi])+'\n')
	file.close()
	time.sleep(30)

