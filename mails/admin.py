from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(mails)
admin.site.register(users)
admin.site.register(mail_members)
admin.site.register(group_members)
admin.site.register(groups)
admin.site.register(sent_mails)
admin.site.register(schedulemails)
admin.site.register(dailymailsdatabase)
admin.site.register(weeklymailsdatabase)
admin.site.register(monthlymailsdatabase)
admin.site.register(users_group)
