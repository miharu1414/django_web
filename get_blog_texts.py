import sys
import requests
from bs4.element import Tag, NavigableString
from bs4 import BeautifulSoup
import math
import time
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSStopFilter
from sklearn.feature_extraction.text import CountVectorizer
import unicodedata

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

def _parse_li(li):
    """
    リストアイテム(li)のテキストを返す。
    ※ li内の入れ子リストは除外する (重複するため)
    """
    buffer = []
    for child in li:
        if type(child) == NavigableString:
            buffer.append(child.string)
        elif type(child) == Tag:
            # リスト構造ではない child のみ返り値に含める
            if child.find_all('li') == []:
                buffer.append(child.get_text())
    return ''.join(buffer)


def get_blog_texts(url: str):
    """get blog texts from url"""
    # get html source
    response = requests.get(url)
    # parse html
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find('body')
    texts = ["0"]
    # extract all <p>...</p> texts
    try:
        texts = [c.get_text() for c in contents.find_all('p')]
 
    # extract all <li>...</li> texts
    
        texts = texts + [_parse_li(li) for li in contents.find_all('li')]

    # processing
        texts = [t.replace('\n', '') for t in texts]
    except (AttributeError,UnboundLocalError):
        pass

    return texts

def calc_tf(b_idx, w_idx,BLOG):
    """b_idx 番目のブログの WORD[w_idx] の TF値を算出する"""
    # WORD[w_idx] の出現回数の和
    word_count = BLOG[b_idx]["bow"][w_idx]
    if word_count == 0:
        return 0.0
    # 全単語の出現回数の和
    sum_of_words = sum(BLOG[b_idx]["bow"])
    # TF値計計算
    return word_count/float(sum_of_words)

def sum_emerge(w_idx,index,BLOG):
    count =0
    for  i in range(index):
        count += BLOG[i]["bow"][w_idx]
    return count

def calc_idf(w_idx,BLOG):
    """WORD[w_idx] の IDF値を算出する"""
    # 総文書数
    N = len(BLOG.keys())
    # 単語 word が出現する文書数 df を計算
    df = len([i for i in BLOG.keys() if BLOG[i]["bow"][w_idx] > 0])
    # idf を計算
    return math.log2(N/float(df + 1))

def calc_tfidf(b_idx, w_idx,BLOG):
    """b_idx 番目のブログの WORD[w_idx] の TF-IDF値を算出する"""
    return calc_tf(b_idx, w_idx,BLOG) * calc_idf(w_idx,BLOG)


def url_list_cal(url_list,BLOG):
    for i, url in enumerate(url_list):
        BLOG[i] = {}
        BLOG[i]["url"] = url

def input_dict(BLOG):
    for i in BLOG.keys():
        url = BLOG[i]["url"]
        print("#{} getting texts from: {}".format(i, url))
        try:
            BLOG[i]["texts"] =  get_blog_texts(url)
            BLOG[i]["texts"] = [t.replace(' ','').lower() for t in BLOG[i]["texts"]]
        except:
            BLOG[i]["texts"] = [""]
            print("error: not getting")
        time.sleep(1)

        
def wakati(BLOG,work,WAKATI):    
              # 各ブログの名詞を分かち書きして登録
    tokenizer = Tokenizer()
    token_filters = [POSStopFilter(['記号','助詞','助動詞','動詞','形容詞','副詞'])]
    a = Analyzer(tokenizer=tokenizer, token_filters=token_filters)


    for i in BLOG.keys():
        texts_flat = "".join(BLOG[i]["texts"])
        tokens = a.analyze(texts_flat)
        BLOG[i]["wakati"] = ' '.join([t.surface for t in tokens])
        work.append(' '.join([t.surface for t in tokens]))
        WAKATI.append(work[i].lower().split())



    
    
if __name__ == "__main__":
    url = sys.argv[1]
    [print(t) for t in get_blog_texts(url)]