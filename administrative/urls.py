from unicodedata import name
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.login_admin, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout_user, name="logout"),
    path('adduser', views.add_user, name="adduser"),
    path('edit/<str:employee_id>', views.edit, name="edit"),
    path('delete/<str:employee_id>', views.delete, name="delete"),
    path('view/<str:employee_id>', views.view, name="view"),
    path('changepassword/<str:employee_id>',
         views.changepassword, name="changepassword"),
    path('mails/<str:employee_id>',
         views.user_mails, name="mails"),
    path('creategroup', views.creategroup, name='creategroup'),
    path('addmember', views.addmember, name='addmember'),
    path('viewgroups', views.viewgroups, name='viewgroups'),
    path('viewgroupdetails/<str:group_name>',
         views.viewgroupdetails, name='viewgroupdetails'),
    path('editgroupdetails/<str:group_name>',
         views.editgroupdetails, name='editgroupdetails'),
    path('deletegroup/<str:group_name>', views.deletegroup, name='deletegroup'),
    path('deletegroupmember/<str:email_address>/<str:group_name>',
         views.deletegroupmembers, name='deletegroupmember'),
    path('addgroupmember/<str:group_name>',
         views.addgroupmember, name='addgroupmember'),
    path('confirmdelete/<str:group_name>',
         views.confirmdelete, name='confirmdelete'),
    path('deletemembers', views.deletemembers, name='deletemembers'),
    path('deleteemail/<str:email_address>',
         views.deleteemail, name='deleteemail'),
    path('approveuser', views.approveuser, name='approveuser'),
    path('activate/<str:email_address>', views.activateuser, name='activate'),
    path('unblockuser/<str:email_add_to_use>',
         views.unblockuser, name='unblockuser'),
    # path("selection", views.selection, name="selection")
]