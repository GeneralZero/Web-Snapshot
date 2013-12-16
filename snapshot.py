#!/usr/bin/env python
import base64
import re
from BeautifulSoup import BeautifulSoup
import urllib2

def convert_img2base64(image_file):
	return base64.b64encode(image_file)

def convert_64base2img(binary):
	return base64.decodestring(binary)

def embed_img(site, html):
	arguments =  re.findall(r'<img.*href=[\"\'](.*\..*)[\"\'].*>', html)
	#print arguments
	for x in arguments:
		if x.find('http') != -1: site = '';
		img = get_html(site + x)
		if img:
			html = re.sub(r'<img.*' + x + '.*>[</img>]?', '<img href\"data:image/' + x[-3:] + ';base64,' + convert_img2base64(img) + '\"> </img>', html)

	arguments =  re.findall(r'<img.*href=[\"\'](.*\..*)[\"\'].*>', html)
	#print arguments
	for x in arguments:
		if x.find('http') != -1: site = '';
		img = get_html(site + x)
		if img:
			html = re.sub(r'<img.*' + x + '.*>[</img>]?', '<img href\"data:image/' + x[-3:] + ';base64,' + convert_img2base64(img) + '\"> </img>', html)	

	arguments =  re.findall(r'url\(([^)]*)\)', html)
	#print arguments
	for x in arguments:
		if x.find('http') != -1:
			site = ''
		#print site + x
		img = get_html(site + x)
		if img:
			html = re.sub(r'url\(([^)]*)\)', 'url(data:image/' + x[-3:] + ';base64,' + convert_img2base64(img) + ')', html)

	return html	

def embed_css(site, html):
	arguments =  re.findall(r'<link.*href=[\"\'](.*\.css)[\"\'].*>', html)
	for x in arguments:
		if x.find('http') != -1: site = '';
		css = get_html(site + x)
		if css:
			html = re.sub(r'<link.*' + x + '.*>[</link>]?', '<style type="text/css">\n' + css +'\n</style>', html)
	return html

def embed_js(site, html):
	arguments =  re.findall(r'<script.*src=[\"\'](.*\.js.*)[\"\'].*>[</script>]?', html)
	for x in arguments:
		if x.find('http') != -1:site = '';
		javascript = get_html(site + x)
		if javascript:
			html = re.sub(r'<script.*' + x + '.*>[</script>]?', '<script>\n' + javascript +'\n</script>', html)
	return html

def get_html(url, suburl=None):
	if suburl:
		url += suburl
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	#print opener.open(url)
	return opener.open(url).read()

if __name__ == '__main__':
	site = 'http://news.ycombinator.com/'
	html = get_html(site)

	soup = BeautifulSoup(html)
	for img in soup.findAll('img'):
		img['src'] = base64.b64encode(get_html(site + img['src']))

	for css in soup.findAll('link', {'type': "text/css" }):
		#print css['href']
		css = '<style media="screen" type="text/css">' + get_html(site + css['href']) + '</style>'
		#print css
		#Get images, fonts, and css from css

	for js in soup.findAll('script'):
		if js.has_key('src'):
			js = '<script>' + get_html(site + js['src']) + '</script>'
			print js

	#html = embed_js(site, html) 
	#html = embed_css(site, html) 
	#html = embed_img(site, html)
	#print html
