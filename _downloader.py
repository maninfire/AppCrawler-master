# -*- coding:utf-8 -*-

from urllib import request
from selenium import webdriver
from _googleplayapi import GooglePlayAPI
import urllib, time, requests, re, os, json

def get_apk_download_link(market, data, url):
	if market == 'yingyongbao':
		matcher = re.findall('data-apkurl=".*?"', data)
		if len(matcher): return matcher[0].replace('data-apkurl="', "").replace('"', "")
		
	elif market == 'baidu':
		matcher = re.findall('<span class="one-setup-btn".*?data_url=".*?"', data, re.S)
		if len(matcher): return re.subn('<span class="one-setup-btn".*?data_url="', "", matcher[0].replace("\r", "").replace("\n", ""))[0].replace('"', "")
		
	elif market == '360':
		matcher = re.findall('url=.*?.apk" data-sid=', data)
		if len(matcher): return matcher[0].replace('url=', "").replace('" data-sid=', "")
		
	elif market == 'googleplay':
		return url
		
	elif market == 'huawei':
		matcher = re.findall('dlurl=".*?"', data)
		if len(matcher): return matcher[0].replace('dlurl="', "").replace('"', "")
		
	elif market == 'xiaomi':
		matcher = re.findall('<div class="app-info-down"><a href=".*?"', data)
		if len(matcher): return 'http://app.mi.com'+matcher[0].replace('<div class="app-info-down"><a href="', "").replace('"', "")
		
	elif market == 'wandoujia':
		return url+"/download"
		
	elif market == 'hiapk':
		matcher = re.findall('<a href="/appdown/.*?" class="link_btn"', data)
		if len(matcher): return 'http://apk.hiapk.com'+matcher[0].replace('<a href="', "").replace('" class="link_btn"', "")
		
	elif market == 'anzhi':
		matcher = re.findall('<a href="#" onclick="opendown\([0-9]+\);"', data)
		if len(matcher): return 'http://www.anzhi.com/dl_app.php?s='+matcher[0].replace('<a href="#" onclick="opendown(', "").replace(');"', "")+'&n=5'
		
	elif market == '91':
		matcher = re.findall(' href=".*?">下载到电脑', data)
		if len(matcher): return 'http://apk.91.com'+matcher[0].replace(' href="', "").replace('">下载到电脑', "")

	elif market == 'oppo':
		matcher = re.findall('<a class="detail_down" onclick="detailInfoDownload\([0-9]+\)">下载到电脑</a>', data)
		if len(matcher): return 'http://store.oppomobile.com/product/download.html?id='+matcher[0].replace('<a class="detail_down" onclick="detailInfoDownload(', "").replace(')">下载到电脑</a>', "")+'&from=0_0'

	elif market == 'pp':
		matcher = re.findall('appdownurl=".*?".*?data.*?">立即下载</a>', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'sogou':
		return "http://zhushou.sogou.com/apps/download.html?appid="+url.split('/')[-1].replace(".html", "")

	elif market == 'gfan':
		matcher = re.findall('<a href=".*?".*?title="下载到电脑"><i class="bt-ico3"></i>下载到电脑</a>', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'meizu':
		matcher = re.findall('data-appid="[0-9]+', data)
		if '?' in url and len(matcher): return url.split('?')[0].replace('detail', 'download.json?app_id=')+matcher[0].replace('data-appid="', "")

	elif market == 'sina':
		matcher = re.findall('<a href=".*?" class="avBtn avBtn-down">立即下载</a>', data)
		if len(matcher): return 'http://app.sina.com.cn'+matcher[0].split('"')[1]

	elif market == 'dcn':
		matcher = re.findall('onclick="Adapt.downPush\(\'.*?\'.*?立即下载</a></li>', data)
		if len(matcher): return matcher[0].split("'")[1]

	elif market == 'liqucn':
		matcher = re.findall('<a href=".*?" target=".*?">下载到电脑</a>', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'appchina':
		matcher = re.findall('onclick="freeDownload\(this,&#39;.*?;\)">免费下载</a>', data)
		if len(matcher): return matcher[0].split(';')[1]

	elif market == '10086':
		matcher = re.findall('<span></span></div><a href=".*?" class="mj_xzdbd"', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'lenovo':
		matcher = re.findall('<a href=".*?" data-pkgname=".*?".*?<span>下载APK文件', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'zol':
		matcher = re.findall('<a id="down_main_android".*?corpsoft\(\'.*?\'', data)
		if len(matcher): return matcher[0].split("'")[-2]

	elif market == 'nduo':
		matcher = re.findall('<a href=".*?".*?><span></span>立即下载</a>', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'cnmo':
		matcher = re.findall('appLocalDownloadUrl=".*?"', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'pconline':
		matcher = re.findall('<a href=".*?\.apk" rel="nofollow" class="btn dl-btn"', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'appcool':
		matcher = re.findall('<a href=".*?" class="det-butn-1"></a>', data)
		if len(matcher): return matcher[0].split('"')[1]

	return ""
	
def get_icon_download_link(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-icon">.*?src=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
	
	elif market == 'baidu':
		matcher = re.findall('<div class="app-pic">.*?=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == '360':
		matcher = re.findall('<dt>.*?<img src=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == 'googleplay':
		matcher = re.findall('<img class="cover-image" src=".*?"', data)
		if len(matcher): return 'https:'+matcher[0].split('"')[-2]
		
	elif market == 'huawei':
		matcher = re.findall('img class="app-ico" lazyload=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == 'xiaomi':
		matcher = re.findall('<img class="yellow-flower" src=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == 'wandoujia':
		matcher = re.findall('<img src=".*?" itemprop="image" width="110" height="110"', data)
		if len(matcher): return matcher[0].split('"')[-8]
		
	elif market == 'hiapk':
		matcher = re.findall('<img.*?src=".*?".*?ICON"', data)
		if len(matcher):
			matcher = re.findall('src=".*?"', matcher[0])
			if len(matcher): return matcher[0].split('"')[-2]
			
	elif market == 'anzhi':
		matcher = re.findall('var ICON="http://.*?";', data)
		if len(matcher): return matcher[0].split('"')[-2]
	
	elif market == '91':
		matcher = re.findall('<img src=".*?" alt=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-4]

	elif market == 'oppo':
		matcher = re.findall('<img class=".*?" dataimg="http://.*?" />', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == 'pp':
		matcher = re.findall('<div class="detail-header clearfix"><div class="app-icon"><img src=".*?".*?</div>', data)
		if len(matcher): return matcher[0].split('"')[5]

	elif market == 'sogou':
		matcher = re.findall('<img class="icon" width="[0-9]+" height="[0-9]+" src=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == 'gfan':
		matcher = re.findall('<img class="app-view png" src=".*?" alt=".*?"/>', data)
		if len(matcher): return matcher[0].split('"')[-4]

	elif market == 'meizu':
		matcher = re.findall('<img class="app_img" src=".*?">\n', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == 'sina':
		matcher = re.findall('<div class="avIcon"><img src=".*?".*?</div>', data)
		if len(matcher): return matcher[0].split('"')[3]

	elif market == 'dcn':
		matcher = re.findall('<img src=".*?".*?class="de-app-icon">', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'liqucn':
		matcher = re.findall('<img src=".*?" />\n.*?<h1>', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'appchina':
		matcher = re.findall('<img class="Content_Icon".*?title=".*?" src=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == '10086':
		matcher = re.findall('<img id="appicon" src=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == 'lenovo':
		matcher = re.findall('<img src=".*?" alt=".*?"><i', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'zol':
		matcher = re.findall('<img src=".*?".*?><i class="marsk"></i>', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'nduo':
		matcher = re.findall('<img src=".*?" width="120" height="120"', data)
		if len(matcher): return matcher[0].split('"')[1]

	elif market == 'cnmo':
		matcher = re.findall('<img width="80" height="80" src=".*?">', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == 'pconline':
		matcher = re.findall('<img width="80" height="80" alt=".*?" src=".*?">\r?\n', data)
		if len(matcher): return matcher[0].split('"')[-2]

	elif market == 'appcool':
		matcher = re.findall('<img src=".*?" original=".*?" width="72" height="72" />', data)
		if len(matcher): return matcher[0].split('"')[3]
		
	return ""

def download_apk(market, url, apkfile, config):

	#Windows
	phantomjs_execute_path = r'D:\Users\Programs\phantomjs\bin\phantomjs.exe'

	#Linux
	#phantomjs_execute_path = '/usr/lib/phantomjs/phantomjs'

	if market == 'googleplay':
		if not len(url): return False
		packagename = url.split("=")[1]
		for i in range(10):
			try:
				api = GooglePlayAPI(config['ANDROID_ID'])
				api.login(config['GOOGLE_LOGIN'], config['GOOGLE_PASSWORD'], packagename)
				m = api.details(packagename)
				doc = m.docV2
				vc = doc.details.appDetails.versionCode
				ot = doc.offer[0].offerType
				if api.download(packagename, vc, ot, apkfile): return True
			except:
				continue

	elif market == 'sogou':
		if not len(url): return False
		for i in range(10):
			try:
				web = requests.get(url, stream=True, timeout=30)
				content = ""
				for chunk in web.iter_content(chunk_size=204800):
					if chunk:
						content += chunk.decode()
				matcher = re.findall('"file_url":".*?"', content)
				if len(matcher):
					file_url = matcher[0].replace('"file_url":"', "").replace('"', "").replace('\\', "")
					web = requests.get(file_url, stream=True, timeout=30)
					with open(apkfile, 'wb') as fout:
						for chunk in web.iter_content(chunk_size=204800):
							if chunk:
								fout.write(chunk)
								fout.flush()
					fout.close()
					return True
				else:
					continue
			except:
				continue

	elif market == 'gfan':
		if not len(url): return False
		if not 'apk=' in url: return False
		referer = 'http://apk.gfan.com/Product/App'+url.split('=')[-1]+'.html'
		headers = {'Referer': referer}
		for i in range(10):
			try:
				urlnew = url
				web = requests.get(urlnew, stream=True, timeout=30, headers=headers)
				j = 0
				while web.status_code == 302 and j <= 4:
					j += 1
					if 'Location' in web.headers:
						urlnew = web.headers['Location']
						web = requests.get(urlnew, stream=True, timeout=30, headers=headers)
					else:
						break
				if web.status_code == 200:
					with open(apkfile, 'wb') as fout:
						for chunk in web.iter_content(chunk_size=204800):
							if chunk:
								fout.write(chunk)
								fout.flush()
					fout.close()
					return True
			except:
				continue

	elif market == 'meizu':
		if not len(url): return False
		for i in range(10):
			try:
				if i % 2 == 0: urlnew = url.replace('/games/', '/apps/')
				else: urlnew = url.replace('/apps/', '/games/')
				web = requests.get(urlnew, stream=True, timeout=30)
				content = ""
				for chunk in web.iter_content(chunk_size=204800):
					if chunk:
						content += chunk.decode()
				matcher = re.findall('"downloadUrl":".*?"', content)
				if len(matcher):
					file_url = matcher[0].replace('"downloadUrl":', "").replace('"', "").replace('\\', "")
					web = requests.get(file_url, stream=True, timeout=30)
					with open(apkfile, 'wb') as fout:
						for chunk in web.iter_content(chunk_size=204800):
							if chunk:
								fout.write(chunk)
								fout.flush()
					fout.close()
					return True
				else:
					continue
			except:
				continue
				
	elif market == 'cnmo':
		if not len(url): return False
		for i in range(10):
			try:
				urlnew = os.popen(phantomjs_execute_path+" _location.js "+url).read().split('\n')[-2].replace('\r', "")
				web = requests.get(urlnew, stream=True, timeout=30)
				with open(apkfile, 'wb') as fout:
					for chunk in web.iter_content(chunk_size=204800):
						if chunk:
							fout.write(chunk)
							fout.flush()
				fout.close()
				return True
			except:
				continue

	else:
		if not len(url): return False
		for i in range(10):
			try:
				web = requests.get(url, stream=True, timeout=30)
				with open(apkfile, 'wb') as fout:
					for chunk in web.iter_content(chunk_size=204800):
						if chunk:
							fout.write(chunk)
							fout.flush()
				fout.close()
				return True
			except:
				continue
		
	return False
	
def download_icon(market, url, pngfile):
	if not len(url):
		return False
	else:
		for i in range(10):
			try:
				web = requests.get(url, stream=True, timeout=30)
				with open(pngfile, 'wb') as fout:
					for chunk in web.iter_content(chunk_size=204800):
						if chunk:
							fout.write(chunk)
							fout.flush()
				fout.close()
				return True
			except:
				continue
	return False

if __name__ == '__main__':
	config = {
		'ANDROID_ID': "",
		'GOOGLE_LOGIN': "",
		'GOOGLE_PASSWORD': ""
	}
	try:
		if os.path.isfile("config.json"):
			with open("config.json") as jsonfile:
				config_dict = json.load(jsonfile)
			for key in config.keys():
				if key in config_dict:
					config[key] = config_dict[key]
			print("读取Config成功")
		else:
			print("Config不存在")
			exit()
	except:
		print("读取Config失败")
		exit()
	if os.path.isfile("Google_Play_Download_List.txt"):
		apk_list = open('Google_Play_Download_List.txt', 'r').read().replace('\r', "").split("\n")
		print("读取下载列表成功")
		fout = open('Google_Play_Download.log', 'w')
		for apk in apk_list:
			if len(apk):
				url = 'https://play.google.com/store/apps/details?id='+apk
				if not os.path.exists('Google_Play_Download'):
					os.makedirs('Google_Play_Download')
				success = download_apk('googleplay', url, 'Google_Play_Download/'+apk+'.apk', config)
				if success:
					print('下载成功 '+apk)
					fout.write('Success '+apk+'\n')
				else:
					print('下载失败 '+apk)
					fout.write('Failed '+apk+'\n')
				fout.flush()
		fout.close()
	else:
		print("下载列表不存在")
		exit()
