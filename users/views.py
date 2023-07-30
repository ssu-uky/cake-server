import re
import environ
env = environ.Env()

import requests

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from rest_framework.exceptions import (
    NotFound, ValidationError
)

from config.settings import KAKAO_REST_API_KEY

from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .serializers import (
    UserListSerializer,
    MypageSerializer,
    LoginSerializer,
    SignupSerializer,FeedbackSerializer,
)

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.mail import send_mail

from .models import User


# 유저 리스트 조회
class UserList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


# user pk로 한 명씩 정보 조회 및 삭제
class UserDetailList(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = User.objects.filter(pk=pk)
        user_serializer = UserListSerializer(user, many=True)
        return Response(user_serializer.data, status=HTTP_200_OK)

    def delete(self, request, pk):
        user = User.objects.filter(pk=pk)
        if user:
            return Response({"message": "삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


# 유저 정보 조회 및 삭제 (mypage)
class Mypage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MypageSerializer(user)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


# 카카오 로그인
# http://127.0.0.1:8000/api/users/signin/kakao/
# 카카오 로그인
# http://127.0.0.1:8000/api/users/signin/kakao/
class KakaoSignView(APIView):
    def get(self, request):
        client_id = KAKAO_REST_API_KEY
        redirect_uri = "https://manage.neokkukae.store/auth/kakao/callback"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )


class KakaoCallbackView(APIView):
    def get(self, request):
        try:
            code = request.GET.get("code")
            client_id = KAKAO_REST_API_KEY
            redirect_uri = "https://manage.neokkukae.store/auth/kakao/callback"
            token_request = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                    "code": code,
                },
            )
            token_json = token_request.json()

            error = token_json.get("error", None)

            if error is not None:
                return Response({"message": "INVALD_CODE"}, status=HTTP_400_BAD_REQUEST)

            access_token = token_json.get("access_token")
            refresh_token = token_json.get("refresh_token")

            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            profile_json = profile_request.json()
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)
            nickname = kakao_account.get("profile").get("nickname", None)

        except KeyError:
            return Response({"message": "INVALID_TOKEN"}, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            kakao_user = User.objects.get(email=email)
            tokens = RefreshToken.for_user(kakao_user)
            response = HttpResponseRedirect(
                f"https://neokkukae.store/KakaoLogin?refresh={str(tokens)}&access={str(tokens.access_token)}&user_pk={kakao_user.pk}"
            )
            return response

        else:
            if email:
                user = User.objects.create(
                    email=email,
                    name=nickname,
                    social_type="kakao",
                    is_active=True,  # 이메일 로그인 사용 시 카카오로 회원가입 한 유저는 이메일 인증 필요없음 (항상 is_active=True로 설정)
                )

                tokens = RefreshToken.for_user(user)
                response = HttpResponseRedirect(
                    f"https://neokkukae.store/KakaoLogin?refresh={str(refresh_token)}&access={str(tokens.access_token)}&user_pk={user.pk}"
                )
                # return Response(response, id, status=HTTP_200_OK)
                return response
            else:
                return Response(
                    {"message": "카카오 아이디 혹은 카카오 이메일이 없습니다."},
                    status=HTTP_400_BAD_REQUEST,
                )


# 사용자 정보 조회
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                "user_pk": user.pk,
                "name": user.name,
                "email": user.email,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
        )


## 이메일 가입 // test용 ###
# 이메일 회원가입
class SignUp(APIView):
    def get(self, request):
        return Response({"message": "이름, 이메일, 비밀번호를 입력해주세요."})

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        # birthday = request.data.get("birthday")

        if not password or len(password) < 8:
            return Response({"message": "비밀번호를 8자 이상 입력해주세요."})
        serializer = SignupSerializer(data=request.data)

        if User.objects.filter(email=email).exists():
            return Response({"message": "이미 가입된 이메일입니다."})

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.social_type = "email"
            user.save()
            serializer = SignupSerializer(user)

            # simple jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    # "user": serializer.data,
                    "user_pk": user.pk,
                    "message": "회원가입 성공",
                    "token": {
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                    },
                },
                status=HTTP_200_OK,
            )

            # simple jwt 토큰 => 쿠키에 저장
            # 회원가입 시 토큰 저장 할 필요 없음
            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 이메일 로그인
class Login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response(
                {"message": "이메일과 비밀번호를 입력해주세요."}, status=HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            serializer = LoginSerializer(user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # 세션에 토큰 저장
            request.session["access"] = access_token
            request.session["refresh"] = refresh_token

            # 쿠키에 토큰 저장
            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)

            res = Response(
                {
                    # "user": serializer.data,
                    "user_pk": user.pk,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=HTTP_200_OK,
            )

            return res
        else:
            return Response({"message": "이메일 또는 비밀번호가 없습니다"})


# 로그아웃
class Logout(APIView):
    def post(self, request):
        logout(request)
        response = Response({"message": "로그아웃 성공"}, status=HTTP_200_OK)
        request.session.flush()
        return response


# 이메일 회원가입 // 이메일 인증 ##


class EmailSignUp(APIView):
    def get(self, request):
        return Response({"message": "이름, 이메일, 비밀번호를 입력해주세요."})

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        # birthday = request.data.get("birthday")

        if not password or len(password) < 8:
            return Response({"message": "비밀번호를 8자 이상 입력해주세요."})
        serializer = SignupSerializer(data=request.data)

        if not name or not email:
            return Response({"message": "정보를 다시 확인하고 입력해주세요."})

        if User.objects.filter(email=email).exists():
            return Response({"message": "이미 가입된 이메일입니다."})

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.social_type = "email"
            user.is_active = False
            user.save()
            serializer = SignupSerializer(user)

            # simple jwt 토큰 접근
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            # 이메일 인증메일 보내기
            # current_site = get_current_site(request).domain
            # current_site = "127.0.0.1:8000"
            current_site = "manage.naekkukae.store"
            link = "https://" + current_site + "/verify/" + str(token)  # 이메일 인증 링크
            email_subject = "이메일 인증을 완료해주세요."
            email_body = (
                "안녕하세요." + user.name + "님, 회원이 되어주셔서 감사합니다. \n아래 링크를 클릭하여 이메일 인증을 완료해주세요. \n" + link
            )


            send_mail(
                email_subject,
                email_body,
                env("EMAIL_HOST_USER"),
                [user.email],
            )

            res = Response(
                {
                    # "user": serializer.data,
                    "user_pk": user.pk,
                    "message": "이메일을 인증하여 회원가입을 완료해주세요.",
                    "token": {
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                    },
                },
                status=HTTP_200_OK,
            )
            return res
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 이메일 인증 확인
class VerifyEmail(APIView):
    def get(self, request, token):
        try:
            token = RefreshToken(token)
            user = User.objects.get(id=token["email"])

            print(user)

            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({"message": "이메일 인증이 완료되었습니다."}, status=HTTP_200_OK)
            else:
                return Response(
                    {"message": "이미 인증된 이메일입니다."}, status=HTTP_400_BAD_REQUEST
                )
        except (InvalidToken, TokenError, User.DoesNotExist):
            return Response({"message": "유효하지 않은 토큰입니다."}, status=HTTP_400_BAD_REQUEST)


# 비밀번호 이메일로 재설정
class FindPassword(APIView):
    def post(self, request):
        email = request.data.get("email", None)
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"email": "가입되어 있는 이메일이 존재하지 않습니다."}, status=HTTP_404_NOT_FOUND
                )

            # 이메일에서 재설정 URL 생성
            current_site = "naekkukae.store"
            reset_link = "https://" + current_site + "/login/resetpw/" + str(user.pk)
            email_subject = "비밀번호 재설정 메일입니다."
            email_body = (
                "안녕하세요."
                + user.name
                + "님,\n비밀번호를 재설정하기 위한 링크를 보내드립니다.\n아래 링크를 클릭하여 비밀번호를 재설정해주세요.\n"
                + reset_link
            )

            # 이메일 전송
            send_mail(
                email_subject,
                email_body,
                env("EMAIL_HOST_USER"),
                [user.email],
            )

            return Response(
                {"detail": "비밀번호 재설정 이메일이 발송되었습니다."}, status=HTTP_200_OK
            )
        return Response(
            {"email": "가입된 이메일이 없습니다."},
            status=HTTP_400_BAD_REQUEST,
        )


class ResetPassword(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound
    
    def post(self, request, pk):
        user = self.get_object(pk)
        new_password = request.data.get("new_password")
        check_password = request.data.get("check_password")

        if new_password and new_password == check_password:
            user.set_password(new_password)
            user.save()
            return Response({"detail": "비밀번호가 변경되었습니다."}, status=HTTP_200_OK)
        else:
            raise ValidationError({"detail": "비밀번호를 올바르게 입력해주세요."})
        
        

class FeedbackView(APIView):
    # 로그인 되어있는 사람만 post 가능
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=401)
        # feedback_name = request.data.get("feedback_name")
        # feedback_email = request.data.get("feedback_email")
        # feedback_content = request.data.get("feedback_content")
        # feedback_password = request.data.get("feedback_password")
        
        feedback_content = request.data.get("feedback_content")
        

        feedback_data = {
            "feedback_name": request.user.name,
            "feedback_email": request.user.email,
            "feedback_content": feedback_content,
            # "feedback_password": feedback_password
        }

        serializer = FeedbackSerializer(data=feedback_data)

        if not all(feedback_data.values()):
            return Response({"error": "모든 필드를 작성해야 합니다."}, status=HTTP_400_BAD_REQUEST)

        # if not re.match(r"[^@]+@[^@]+\.[^@]+", feedback_email):
        #     return Response({"error": "유효한 이메일을 입력해야 합니다."}, status=HTTP_400_BAD_REQUEST)

        # if not re.match(r"^(?=.*[a-z])(?=.*[0-9])[a-z0-9]+$", feedback_password):
        #     return Response({"error": "암호는 소문자와 숫자 조합이어야 합니다."}, status=HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            saved_feedback = serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


