#!/usr/bin/env python
import base64
import re
import urllib2

def convert_img2base64(image_file):
	return base64.b64encode(image_file.read())

def convert_64base2img(binary):
	return base64.decodestring(binary)

def embed_img(site, html):
	arguments =  re.findall(r'<img.*href=[\"\'](.*\..*)[\"\'].*>', html)
	print arguments
	for x in arguments:
		if x.find('http') != -1:
			site = ''
		img = get_html(site + x)
		if img:
			html = re.sub(r'<img.*' + x + '.*>[</img>]?', '' + convert_img2base64(img) + '', html)

	arguments =  re.findall(r'<img.*href=[\"\'](.*\..*)[\"\'].*>', html)
	print arguments
	for x in arguments:
		if x.find('http') != -1:
			site = ''
		img = get_html(site + x)
		if img:
			html = re.sub(r'<img.*' + x + '.*>[</img>]?', '' + convert_img2base64(img) + '', html)	
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

def get_html(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	return opener.open(url).read()

if __name__ == '__main__':
	site = 'http://localhost/'
	html = get_html(site)

	html = embed_js(site, html) 
	html = embed_css(site, html) 
	print html
