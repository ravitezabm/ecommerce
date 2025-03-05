from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('product_list/',views.list_products,name='list_product'),
    path('product_detailed/<pk>',views.detail_products,name='detail_product')
]
urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
