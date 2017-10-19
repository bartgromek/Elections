from django.conf.urls import url

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
app_name = 'elections2000'

urlpatterns = [
    url(r'^$', views.main_page),
    url(r'^country/$', views.country_results, name='country'),
    url(r'^voivs/$', views.voivodeships, name='voivodeships'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
'''
url(r'^woj(?P<pk>[0-9]+)$', views.wyniki_woj),
url(r'^okr(?P<pk>[0-9]+)$', views.wyniki_okr),
url(r'^gm(?P<pk>[0-9]+)$', views.wyniki_gm),
url(r'^obw(?P<pk>[0-9]+)$', views.wyniki_obw),
url(r'^kraj/pot', views.woj),
url(r'^woj(?P<pk>[0-9]+)/pot', views.woj_okr),
url(r'^okr(?P<pk>[0-9]+)/pot', views.okr_gm),
url(r'^gm(?P<pk>[0-9]+)/pot', views.gm_obw),
url(r'^obw(?P<pk>[0-9]+)/pot', views.obw_pot),
url(r'^gmina/(?P<gmina>\w+)', views.wyniki_wyszukiwania),
url(r'^login/', views.Logowanie.as_view(), name='logowanie'),
url(r'^nazwa_uz/', views.nazwa_uz),
url(r'^wyloguj/', views.wyloguj, name='wyloguj'),
url(r'^edit_votes(?P<pk>[0-9]+)$', views.edit_votes, name='edit'),
'''
