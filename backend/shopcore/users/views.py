import logging

logger = logging.getLogger(__name__)

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .permissions import IsAdminGroupUser
from .serializers import CustomUserSerializer, LoginSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class InfoView(APIView):
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)

        logger.info(f"User info requested: {user.email}")

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        logger.info(f"Logout request received for user: {request.user}")
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @method_decorator(csrf_exempt)
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            logger.info(f"Login successful for user: {email}")
            return Response({
                "message": "Login successful",
                "user_id": user.id
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Login failed for user: {email}")
            if not CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"message": "No user with this email found"}, status=401)
            return JsonResponse({"message": "Invalid password or user is inactive"}, status=401)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"User registered successfully: {request.data.get('email')}")
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminGroupUser]

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return self.list(request, *args, **kwargs)
        return JsonResponse({"message": "Not authorized to view all users."}, status=403)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminGroupUser]

    def get(self, request, *args, **kwargs):
        # Nur der Benutzer selbst oder ein Admin kann die Details abrufen
        user = self.get_object()
        if request.user.id == user.id or request.user.is_staff:
            return self.retrieve(request, *args, **kwargs)
        return JsonResponse({"message": "Not authorized to view this user."}, status=403)

    def put(self, request, *args, **kwargs):
        # Nur der Benutzer selbst oder ein Admin kann seine Daten ändern
        user = self.get_object()
        if request.user.id == user.id or request.user.is_staff:
            return self.update(request, *args, **kwargs)
        return JsonResponse({"message": "Not authorized to update this user."}, status=403)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if request.user == user:
            if 'is_active' in request.data or 'is_staff' in request.data:
                return JsonResponse({"message": "You cannot change your own is_active or is_staff status."},
                                status=403)

        if 'is_active' in request.data:
            new_is_active = request.data['is_active']
            if new_is_active != user.is_active:
                if user.is_superuser:
                    return JsonResponse({"message": "You cannot change is_active status of a superuser."},
                                    status=403)
                if not request.user.is_staff:
                    return JsonResponse({"message": "You do not have permission to update is_active."},
                                    status=403)

        if 'is_staff' in request.data:
            new_is_staff = request.data['is_staff']
            if new_is_staff != user.is_staff:
                if not request.user.is_superuser:
                    return JsonResponse({"message": "You do not have permission to update is_staff."},
                                    status=403)
                if user.is_superuser:
                    return JsonResponse({"message": "You cannot change is_staff of a superuser."},
                                    status=403)

        if request.user.is_staff or request.user.is_superuser:
            return self.update(request, *args, **kwargs)

        return JsonResponse({"message": "Not authorized to update this user."}, status=403)

    def delete(self, request, *args, **kwargs):
        # Nur Admins dürfen Benutzer löschen
        if request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        return JsonResponse({"message": "Not authorized to delete this user."}, status=403)
