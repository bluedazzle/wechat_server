from django.conf.urls import include, url
from page.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'wechat_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^phone/$', PhonePageView.as_view()),
    url(r'^hint/$', HintPageView.as_view()),
]
