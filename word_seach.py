#edit yourself

from sklearn.feature_extraction.text import CountVectorizer
import random
import enum
from get_blog_texts import get_blog_texts
import time 
import math


def calc_tf(b_idx, w_idx):
    """b_idx 番目のブログの WORD[w_idx] の TF値を算出する"""
    # WORD[w_idx] の出現回数の和
    word_count = BLOG[b_idx]["bow"][w_idx]
    if word_count == 0:
        return 0.0
    # 全単語の出現回数の和
    sum_of_words = sum(BLOG[b_idx]["bow"])
    # TF値計計算
    return word_count/float(sum_of_words)

def calc_idf(w_idx):
    """WORD[w_idx] の IDF値を算出する"""
    # 総文書数
    N = len(BLOG.keys())
    # 単語 word が出現する文書数 df を計算
    df = len([i for i in BLOG.keys() if BLOG[i]["bow"][w_idx] > 0])
    # idf を計算
    return math.log2(N/float(df + 1))

def calc_tfidf(b_idx, w_idx):
    """b_idx 番目のブログの WORD[w_idx] の TF-IDF値を算出する"""
    return calc_tf(b_idx, w_idx) * calc_idf(w_idx)


url_list =[]
url_list.append("https://dev.classmethod.jp/cloud/aws/aws-nw-architectures-net320/")

BLOG = {}
for i, url in enumerate(url_list):
    BLOG[i] = {}
    BLOG[i]["url"] = url
print("len(BLOG): {}".format(len(BLOG)))
print("BLOG[0][\"url\"]: {}".format(BLOG[0]["url"]))


for i in BLOG.keys():
    url = BLOG[i]["url"]
    print("#{} getting texts from: {}".format(i, url))
    BLOG[i]["texts"] = get_blog_texts(url)
    time.sleep(1)

for i in BLOG.keys():
    BLOG[i]["texts"] = [t.replace(' ','').lower() for t in BLOG[i]["texts"]]

print("len(BLOG[0][texts]): {}".format(len(BLOG[0]["texts"])))
print("len(BLOG[0][texts][0]): {}".format(BLOG[0]["texts"][0]))

for i in BLOG.keys():
    BLOG[i]["texts"] = [t.replace(' ','').lower() for t in BLOG[i]["texts"]]

print("len(BLOG[0][texts]): {}".format(len(BLOG[0]["texts"])))
print("len(BLOG[0][texts][0]): {}".format(BLOG[0]["texts"][0]))

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSStopFilter

tokenizer = Tokenizer()
token_filters = [POSStopFilter(['記号','助詞','助動詞','動詞'])]
a = Analyzer(tokenizer=tokenizer, token_filters=token_filters)

test_tokens = a.analyze(BLOG[0]["texts"][0])
for t in test_tokens:
    print(t)
    

# 解析
for i in BLOG.keys():
    texts_flat = "。".join(BLOG[i]["texts"])
    tokens = a.analyze(texts_flat)
    BLOG[i]["wakati"] = ' '.join([t.surface for t in tokens])
# 確認
print("BLOG[0][wakati]: {}".format(BLOG[0]["wakati"]))


vectorizer = CountVectorizer()

X = vectorizer.fit_transform([BLOG[i]["wakati"] for i in BLOG.keys()])
for i, bow in enumerate(X.toarray()):
    BLOG[i]["bow"] = bow

WORDS = vectorizer.get_feature_names()
print(WORDS)

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
    


index = 0
print("# TF values of blog:{}".format(BLOG[index]["url"]))
sample_tfs = [calc_tf(index, w_idx) for w_idx, word in enumerate(WORDS)]
tfs_sorted = sorted(enumerate(sample_tfs), key=lambda x:x[1], reverse=True)
for i, tf in tfs_sorted[:20]:
    print("{}\t{}".format(WORDS[i], round(tf, 4)))
    



IDFS = [calc_idf(w_idx) for w_idx, word in enumerate(WORDS)]

idfs_sorted  = sorted(enumerate(IDFS), key=lambda x:x[1], reverse=True)
print("# IDF values")
for w_idx, idf in idfs_sorted[:10]:
    print("{}\t{}".format(WORDS[w_idx], round(idf, 4)))
print("︙")
for w_idx, idf in idfs_sorted[-10:]:
    print("{}\t{}".format(WORDS[w_idx], round(idf, 4)))


