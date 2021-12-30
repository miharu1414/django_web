# 必要なPdfminer.sixモジュールのクラスをインポート
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO

# 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得
fp = open("test.pdf", 'rb')

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

print(text)
