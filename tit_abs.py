import requests
import re
import os
from docx import Document
from requests.exceptions import RequestException


def get_html_text(url, headers):
	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except RequestException:
		print('Fail to get html text.')


def parser_lit_links(html):
	pattern = re.compile('.*?class="issue-item_title".*?href="(.*?)">', re.S)
	lit_brok_links = re.findall(pattern, html)
	lit_links = []
	for lit_brok_link in lit_brok_links:
		lit_link = 'https://pubs.acs.org' + lit_brok_link
		lit_links.append(lit_link)
	return lit_links


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


def write_to_docx(doc, path, title, abstract, abstract_gif_url):
	try:
		doc.add_paragraph("Title:")
		doc.add_paragraph(title)
		doc.add_paragraph("Abstract:")
		doc.add_paragraph(abstract)
		pic_name = path + title + ".gif"
		with open(pic_name, 'wb') as f:
			r = requests.get(abstract_gif_url)
			f.write(r.content)
		doc.add_picture(pic_name)
		doc.add_paragraph("\n\n\n")
		doc.save('Title & Abstract.docx')
	except:
		print("Fail to save this to docx.")


def main(kw):
	url = "https://pubs.acs.org/action/doSearch?AllField=" + kw
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
	html = get_html_text(url, headers)
	lit_links = parser_lit_links(html)
	doc = Document()
	path = "pics for Literature " + kw + os.path.sep
	if not os.path.exists(path):
		os.makedirs(path)
	for lit_link in lit_links:
		lit_html = get_html_text(lit_link, headers=headers)
		title = get_title(lit_html)
		abstract = get_abstract_text(lit_html)
		abstract_gif_url = get_abstract_pic(lit_html)
		write_to_docx(doc, path, title, abstract, abstract_gif_url)
		print('success' + lit_link)


if __name__ == '__main__':
	keyword = input("Input keyword: ")
	main(keyword)

