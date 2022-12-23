from django.urls import path,include
from . import views
#from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register("LoanDetail",views.LoanDetailApi)
#router.register("NewUser",views.UserDetailApi)

urlpatterns = [
  #path('api/',include(router.urls)),
  path('apilist/', views.loanList, name='loanapilist'),
  path('apicreate/', views.loanCreate, name='loanapicreate'),
]
