import base64
from io import BytesIO
import re
from tabnanny import check
from urllib import request
from django.shortcuts import redirect, render
from django.views import generic
from .forms import ImageUploadForm, KakikomiForm
from .lib import predict
import numpy as np
from PIL import Image
from .scraping import Scraping
from .scraping_pdf import Scraping_pdf
from .pdf_to_text import Pdf_to_text


class UploadView(generic.FormView):
    template_name = 'mnist/upload.html'
    form_class = KakikomiForm

    def form_valid(self, form):
     # アップロードファイル本体を取得
        Word = form.cleaned_data['file']
        Num_site = 3
        kind = form.cleaned_data["check"]
        # 推論した結果を、テンプレートへ渡して表示
        if kind:
            context = {
                'result': Scraping_pdf(Word,Num_site),
            }
        else:
            context = {
                'result': Scraping(Word,Num_site),
            }        
        return render(self.request, 'mnist/result.html', context)
    

class Pdf_to_text_View(generic.FormView):
    template_name = 'mnist/pdf_to_text.html'
    form_class = KakikomiForm


    def form_valid(self, form):
     # アップロードファイル本体を取得
        pdf_url = form.cleaned_data['file']
        

        # 推論した結果を、テンプレートへ渡して表示
        context = {
            'result': Pdf_to_text(pdf_url),
        }
        return render(self.request, 'mnist/result.html', context)


class PaintView(generic.TemplateView):
    template_name = 'mnist/paint.html'

    def post(self, request):
        base_64_string = request.POST['img-src'].replace(
            'data:image/png;base64,', '')
        file = BytesIO(base64.b64decode(base_64_string))

        # ファイルを、28*28にリサイズし、グレースケール(モノクロ画像)
        img = Image.open(file).resize((28, 28)).convert('L')

        # 学習時と同じ形に画像データを変換する
        img_array = np.asarray(img) / 255
        img_array = img_array.reshape(1, 784)

        # 推論した結果を、テンプレートへ渡して表示
        context = {
            'result': predict(img_array),
        }
        return render(self.request, 'mnist/result.html', context)



