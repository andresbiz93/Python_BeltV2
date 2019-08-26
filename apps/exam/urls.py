from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.root),
	url(r'^create$', views.create),
	url(r'^board$', views.board),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^board/post_thought', views.post_thought),
	url(r'^board/(?P<thought_id>[0-9]+)/details', views.view_thought),
	url(r'^board/(?P<thought_id>[0-9]+)/delete', views.delete_thought),
	url(r'^board/(?P<thought_id>[0-9]+)/like_thought', views.like_thought),
	url(r'^board/(?P<thought_id>[0-9]+)/unlike_thought', views.unlike_thought)
]