from django import forms


class ImageUploadForm(forms.Form):
    file = forms.ImageField(label='画像ファイル')

class KakikomiForm(forms.Form):
        file = forms.CharField(
        label='調べたい分野',
        max_length=100,
        required=True,
        help_text='必須',
        )
        check = forms.BooleanField(
            label='pdf',
            required = False,
        )
        