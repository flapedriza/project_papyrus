from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import status

from .models import User
from .serializers import UserSerializer, ProfileSerializer


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):

    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk=None):
        if pk and pk == str(request.user.pk):
            return self.serialize_user(request.user)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        return self.serialize_user(request.user)

    def update(self, request, pk=None):
        if pk and pk == str(request.user.pk):
            return super(UserViewSet, self).update(request, pk)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        if pk and pk == str(request.user.pk):
            return super(UserViewSet, self).update(request, pk)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def serialize_user(self, user):
        serialized = self.serializer_class(user)
        return Response(serialized.data, status=status.HTTP_200_OK)


class SignUpView(APIView):

    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            user = serializer.instance
            user.set_password(data['password'])
            user.save()

            token = Token.objects.create(user=user)
            result = {'token': token.key}

            return Response(result, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    serializer_class = AuthTokenSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            result = {'token': token.key}
            response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(result, status=response_status)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)