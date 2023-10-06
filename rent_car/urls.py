from django.urls import path

from rent_car import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('car-list', views.TypeRateList.as_view(), name='car-list'),
    path('save-data', views.SaveData.as_view(), name='save-data'),
    path('detail/<int:extra_id>', views.DetailExtra.as_view(), name='detail'),
    path('price', views.AdjustPrice.as_view(), name='price'),
]
