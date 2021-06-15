from django.urls import path

from .views import *

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("page/<path:menu_path>/", PageView.as_view(), name="page"),
    path("page/", PageView.as_view(), name="page-base"),
    path("basic/", BasicView.as_view(), name="basic"),
    path("classification/", ClassificationView.as_view(), name="classification"),
    path("api/basic/", BasicAjaxView.as_view(), name="basic-api"),
    path("api/classification/", ClassificationAjaxView.as_view(), name="classification-api"),
]
