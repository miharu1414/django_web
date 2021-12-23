import requests
from bs4 import BeautifulSoup


# Google検索するキーワードを設定
search_word = input("検索する単語")

# 上位から何件までのサイトを抽出するか指定する
count_search = int(input("サイト件数:"))
pages_num = count_search + 1

print(f'【検索ワード】{search_word}')

# Googleから検索結果ページを取得する
url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
request = requests.get(url)

# Googleのページ解析を行う
soup = BeautifulSoup(request.text, "html.parser")
search_site_list = soup.select('div.kCrYT > a')

#urlリスト 
url_list = []
count_site_correct = 0

# ページ解析と結果の出力
for rank, site in zip(range(1, pages_num), search_site_list):
    
    try:
        site_title = site.select('h3.zBAuLc')[0].text
    except IndexError:
        site_title = site.select('img')[0]['alt']
    site_url = site['href'].replace('/url?q=', '')
    # 結果を出力する
    print(str(rank) + "位: " + site_title + ": " + site_url)
    if site_title.find("PDF") != -1:
        print("pdfなので除外")
        continue
    count_site_correct += 1
    url_list.append(site_url)

for i in range(count_site_correct):
    print("{}:{}".format(i+1,url_list[i]))
    
print(count_site_correct)

 
    