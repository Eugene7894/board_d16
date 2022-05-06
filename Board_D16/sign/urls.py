from django.urls import path

from .views import OTPVerif, UserCreation


urlpatterns = [
    path('', UserCreation.as_view(), name='signup'),
    path('otp/<int:pk>', OTPVerif.as_view(), name='otp_page'),

]