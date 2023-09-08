from django.urls import path
from .views import *

urlpatterns = [
    # path('', home),
    # path('student/', post_student),
    # path('delete/<slug:slug>/', delete_student),
    # path('update-student/<id>/', update_student),
    path("", StudentAPI.as_view()),
    path("register-user/", RegisterUser.as_view()),

    
]
