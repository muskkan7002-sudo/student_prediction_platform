from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict, name="predict"),
    path("report/<int:pk>/pdf/", views.prediction_report_pdf, name="prediction_report_pdf"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("about/", views.about, name="about"),
]
