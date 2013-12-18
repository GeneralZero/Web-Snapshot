#!/usr/bin/env python
from base64 import b64encode, decodestring
from sys import argv
import optparse
from urlparse import urlparse, urljoin
from BeautifulSoup import BeautifulSoup
import urllib2
import re

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
		for tag in soup.findAll({'img': True, 'script': True, 'link': True, 'style': True}):
			if tag.has_key('src'):
				if tag.name == 'img':
					#If is a img
					img_data = get_html(get_url(base_url, tag['src']))
					#print img_data[0]
					if img_data[0] in ['image/jpeg', 'image/gif', 'image/png']:
						tag['src'] =  'data:' + img_data[0] + ';base64,' + b64encode(img_data[1])
				if tag.name == 'script':
					#If is a scrypt
					_, data = get_html(get_url(base_url, tag['src']))
					js = '<script>' + data+ '</script>'
			if tag.has_key('href'):
				if (tag.has_key('type') and  tag['type'] == "text/css") or ( tag.has_key('rel') and tag['rel'] == "stylesheet"):
					_, data = get_html(get_url(base_url, tag['href']))
					temp_str = str(data)
					for urls in re.findall('url\(([^)]+)\)', temp_str):
						if urls.find('data:') == 0:
							continue
						#print urls
						img_data = get_html(get_url(base_url, urls))
						offset = temp_str.find(urls)
						temp_str = temp_str[:offset] + 'data:' + img_data[0] + ';base64,' + b64encode(img_data[1]) + temp_str[offset + len(urls):]
					tag = '<style media="screen" type="text/css">' + temp_str + '</style>'
					#Get images, fonts, and css from css

		for tag in soup.findAll(attrs={'style': True}):
			temp_str = str(tag['style'])
			for urls in re.findall('url\(([^)]+)\)', temp_str):
				if urls.find('data:') == 0:
					continue
				#print urls
				img_data = get_html(get_url(base_url, urls))
				offset = temp_str.find(urls)
				temp_str = temp_str[:offset] + 'data:' + img_data[0] + ';base64,' + b64encode(img_data[1]) + temp_str[offset + len(urls):]
			#print temp_str
			tag['style'] = temp_str

		if len(argv) > 2:
			url_file = open(argv[2], 'w')
			url_file.write(str(soup))
		else:
			print soup