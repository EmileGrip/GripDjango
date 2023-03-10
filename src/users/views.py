from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from src.users.models import User,Skill,AdminManager,AdminManagerEmployer
from src.users.permissions import IsUserOrReadOnly,IsManager,IsAdmin
from src.users.serializers import CreateUserSerializer, UserSerializer,SkillSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import authenticate
from django.conf import settings

import jwt

class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet,mixins.ListModelMixin):
    """
    Creates, Updates and Retrieves - User Accounts
    """

    queryset = User.objects.all()
    serializers = {'default': UserSerializer, 'create': CreateUserSerializer,'list':UserSerializer}
    permissions = {'default': (IsAdmin,), 'create': (IsAdmin,)}
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_manager','is_employer']

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def get_user_data(self, instance):
        try:
            return Response(UserSerializer(self.request.user, context={'request': self.request}).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + e}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['get'], url_path='manager', url_name='list_manager')
    def list_manager(self, request, *args, **kwargs):

        print(AdminManager.objects.filter(admin=request.user).values_list('manager_id'))
        queryset = self.filter_queryset(User.objects.filter(id__in=AdminManager.objects.filter(admin=request.user).values_list('manager_id')))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='employer', url_name='list_employer')
    def list_employer(self, request, *args, **kwargs):
        queryset = self.filter_queryset(User.objects.filter(id__in=AdminManagerEmployer.objects.filter(admin=request.user).values_list('employer_id')))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='employer-manager', url_name='list_employer_manager')
    def list_employer_manager(self, request, *args, **kwargs):
        queryset = self.filter_queryset(User.objects.filter(id__in=AdminManagerEmployer.objects.filter(manager=request.user).values_list('employer_id')))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(CreateUserSerializer(request.user, context={'request': request}).data)

    def put(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(UserSerializer(user, context={'request': request}).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SkillViewset(viewsets.ReadOnlyModelViewSet):
    # MultiPartParser AND FormParser
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    # "You will typically want to use both FormParser and MultiPartParser
    # together in order to fully support HTML form data."
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name','title','description']
    search_fields = ['name','title','description']

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encoded_jwt = jwt.encode(
            {"pk": str(user.pk)}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(
            data={"access": user.get_tokens(), "data": UserSerializer(user, context={'request': request}).data})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)