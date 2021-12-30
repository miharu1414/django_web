#edit yourself
from numpy.core.numeric import correlate
from numpy.lib.function_base import delete
from sklearn.feature_extraction.text import CountVectorizer
from get_blog_texts import get_blog_texts,url_list_cal,input_dict,wakati,calc_tf,calc_idf,calc_tfidf,sum_emerge,is_japanese
import requests
from bs4 import BeautifulSoup



# 必要なPdfminer.sixモジュールのクラスをインポート
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
import urllib.request
import time

def Scraping_pdf():
#登場しすぎた場合に削除する基準　　　　1サイト当り何回登場したら排除するか
    result = ""
    delete_ratio = 100

    # Google検索するキーワードを設定
    search_word = input("検索する単語:")
    search_word += " PDF"
    # 上位から何件までのサイトを抽出するか指定する

    num_site = int(input("サイト件数:"))
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
        if site_title.find("PDF")!=-1:
            pass
        else:
            print("pdfじゃないので除外")
            continue
        count_site_correct += 1
        url_list.append(site_url)

    for i in range(count_site_correct):
        url_list[i] = url_list[i].split('&s')[0]
        print("{}:{}".format(i+1,url_list[i]))
        
    print(count_site_correct)


    BLOG = {}

    rightpdf = 0
    i =0
    """pdf用のコード"""
    while i < count_site_correct:
        pdf_url = url_list[i] 
        # 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得


        url = pdf_url
        save_name='only.pdf'
        try:
            urllib.request.urlretrieve(url, save_name)
            time.sleep(1)
        
            fp = open(save_name, 'rb')
            

            # 出力先をPythonコンソールするためにIOストリームを取得
            outfp = StringIO()


            # 各種テキスト抽出に必要なPdfminer.sixのオブジェクトを取得する処理

            rmgr = PDFResourceManager() # PDFResourceManagerオブジェクトの取得
            lprms = LAParams()          # LAParamsオブジェクトの取得
            device = TextConverter(rmgr, outfp, laparams=lprms)    # TextConverterオブジェクトの取得
            iprtr = PDFPageInterpreter(rmgr, device) # PDFPageInterpreterオブジェクトの取得
            
            # PDFファイルから1ページずつ解析(テキスト抽出)処理する
            for page in PDFPage.get_pages(fp):
                iprtr.process_page(page)

            text = outfp.getvalue()  # Pythonコンソールへの出力内容を取得
            BLOG[rightpdf] = {}
            BLOG[rightpdf]["texts"] = text
            fp.close()
            
            BLOG[rightpdf]["url"] = url
            rightpdf +=1
        except:
            pass
        i += 1
        
    count_site_correct = rightpdf



    for i in BLOG.keys():
        BLOG[i]["texts"] = [t.replace(' ','').lower() for t in BLOG[i]["texts"]]
        print( BLOG[i]["texts"])


    print(BLOG.keys())


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
            result += "# TF values of blog:{}".format(BLOG[index]["url"])
            sample_tfs = [calc_tf(index, w_idx,BLOG) for w_idx, word in enumerate(WORDS)]
            tfs_sorted = sorted(enumerate(sample_tfs), key=lambda x:x[1], reverse=True)
            for i, tf in tfs_sorted[:10]:
                print("{}\t{}".format(WORDS[i], round(tf, 4)))
                result += str(WORDS[w_idx]) + "\t" + str(round(tf_idf,4)) + "\n"
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
                result += str(WORDS[w_idx]) + "\n" + str(round(tf_idf, 4)) + "\n"
            print("︙")
            for w_idx, idf in idfs_sorted[-10:]:
                print("{}\t{}".format(WORDS[w_idx], round(idf, 4)))
            for w_idx, idf in idfs_sorted:
                if count_right == 0:
                    SUM_IDF[str(WORDS[w_idx])] = round(idf, 4)
                else:   
                    SUM_IDF[str(WORDS[w_idx])] += round(idf, 4)
                    
            print("# TF-IDF values")
            TF_IDF = [calc_tfidf(index,w_idx,BLOG) for w_idx, word in enumerate(WORDS)]
            tf_idfs_sorted  = sorted(enumerate(TF_IDF), key=lambda x:x[1], reverse=True)
            
            for w_idx, tf_idf in tf_idfs_sorted[:10]:
                print("{}\t{}".format(WORDS[w_idx], round(tf_idf, 4)))
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
        result += str(SUM_TF[i][0]) + "\n" + str(round(SUM_TF[i][1], 4)) + "\n"

    print("\nトータルの集計 IDF")
    for i in range(min(10,len(SUM_IDF))):
        print("{}\t{}".format(SUM_IDF[i][0], round(SUM_IDF[i][1], 4)))
        result += str(SUM_IDF[i][0]) +"\n" + str(round(SUM_IDF[i][1], 4)) + "\n"

    print("\nトータルの集計 TF-IDF")
    for i in range(min(10,len(SUM_TFIDF))):
        print("{}\t{}".format(SUM_TFIDF[i][0], round(SUM_TFIDF[i][1], 4)))
        result += str(SUM_TFIDF[i][0]) + "\n" +  str(round(SUM_TFIDF[i][1], 4)) + "\n"
        
    print(WORDS)
    result += "\n\n単語リスト\n" + "".join(WORDS)
    return result


if __name__ == "__main__":
  Scraping_pdf()