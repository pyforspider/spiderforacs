#!/user/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import os
from mailmerge import MailMerge
from docx import Document


def get_html_text(url, headers):
	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print('Fail to get html text.')


def get_title(html):
	pattern = re.compile('content="(.*?)"', re.S)
	title_text = re.findall(pattern, html)[1]
	return title_text


def get_abstract_text(html):
	pattern = re.compile('content="(.*?)"', re.S)
	abstract_text = re.findall(pattern, html)[8]
	return abstract_text


def get_abstract_pic(html):
	pattern = re.compile('article_abstract-img.*?src="(.*?)"', re.S)
	abstract_gif_broken_url = re.findall(pattern, html)[0]
	abstract_gif_url = "https://pubs.acs.org" + abstract_gif_broken_url
	return abstract_gif_url


def write_to_docx(title, abstract, pic):
	doc = Document()
	doc.add_paragraph(title)
	doc.add_paragraph(abstract)
	with open('pic.gif', 'wb') as f:
		r = requests.get(pic)
		f.write(r.content)
	doc.add_picture('pic.gif')
	doc.save('Title & Abstract.docx')


def main():
	url = 'https://pubs.acs.org/doi/10.1021/acsmedchemlett.5b00041'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
	html = get_html_text(url, headers)
	title = get_title(html)
	abstract = get_abstract_text(html)
	abstract_gif_url = get_abstract_pic(html)
	write_to_docx(title, abstract, abstract_gif_url)


if __name__ == '__main__':
	main()

