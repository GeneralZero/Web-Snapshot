#!/usr/bin/env python
from base64 import b64encode, decodestring
from sys import argv
import optparse
from urlparse import urlparse, urljoin
from BeautifulSoup import BeautifulSoup
import urllib2

def convert_img2base64(image_file):
	return base64.b64encode(image_file)

def convert_64base2img(binary):
	return base64.decodestring(binary)

def get_url(url, suburl=None):
	if suburl:
		url2 = urlparse(suburl)
		if url2.netloc == '':
			return urljoin(url, suburl)
		elif url2.scheme == '':
			return 'http://' + ''.join(url2[1:])
		else:
			return url2.geturl()
	return url

def get_html(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	try:
		#print url
		test = opener.open(url)
		content = test.info().type
		#print content
		return content, test.read()
	except urllib2.HTTPError as e:
		print "Could not get ", e, url
		return ["",""]

if __name__ == '__main__':
	if len(argv) < 2:
		print argv[0] + ": URL [outputfile]"
	else:
		site = argv[1]
		#Get Base Url for local includes
		url = urlparse(site)
		if url.scheme == '':
			url = urlparse('http://' +  ''.join(url[1:]))
		base_url = url.scheme + "://" +  url.netloc
		#print base_url

		#Get html of page
		_, html = get_html(get_url(url.geturl()))
		soup = BeautifulSoup(html)

		#Convert img to base64
		for img in soup.findAll('img'):
			if img.has_key('src'):
				_, img_data = get_html(get_url(base_url, img['src']))
				#print img_data[0]
				if img_data in ['image/jpeg', 'image/gif', 'image/png']:
					img['src'] =  'data:' + img_data[0] + ';base64,' + b64encode(img_data[1])

		#Embed CSS in page
		for css in soup.findAll('link', {'type': "text/css" }):
			if css.has_key('href'):
				#print css['href']
				_, data = get_html(get_url(base_url, css['href']))
				css = '<style media="screen" type="text/css">' + data + '</style>'
				#print css
				#Get images, fonts, and css from css

		#Embed JS in page
		for js in soup.findAll('script'):
			#print js
			if js.has_key('src'):
				_, data = get_html(get_url(base_url, js['src']))
				js = '<script>' + data+ '</script>'
		if len(argv) > 2:
			url_file = open(argv[2], 'w')
			url_file.write(html)
		else:
			print html