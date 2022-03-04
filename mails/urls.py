from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path("selection", views.selection, name="selection"),
    path("storedmails", views.storedmails, name="storedmails"),
    path("sendemail", views.sendemail, name="sendemail"),
    path("sendemail/<str:title>", views.sendemail, name="sendemail"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('signout', views.signout, name='signout'),
    # path("groupemail", views.groupemail, name='groupemail'),
    # path('groupemail/<str:title>', views.groupemail, name='groupemail'),
    path('schedulemail', views.schedulemail, name='schedulemail'),
    path('schedulemail/<str:title>', views.schedulemail, name='schedulemail'),
    path('viewemailids', views.viewemailids, name='viewemailids'),
    path('viewgroups', views.viewgroups, name='viewgroups'),
    path('viewgroupdetails/<str:group_name>',
         views.viewgroupdetails, name='viewgroupdetails'),
    path('sentmails', views.sentmailslist, name='sentmails'),
    path('registeruser', views.registeruser, name='registeruser'),
    path('userverification', views.userverification, name='userverification'),
    path('validatewithotp', views.validatewithotp, name='validatewithotp'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('addgroupmember/<str:group_name>',
         views.addgroupmember, name='addgroupmember'),
    path('viewgroupstomodify', views.viewgroups1, name='viewgroupstomodify'),
    path('viewgroupdetailstomodify/<str:group_name>',
         views.viewgroupdetails1, name='viewgroupdetailstomodify'),
    path('editgroupdetails/<str:group_name>',
         views.editgroupdetails, name='editgroupdetails'),
    path('deletegroupmember/<str:email_address>/<str:group_name>',
         views.deletegroupmembers, name='deletegroupmember'),
    path('editprofile', views.editprofile, name='editprofile'),

    # path('unblockuser', views.unblockuser, name='unblockuser')
#     path('forgetpage', views.forgetpage, name='forgetpage')
    # path("",views.,name="")
]
