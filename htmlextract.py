from lxml import html
import requests

sites = open('sites.txt', 'r')
for line in sites:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    line = line[:-1]
    print(line)
    try:
        if 'https://' in line or 'http://' in line:
            page = requests.get(line, headers= headers)
        else:
            page = requests.get('http://'+line, headers= headers)
        line2 = line
        pos = line2.rfind('//')
        line2 = line2[pos+2:]
        pos = line2.rfind('.') # find rightmost dot       # found one
        line2 = line2[:pos]
        if 'www.' in line2:
            line2 = line2[4:]
        file = open('htmlfiles/'+line2+'.htm', 'w+', encoding = 'utf8')
        file.write(page.text)
        file.close()
    except:
        print(line,'niet kunnen bereiken')
   
    # file = open('amazontest1.htm', 'w+', encoding = 'utf8')
    # file.write(page.text)
    # headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt)'}
    # page = requests.get(line)
    # file = open('amazontest2.htm', 'w+', encoding = 'utf8')
    # file.write(page.text)
    # headers = {'User-Agent': 'Mozilla/2.0 (compatible; MSIE 3.02; Windows 3.1)'}
    # page = requests.get(line)
    # file = open('amazontest3.htm', 'w+', encoding = 'utf8')
    # file.write(page.text)
    # headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1'}
    # page = requests.get(line)
    # file = open('amazontest4.htm', 'w+', encoding = 'utf8')
    # file.write(page.text)
    # headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'}
    # page = requests.get(line)
    # file = open('amazontest5.htm', 'w+', encoding = 'utf8')
    # file.write(page.text)

