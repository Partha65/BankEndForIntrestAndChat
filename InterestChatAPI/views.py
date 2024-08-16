from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from django.contrib.auth.models import User
from .models import Interest, ChatMessage
from .serializers import InterestSerializerId, UserSerializer, InterestSerializer, ChatMessageSerializer
from django.db.models import Q

class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.data['username'])
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
# User = get_user_model()

class UnrequestedUsersView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user

        # Get users who have already been requested by the current user
        requested_users = Interest.objects.filter(sender=current_user).values_list('receiver', flat=True)

        frind_user = Interest.objects.filter(receiver=current_user).values_list('sender', flat=True)
        # Exclude the requested users and the current user themselves
        return User.objects.exclude(id__in=requested_users).exclude(id__in=frind_user).exclude(id=current_user.id)

class AcceptedInterestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user

        # Get the list of users who have accepted the current user's interest requests
        accepted_interests = Interest.objects.filter(Q(sender=current_user, status='accepted') | Q(receiver=current_user, status='accepted')).values_list('sender','receiver')

        # Get the users who accepted the current user's requests
        sent_requests_accepted = Interest.objects.filter(sender=current_user, status='accepted').values_list('receiver', flat=True)
        
        # Get the users whose requests were accepted by the current user
        received_requests_accepted = Interest.objects.filter(receiver=current_user, status='accepted').values_list('sender', flat=True)
        
        accepted_user_ids = set(sent_requests_accepted) | set(received_requests_accepted)

        # Return full user objects for accepted interests
        return User.objects.filter(id__in=accepted_user_ids).exclude(id=current_user.id)
    
class SendInterestAPI(generics.CreateAPIView):
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['sender'] = request.user.id
        interest = Interest.objects.create(sender=request.user, receiver=User.objects.get(id=data['receiver']))
        return Response(InterestSerializer(interest).data)

class ListInterestsAPI(generics.ListAPIView):
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Interest.objects.filter(receiver= self.request.user, status= "pending").exclude(sender_id=self.request.user.id)

class AcceptRejectInterestAPI(generics.UpdateAPIView):
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        interest = Interest.objects.get(id=pk, receiver=request.user)
        interest.status = request.data['status']
        interest.save()
        return Response(InterestSerializer(interest).data)

class ChatMessageAPI(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(
            sender=self.request.user,
            receiver__id=self.kwargs['receiver_id']
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, receiver=User.objects.get(id=self.kwargs['receiver_id']))

class LogedInUserDetails(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        # Exclude the requested users and the current user themselves
        return User.objects.filter(id= current_user.id )
    
class InterestId(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, receiver_id, *args, **kwargs):
        try:
            print("req id ",request.user.id,receiver_id)
            try:
                id1 = Interest.objects.get(sender_id=request.user.id, receiver_id=receiver_id).id
            except Exception as e:
                id1 = ""  
            try:
                id2 = Interest.objects.get(sender_id=receiver_id, receiver_id=request.user.id).id
            except Exception as e:
                id2 = ""    
            if id1 == "" and id2 !="":
                final_id = id2
            elif id1 != "" and id2 =="":    
                final_id = id1
            return Response({'id': final_id}, status=status.HTTP_200_OK)
        except Interest.DoesNotExist:
            return Response({'error': 'Interest not found'}, status=status.HTTP_404_NOT_FOUND)