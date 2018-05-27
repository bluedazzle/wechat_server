from django.conf.urls import include, url
from service.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'wechat_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^sxrhy/$', MainServiceView.as_view()),
]
