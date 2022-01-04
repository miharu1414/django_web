from django.urls import path
from . import views

app_name = 'mnist'

urlpatterns = [
    path('', views.UploadView.as_view(), name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('paint/', views.PaintView.as_view(), name='paint'),
    path('pdf_to_text/', views.Pdf_to_text_View.as_view(), name='pdf_to_text'),
]
