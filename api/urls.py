from django.conf.urls import include, url
from api.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'wechat_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^phone/$', PhoneBindView.as_view()),
]
