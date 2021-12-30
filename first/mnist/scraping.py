#edit yourself
import re
from numpy import result_type
from numpy.lib.function_base import delete
from sklearn.feature_extraction.text import CountVectorizer
from get_blog_texts import get_blog_texts,url_list_cal,input_dict,wakati,calc_tf,calc_idf,calc_tfidf,sum_emerge,is_japanese
import requests
from bs4 import BeautifulSoup

def Scraping(word,num_site):
    result = ""
    #登場しすぎた場合に削除する基準　　　　1サイト当り何回登場したら排除するか
    delete_ratio = 100

    # Google検索するキーワードを設定
    search_word = word
    search_word += ""
    # 上位から何件までのサイトを抽出するか指定する
    num_site = int(num_site)
    pages_num = num_site + 1

    print(f'【検索ワード】{search_word}')

    #urlリスト 
    url_list = []
    count_site_correct = 0
    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
    request = requests.get(url)
    # Googleのページ解析を行う
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')
    # ページ解析と結果の出力
    for rank, site in zip(range(1, pages_num), search_site_list):
        
        try:
            site_title = site.select('h3.zBAuLc')[0].text
        except IndexError:
            site_title = site.select('img')[0]['alt']
        site_url = site['href'].replace('/url?q=', '')
        # 結果を出力する
        print(str(rank) + "位: " + site_title + ": " + site_url)
        if site_title.find("PDF")!=-1 or site_url.find("twitter")  != -1 or site_title.find("マイナビ")  != -1:
            print("pdfなので除外")
            continue
        count_site_correct += 1
        url_list.append(site_url)

    for i in range(count_site_correct):
        url_list[i] = url_list[i].split('&s')[0]
        print("{}:{}".format(i+1,url_list[i]))
        
    print(count_site_correct)


    BLOG = {}
    url_list_cal(url_list, BLOG)

    #textの抽出
    input_dict(BLOG)


    for i in BLOG.keys():
        #print(BLOG[i]["texts"])
        BLOG[i]["texts"] = [t.replace(' ','').lower() for t in BLOG[i]["texts"]]
        print( BLOG[i]["texts"])


    #print(BLOG.keys())


    work = []
    WAKATI = []
    # 解析
    wakati(BLOG,work,WAKATI)


    # 確認
    for i in BLOG.keys():
        print("BLOG[{}][wakati]: {}".format(i,BLOG[i]["wakati"]))

    #正常に抽出できてないサイトは排除
    for i in range(count_site_correct):
        if BLOG[i]["wakati"] == 0:
            del BLOG[i]
            
    vectorizer = CountVectorizer()
    print(BLOG.keys())
    X = vectorizer.fit_transform([BLOG[i]["wakati"] for i in BLOG.keys()])
    for i, bow in enumerate(X.toarray()):
        BLOG[i]["bow"] = bow

    WORDS = vectorizer.get_feature_names()


    """
    num_comeout = int(input())
    n = num_comeout  #登場回数
    for i in BLOG.keys():
        print("url of SITE[{}]: {}".format(i,BLOG[i]["url"]))
        print("list high frequency(>={}) words of SITE[{}]".format(n, i))
        for w_idx, count in enumerate(BLOG[i]["bow"]):
            if count >= n:
                print(" - {}\t{}: WORDS[{}]".format(count, WORDS[w_idx], w_idx))
    """

    #数字,英字だけのもの　や　多すぎるものは排除
    i_words = 0
    print()
    while i_words < len(WORDS):
        if WORDS[i_words].isdecimal():#数字のみなら削除
            del WORDS[i_words]
            continue
        elif is_japanese(WORDS[i_words]) == False:#英語のみなら削除
            del WORDS[i_words]
            continue
        elif sum_emerge(i_words,count_site_correct,BLOG) > delete_ratio*count_site_correct:
            del WORDS[i_words]
            continue
        i_words += 1
        
            
    print(WORDS)
    SUM_IDF = {}
    SUM_TFIDF = {}
    SUM_TF = {}
    count_right = 0
    for index in range(count_site_correct):
        try:
            print("# TF values of blog:{}".format(BLOG[index]["url"]))
            result += "# TF values of blog:" + str(BLOG[index]["url"]) + "\n"
            sample_tfs = [calc_tf(index, w_idx,BLOG) for w_idx, word in enumerate(WORDS)]
            tfs_sorted = sorted(enumerate(sample_tfs), key=lambda x:x[1], reverse=True)
            for i, tf in tfs_sorted[:10]:
                print("{}\t{}".format(WORDS[i], round(tf, 4)))
                result += str(WORDS[i]) + "\t" + str(round(tf,4)) + "\n"
            for i, tf in tfs_sorted:
                if count_right == 0:
                        SUM_TF[str(WORDS[i])] = round(tf, 4)
                else:   
                        SUM_TF[str(WORDS[i])] += round(tf, 4)
            
            IDFS = [calc_idf(w_idx,BLOG) for w_idx, word in enumerate(WORDS)]
            idfs_sorted  = sorted(enumerate(IDFS), key=lambda x:x[1], reverse=True)
            
            print("# IDF values")
            result += "# IDF values\n"
            for w_idx, idf in idfs_sorted[:10]:
                print("{}\t{}".format(WORDS[w_idx], round(idf, 4)))
                result += str(WORDS[w_idx]) + "\t" + str(round(tf,4)) + "\n"
            print("︙")
            result += "︙\n" 
            for w_idx, idf in idfs_sorted[-10:]:
                print("{}\t{}".format(WORDS[w_idx], round(idf, 4)))
                result += str(WORDS[w_idx]) + "\t" + str(round(tf,4)) + "\n"
            for w_idx, idf in idfs_sorted:
                if count_right == 0:
                    SUM_IDF[str(WORDS[w_idx])] = round(idf, 4)
                else:   
                    SUM_IDF[str(WORDS[w_idx])] += round(idf, 4)
                    
            print("# TF-IDF values")
            result += "# TF-IDF values\n"
            TF_IDF = [calc_tfidf(index,w_idx,BLOG) for w_idx, word in enumerate(WORDS)]
            tf_idfs_sorted  = sorted(enumerate(TF_IDF), key=lambda x:x[1], reverse=True)
            
            for w_idx, tf_idf in tf_idfs_sorted[:10]:
                print("{}\t{}".format(WORDS[w_idx], round(tf_idf, 4)))
                result += str(WORDS[w_idx]) + "\t" + str(round(tf_idf,4)) + "\n"
            for w_idx, tf_idf in tf_idfs_sorted:
                if count_right == 0:
                    SUM_TFIDF[str(WORDS[w_idx])] = round(tf_idf, 4)
                else:   
                    SUM_TFIDF[str(WORDS[w_idx])] += round(tf_idf, 4)
            count_right += 1
            
        except KeyError:
            pass
    SUM_TFIDF  = sorted(SUM_TFIDF.items(), key=lambda x:x[1], reverse=True)
    SUM_IDF  = sorted(SUM_IDF.items(), key=lambda x:x[1], reverse=True)
    SUM_TF  = sorted(SUM_TF.items(), key=lambda x:x[1], reverse=True)

    print("\nトータルの集計 TF")
    result += "トータルの集計 TF\n"
    for i in range(min(10,len(SUM_TF))):
        print("{}\t{}".format(SUM_TF[i][0], round(SUM_TF[i][1], 4)))
        result += str(SUM_TF[i][0]) +"\t" +  str(round(SUM_TF[i][1], 4)) + "\n"
        

    print("\nトータルの集計 IDF")
    for i in range(min(10,len(SUM_IDF))):
        print("{}\t{}".format(SUM_IDF[i][0], round(SUM_IDF[i][1], 4)))
        result += str(SUM_TF[i][0]) +"\t" +  str(round(SUM_TF[i][1], 4)) + "\n"

    print("\nトータルの集計 TF-IDF")
    for i in range(min(10,len(SUM_TFIDF))):
        print("{}\t{}".format(SUM_TFIDF[i][0], round(SUM_TFIDF[i][1], 4)))
        result += str(SUM_TF[i][0]) +"\t" +  str(round(SUM_TF[i][1], 4)) + "\n"
        
    print(WORDS)
    result += "\n\n単語リスト\n" + " ".join(WORDS) 
    return result

if __name__ == "__main__":
    Word = input("単語:")
    Num_site = input("サイト件数:")
    s = Scraping(Word,Num_site)
    print("finished")
    a = input()
    print(s)