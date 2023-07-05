from django.urls import path
from .views import LoginAPIView,UserLogout,UserList,Register,UserReport
from .transbank import TransbankCreateView, TransbankCommitView, TransbankReverseOrCancelView

app_name = 'api'

urlpatterns = [
    path('log/', LoginAPIView.as_view(), name='login'),
    path('out/', UserLogout.as_view(), name='logout'),
    path('list-user/', UserList().as_view()),
    path('register-user/', Register().as_view()),
    # update_user
    # update_pass

    path('report-user/', UserReport.as_view(), name='user_report'),
    # reporte_arriendos_
    # reporte_agendas


    #transbank
    path('transbank/transaction/create', TransbankCreateView.as_view()),
    path('transbank/transaction/commit/<str:tokenws>', TransbankCommitView.as_view()),
    path('transbank/transaction/reverse-or-cancel/<str:tokenws>', TransbankReverseOrCancelView.as_view()),
  
]

