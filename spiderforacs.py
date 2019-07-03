import requests
import re
import os


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
	result = re.findall(pattern, html)
	return result


def parse_names(html):
	pattern2 = re.compile('.*?class="issue-item_title".*?href=.*?>(.*?)<span', re.S)
	pattern3 = re.compile('.*?class="single_highlight_class">(.*?)</span>.*?</a></h5><h4>', re.S)
	pattern4 = re.compile('.*?class="issue-item_title".*?class="single_highlight_class".*?</span>(.*?)</a></h5><h4></h4></span><ul.class="issue-item_loa"', re.S)
	pdfnames2 = re.findall(pattern2, html)
	pdfnames3 = re.findall(pattern3, html)
	pdfnames4 = re.findall(pattern4, html)
	pdfnames = []
	for i in range(len(pdfnames2)):
		a = pdfnames2[i] + pdfnames3[i] + pdfnames4[i]
		pdfnames.append(a)
	return pdfnames
	
#   PQuery can do like this:
#   wrap.find('p').remove() 
#   print(wrap.text())


def save_pdf(result, big_path, pdfnames):
	count = 0
	for i in result:
		try:
			print ("Aquiring pdf file "+ pdfnames[count] + ".pdf")
			r = requests.get(i)
			file_path = big_path + os.path.sep + '{file_name}.{file_suffix}'.format(
				file_name=str(count) +' ' + pdfnames[count],
				file_suffix='pdf')
			with open(file_path, 'wb') as f:
				f.write(r.content)
				count = count + 1
		except:
			print( 'Fail to dowmload file '+ pdfnames[count] )
			count = count + 1

def main(kw):
	url = "https://pubs.acs.org/action/doSearch?AllField=" + kw
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
	html = get_one_page(url, headers)
	result = parse_one_page(html)
	big_path = 'Literature for '+ kw + os.path.sep
	if not os.path.exists(big_path):
		os.makedirs(big_path)
	result2 = []
	for i in result:
		urlpdf = 'https://pubs.acs.org' + i
		result2.append(urlpdf)
	pdfnames = parse_names(html)
	save_pdf(result2, big_path, pdfnames)


if __name__ == '__main__':
	kw = 'BODIPY'
	kw = input ('Key Word: ')
	main(kw)
	

