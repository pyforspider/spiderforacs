import requests
import re
import os
from lxml import etree


def get_one_page(url,headers):
	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "Failed"


def parse_one_page(html):
	pattern = re.compile('.*?title="PDF".*?href="(.*?)"', re.S)
	pdf_links = re.findall(pattern, html)
	return pdf_links


# def parse_names(html, kw):
	# This section has a problem with keyword= MOF-5
	# pattern2 = re.compile('.*?class="issue-item_title".*?href=.*?>(.*?)<span', re.S)
	# pattern3 = re.compile('.*?class="single_highlight_class">(.*?)</span>.*?</a></h5><h4>', re.S)
	# pattern4 = re.compile('.*?class="issue-item_title".*?class="single_highlight_class".*?</span>(.*?)</a></h5><h4></h4></span><ul.class="issue-item_loa"', re.S)
	# pdfnames2 = re.findall(pattern2, html)
	# pdfnames3 = re.findall(pattern3, html)
	# pdfnames4 = re.findall(pattern4, html)
	# pdfnames = []
	# for i in range(len(pdfnames2)):
	# 	a = pdfnames2[i] + pdfnames3[i] + pdfnames4[i]
	# 	pdfnames.append(a)
	# return pdfnames

def parser_names(html):
	selector = etree.HTML(html)
	lis = selector.xpath('//h5[@class="issue-item_title"]')
	pdf_name_list = []
	for h5 in lis:
		'''This small black point '.' costs me hours.'''
		pdf_name = ''
		pdf_name_splits = h5.xpath('.//text()')
		for i in pdf_name_splits:
			pdf_name += i
		pdf_name_list.append(pdf_name)
	return pdf_name_list


def save_pdf(pdf_intact_links, big_path, pdf_names, i):
	count = 0
	for pdf_intact_link in pdf_intact_links:
		try:
			print("Acquiring pdf file " + pdf_names[count] + ".pdf")
			r = requests.get(pdf_intact_link)
			file_path = big_path + os.path.sep + '{file_name}.{file_suffix}'.format(
				file_name=str(count+i*20) + ' ' + pdf_names[count],
				file_suffix='pdf')
			with open(file_path, 'wb') as f:
				f.write(r.content)
				count = count + 1
		except:
			print('Fail to download file ' + pdf_names[count])
			count = count + 1


def main(kw, page_number):
	url = "https://pubs.acs.org/action/doSearch?AllField=" + kw
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
	big_path = 'Literature for ' + kw + os.path.sep
	if not os.path.exists(big_path):
		os.makedirs(big_path)

	for i in range(page_number):
		url_page = url + "&startPage=" + str(i) + "&pageSize=20"
		html = get_one_page(url_page, headers)
		pdf_links = parse_one_page(html)
		pdf_intact_links = []
		for pdf_link in pdf_links:
			pdf_intact_link = 'https://pubs.acs.org' + pdf_link
			pdf_intact_links.append(pdf_intact_link)
		pdf_names = parser_names(html)
		save_pdf(pdf_intact_links, big_path, pdf_names, i)


if __name__ == '__main__':
	kw = 'BODIPY'
	total_page = 10
	kw = input ('Key Word: ')
	main(kw, total_page)

#   PQuery can do like this:
#   wrap.find('p').remove()
#   print(wrap.text())
	

