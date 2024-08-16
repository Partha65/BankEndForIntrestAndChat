from django.urls import path
from .views import AcceptedInterestsView, InterestId, RegisterAPI, LoginAPI, SendInterestAPI, ListInterestsAPI, AcceptRejectInterestAPI, ChatMessageAPI, UnrequestedUsersView, LogedInUserDetails
from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('unrequested-users/', UnrequestedUsersView.as_view(), name='unrequested-users'),
    path('accepted-users/', AcceptedInterestsView.as_view(), name='accepted-users'),
    path('interests/', SendInterestAPI.as_view(), name='send_interest'),
    path('logedin-user-details/', LogedInUserDetails.as_view(), name='logedin_user_details'),
    path('intrest-id/<int:receiver_id>/', InterestId.as_view(), name='interest_id'),
    path('interests/list/', ListInterestsAPI.as_view(), name='list_interests'),
    path('interests/<int:pk>/status/', AcceptRejectInterestAPI.as_view(), name='accept_reject_interest'),
    path('chat/<int:receiver_id>/', ChatMessageAPI.as_view(), name='chat'),
]
