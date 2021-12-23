from bs4 import BeautifulSoup
import requests

url = "https://dev.classmethod.jp/cloud/aws/aws-nw-architectures-net320/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
type(soup)
contents = soup.find('div')
print(contents.get_text())
print(soup.get_text())
texts_p = [c.get_text() for c in contents.find_all('p')]

import re

# p 要素の抽出
texts_p = [c.get_text() for c in contents.find_all('p')]
# 空白行削除 + 改行コード削除
texts_p = [t.replace('\n','') for t in texts_p if re.match('\S', t)]