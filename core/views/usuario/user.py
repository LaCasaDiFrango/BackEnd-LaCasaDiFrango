from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsAdminUser, IsConsumerUser, IsGuestOrReadOnly

from core.models.usuario.user import User
from core.serializers.usuario.user import UserSerializer, UserListSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]  # Só admin pode ver ou editar outros usuários
        if self.action == 'me':
            return [IsAuthenticated()]  # Qualquer usuário logado pode acessar o próprio perfil
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Return the current authenticated user"""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

