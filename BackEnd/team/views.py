import json
import stripe

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework import response
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.conf import settings
from .models import Plan, Team
from .serializers import TeamSerializer, UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    querySet = Team.objects.all()

    def get_queryset(self):
        return self.queryset.fileter(members__in=[self.request.user]).first()

    def perform_create(self, serializer):
        obj = serializer.save(created_by=self.request.user)
        obj.members.add(self.request.user)
        obj.save()


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_my_team(request):
    team = Team.objects.filter(members__in=[request.user]).first()
    serializer = TeamSerializer(team)

    return Response(serializer.data)


@api_view(['POST'])
def upgrade_plan(request):
    team = Team.objects.filter(members__in=[request.user]).first()
    plan = request.data['plan']

    if plan == 'free':
        plan = Plan.objects.get(name='Free')
    elif plan == 'smallteam':
        plan = Plan.objects.get(name='Small Team')
    elif plan == 'bigteam':
        plan = Plan.objects.get(name='Big Team')

    team.plan = plan
    team.save()

    serializer = TeamSerializer(team)

    return Response(serializer.data)


@api_view(['GET'])
def get_stripe_pub_key(request):
    pub_key = settings.STRIPE_PUB_KEY
    return Response({'pub_key': pub_key})


@api_view(['POST'])
def add_member(request):
    team = Team.objects.filter(members__in=[request.user]).first()
    email = request.data['email']
    print('Email', email)
    user = User.objects.get(username=email)
    team.members.add(user)
    team.save()

    return Response()


@api_view(['POST'])
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    data = json.loads(request.body)
    plan = data['plan']

    if plan == 'smallteam':
        pirce_id = settings.STRIPE_PRICE_ID_SMALL_TEAM
    else:
        pirce_id = settings.STRIPE_PRICE_ID_BIG_TEAM

    team = Team.objects.filter(members__in=[request.user]).first()

    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=team.id,
            success_url='%s?session_id={CHECKOUT_SESSION_ID}' % settings.FRONTEND_WEBSITE_SUCCESS_URL,
            cancel_url='%s' % settings.FRONTEND_WEBSITE_CANCEL_URL,
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': pirce_id,
                    'quantity': 1
                }
            ]
        )
        return Response({'sessionId': checkout_session['id']})
    except Exception as e:
        return Response({'Error': str(e)})
