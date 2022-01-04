# 必要なPdfminer.sixモジュールのクラスをインポート
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
import time
import urllib.request

def Pdf_to_text(pdf_url):
    url = pdf_url
    save_name='only1.pdf'
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
        fp.close()
        table = str.maketrans({
        '\u3000': '',
        ' ': '',
        '\t': '',
        '\n':'    '
        })
        text = text.translate(table)
    except:
        text = "このurlは処理できませんでした．"+"\n"+"再度ご確認ください．"
    print(text)
    return text

    
            
