from django.urls import path, include
from . import views

app_name = 'statuses'

urlpatterns = [
    path('status/<int:status_pk>', views.StatusDetailView.as_view(), name='status_detail'),
    path('create-status/<int:pk>/', views.StatusCreationView.as_view(), name='status_creation'),
    path('status/<int:status_pk>/like', views.StatusLikeView.as_view(), name='status_like'),
    path('status/<int:status_pk>/unlike', views.StatusUnlikeView.as_view(), name='status_unlike'),
    path('status/<int:status_pk>/comment', views.StatusCommentCreateView.as_view(), name='status_create_comment'),
    path('status/<int:status_pk>/edit', views.EditStatusView.as_view(), name='edit_status'),
    path('status/<int:status_pk>/delete', views.DeleteStatusView.as_view(), name='delete_status'),
    path('status/<int:status_pk>/pin', views.PinStatusView.as_view(), name='pin_status'),
    path('user/<int:pk>/status_list', views.StatusListView.as_view(), name='status_list'),
    path('user/private_status_list', views.PrivateStatusListView.as_view(), name='private_status_list'),
]
