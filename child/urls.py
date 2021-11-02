from django.urls import path, include

from . import views

urlpatterns = [
    path('childview', views.childview, name = 'childview'),
    path('kids', views.kids, name = 'kids'),
    path('addChild', views.addChild, name = 'addChild'),
    path('newChild', views.newChild, name = 'newChild'),
    path('newChild2', views.newChild2, name = 'newChild2'),
    path('newChild3', views.newChild3, name = 'newChild3'),
    path('newChild4', views.newChild4, name = 'newChild4'),
    path('newChild5', views.newChild5, name = 'newChild5'),

    path('removeChild', views.removeChild, name = 'removeChild'),
    path("<int:Kids_id>", views.childview),
    path('updateChild', views.updateChild, name = 'updateChild'),
    path('updateChildPersonal', views.updateChildPersonal, name = 'updateChildPersonal'),
    path('updateChild3', views.updateChild3, name = 'updateChild3'),
    path('updateContacts', views.updateContacts, name = 'updateContacts'),
    path('updateChildComplete', views.updateChildComplete, name = 'updateChildComplete'),
    path('newParent', views.newParent, name = 'newParent'),
]


# url 'childview' %}?name={{kid.id}}


