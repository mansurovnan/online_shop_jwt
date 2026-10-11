
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token talab qilinadi."},
                status=400,
            )

        try:
            token = RefreshToken(refresh_token)
            if str(token["user_id"]) != str(request.user.pk):
                return Response(
                    {"detail": "Bu token sizga tegishli emas."},
                    status=400,
                )
            token.blacklist()
        except Exception:
            return Response(
                {"detail": "Refresh token noto'g'ri yoki bekor qilingan."},
                status=400,
            )

        return Response({"detail": "Logout muvaffaqiyatli."})
