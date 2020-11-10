from django.urls import path
from . import views
urlpatterns =[
    path("send",views.sendEmail,name="send"),
    path("receive",views.getMessages,name="receive"),
]