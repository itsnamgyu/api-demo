import json

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.forms import BasicForm, ClassificationForm
from dt_content.views.core import PageView as BasePageView


class IndexView(BasePageView):
    template_name = "core/index.html"
    menu_base_url = reverse_lazy("core:page-base")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dt_stripe"] = apps.is_installed("dt_stripe")
        context["simple_sendgrid"] = apps.is_installed("simple_sendgrid")
        return context


class PageView(BasePageView):
    template_name = "core/page.html"
    menu_base_url = reverse_lazy("core:page-base")


db_names = [
    "도윤",
    "서아",
    "서준",
    "하윤",
    "하준",
    "지안",
    "은우",
    "서윤",
    "시우",
    "하은"
    "이준",
    "지호",
]


class BasicView(FormView):
    form_class = BasicForm
    template_name = "core/basic_form.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        number = form.cleaned_data["student_number"]
        name = db_names[number]
        return render(self.request, "core/basic_result.html", context={
            "number": number,
            "name": name
        })


class ClassificationView(FormView):
    form_class = ClassificationForm
    template_name = "core/classification_form.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return render(self.request, "core/classification_result.html", context={
            "p": form.p,
        })


class BasicAjaxView(FormView):
    form_class = BasicForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        number = form.cleaned_data["student_number"]
        name = db_names[number]
        return JsonResponse({
            "number": number,
            "name": name
        })


class ClassificationAjaxView(FormView):
    form_class = ClassificationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        p = form.p
        return JsonResponse({
            "cat_probability": p,
        })
