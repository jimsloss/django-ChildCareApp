from django.urls import path, include


from . import views

urlpatterns = [

    # acccounts
    path('accounts', views.accounts, name = 'accounts'),

    # accounts - invoices - create invoice
    path('newInvoice', views.newInvoice, name = 'newInvoice'),
    #path('editWeekInvoice/<int:id>', views.editWeekInvoice, name = 'editWeekInvoice'),
    path('editWeekInvoice/<int:id>/<str:month>/<str:year>/<str:parentname>/', views.editWeekInvoice, name = 'editWeekInvoice'),
    #path('editWeekInvoice/<str:id>/<str:month>/<str:year>/<str:surname>/', views.editWeekInvoice, name = 'editWeekInvoice'),
    #path('editWeekInvoice>', views.editWeekInvoice, name = 'editWeekInvoice'),
   
    

    # accounts - purchases - add purchase
    path('addPurchase', views.addPurchase, name = 'addPurchase'),

    # accounts - 
    path('changefees', views.changefees, name = 'changefees'),
    path('changefees2', views.changefees2, name = 'changefees2'),
    path('invoiceview', views.invoiceview, name = 'invoiceview'),

]