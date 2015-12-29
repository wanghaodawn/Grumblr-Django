
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'grumblr.views.login_page', name = 'home'),
    url(r'^login$','django.contrib.auth.views.login',{'template_name':'login_page.html'}, name = 'login'),
    url(r'^signup_page$', 'grumblr.views.signup_page', name = 'signup'),
    url(r'^profile$', 'grumblr.views.profile', name = 'profile'),
    url(r'^global_page$', 'grumblr.views.add_post', name = 'global'),
    url(r'^profile-page/(?P<id>\d+)$', 'grumblr.views.profile_page', name = 'profile_page'),
    url(r'^edit_page$','grumblr.views.edit_page', name = 'edit_page'),
    url(r'^photo/(?P<id>\d+)$','grumblr.views.upload_photo',name = 'upload_photo'),
    url(r'^follower_page$','grumblr.views.follow_page',name = 'follow_page'),
    url(r'^follow/(?P<id>\d+)$','grumblr.views.follow',name = 'follow'),
    url(r'^unfollow/(?P<id>\d+)$','grumblr.views.unfollow',name = 'unfollow'),
    url(r'^change_password$','grumblr.views.change_password',name='change_password'),
    url(r'^logout$','django.contrib.auth.views.logout_then_login', name = 'logout'),
    url(r'^confirmmessage$','grumblr.views.change_password',name = 'confirmmessage'),
    url(r'^email_sent/(?P<token>[a-zA-Z0-9_\-]+)/(?P<username>[a-zA-Z0-9_]+)/$','grumblr.views.email_sent',name ='email_sent'),
    url(r'^reset_password$','grumblr.views.reset_password',name='reset'),
    url(r'^get_posts$','grumblr.views.get_posts',name = 'get_posts'),
    url(r'^get_changes$','grumblr.views.get_changes',name = 'get_changes'),
    url(r'^get_changes/(?P<log_id>\d+)$','grumblr.views.get_changes',name = 'get_changes'),
    url(r'^add_comment/(?P<post_id>\d+)$','grumblr.views.add_comment',name='add_comment')
]
