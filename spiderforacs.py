import requests
import re
import os
from lxml import etree


def get_html_text(url, headers):
	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "Failed"


def parse_pdf_link(html):
	pattern = re.compile('.*?title="PDF".*?href="(.*?)"', re.S)
	pdf_links = re.findall(pattern, html)
	pdf_intact_links = []
	for pdf_link in pdf_links:
		pdf_intact_link = 'https://pubs.acs.org' + pdf_link
		pdf_intact_links.append(pdf_intact_link)
	return pdf_intact_links


def parser_names(html):
	selector = etree.HTML(html)
	lis = selector.xpath('//h5[@class="issue-item_title"]')
	pdf_name_list = []
	for h5 in lis:
		'''This small black point '.' costs me hours.'''
		pdf_name = ''
		pdf_name_splits = h5.xpath('.//text()')
		for split in pdf_name_splits:
			pdf_name += split
		pdfname_str_lis = list(pdf_name)
		number = 0
		for char in pdfname_str_lis:
			if char in ['<', '>', '/', '\\', '|', ':', '"', '*', '?']:
				pdfname_str_lis.pop(number)
			number += 1
		pdf_name = ''.join(pdfname_str_lis)
		pdf_name_list.append(pdf_name)
	return pdf_name_list


def save_pdf(pdf_intact_links, big_path, pdf_names, i):
	count = 0
	for pdf_intact_link in pdf_intact_links:
		try:
			print("Acquiring PDF file: " + pdf_names[count][0:60] + '...' + ".pdf")
			r = requests.get(pdf_intact_link)
			file_path = big_path + os.path.sep + '{file_name}.{file_suffix}'.format(
				file_name=str(count+i*20+1) + ' ' + pdf_names[count],
				file_suffix='pdf')
			with open(file_path, 'wb') as f:
				f.write(r.content)
				count = count + 1
				print('Success to download PDF file.')
		except: # FileNotFoundError or OSError
			print('Fail to download PDF file.')
			count = count + 1


def main(kw, page_number):
	url = "https://pubs.acs.org/action/doSearch?AllField=" + kw
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
	big_path = 'Literature for ' + kw + os.path.sep
	if not os.path.exists(big_path):
		os.makedirs(big_path)
	for i in range(page_number):
		url_page = url + "&startPage=" + str(i) + "&pageSize=20"
		html = get_html_text(url_page, headers)
		pdf_intact_links = parse_pdf_link(html)
		pdf_names = parser_names(html)
		save_pdf(pdf_intact_links, big_path, pdf_names, i)


if __name__ == '__main__':
	total_page = 10
	keyword = input('Key Word: ')
	main(keyword, total_page)


#   PQuery can do like this:
#   wrap.find('p').remove()
#   print(wrap.text())
