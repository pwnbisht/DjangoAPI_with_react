from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import UserFiles
from api.serializers.serializers import RegistrationSerializer, LoginSerializer, UserFilesSerializer


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a given user.

    Args:
        user: The user object.

    Returns:
        dict: Dictionary containing 'refresh' and 'access' tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    """
    API view for user registration.
    """
    def post(self, request):
        """
        Handle POST requests for user registration.

        Args:
            request: HTTP request object.

        Returns:
            Response: HTTP response with token or error.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    API view for user login.
    """
    def post(self, request):
        """
        Handle POST requests for user login.

        Args:
            request: HTTP request object.

        Returns:
            Response: HTTP response with success message and token or error.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            password = serializer.data['password']

            # authenticate user
            user = authenticate(email=email, password=password)
            if user is not None:
                # Generate and return JWT tokens
                token = get_tokens_for_user(user)
                return Response({'msg': "Login Successfull", 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {"non_field_errors": ['Email or Password is not valid']}},
                                status=status.HTTP_401_UNAUTHORIZED)


class UserFilesView(generics.ListCreateAPIView):
    """
    API view for listing and creating user files.
    """
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handle file creation requests.

        Args:
            request: HTTP request object.

        Returns:
            Response: HTTP response with created file data or error.
        """
        # Validate the file format
        file_serializer = self.get_serializer(data=request.data)
        file_serializer.is_valid(raise_exception=True)

        if file_serializer.validated_data is None:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Perform the actual creation of a file.

        Args:
            serializer: Serializer object.

        Returns:
            None
        """
        serializer.save(user=self.request.user)
