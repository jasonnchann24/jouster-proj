from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, filters
from api.common import permissions as commonPermissions
from api.user_accounts.serializers import (
    GroupSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserCreateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ["username", "email"]
    filterset_class = UserFilter
    ordering_fields = ["date_joined", "username", "email"]
    ordering = ["-date_joined"]

    def get_permissions(self):
        if self.action == "create":
            return []
        elif self.action in ["update", "partial_update"]:
            return [commonPermissions.IsOwner()]
        elif self.action == "destroy":
            return [permissions.IsAdminUser()]

        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "create":
            return UserCreateSerializer

        return UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
