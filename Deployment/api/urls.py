
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path("",views.index,name="index"),
    path("predict_price",views.predict_price, name="predict_price")
]