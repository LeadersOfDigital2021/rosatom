from django.urls import path
from .views import AutenticationView, MainView, MeetingSend, MeetingPrintView, MeetingPrintExtView,\
    AddMeettingView, LogoutView, NotFoundView, MeetingDetailView
from django.conf import settings
from django.conf.urls.static import static

handler404 = "core.views.page_not_found_view"

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('auth', AutenticationView.as_view(), name='auth'),
    path('add_meeting', AddMeettingView.as_view(), name='add_meeting'),
    path('404', NotFoundView.as_view(), name='404'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('meeting_detail/<int:meeting_id>', MeetingDetailView.as_view(), name='view'),
    path('meeting_print/<int:meeting_id>', MeetingPrintView.as_view(), name='view'),
    path('meeting_print_ext/<str:uid>', MeetingPrintExtView.as_view(), name='view'),
    path('meeting_send/<int:meeting_id>', MeetingSend.as_view(), name='view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
