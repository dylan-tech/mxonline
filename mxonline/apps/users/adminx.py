import xadmin
from users.models import EmailVerityCode, Banner


class EmailVerityCodeAdmin(object):
    list_display = ['code',  'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'url', 'image', 'index', 'add_time']
    search_fields = ['title', 'url', 'image', 'index']
    list_filter = ['title', 'url', 'image', 'index', 'add_time']


xadmin.site.register(EmailVerityCode, EmailVerityCodeAdmin)
xadmin.site.register(Banner, BannerAdmin)

