from django.urls import path
from .views.bathroom_views import BathroomDetail, Bathrooms
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('bathrooms/', Bathrooms.as_view(), name='bathrooms'),
    path('bathrooms/<int:pk>/', BathroomDetail.as_view(), name='bathroom_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
