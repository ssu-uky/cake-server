from django.urls import path
from . import views



urlpatterns = [
    # 카카오 로그인
    
    path("signin/kakao/", views.KakaoSignView.as_view()), # 카카오 로그인 
    path("info/", views.UserInfoView.as_view()), # 유저 정보 확인
    
    # 127.0.0.1:8000/api/users/list/
    path("list/", views.UserList.as_view()), # 유저 리스트 조회 (admin용)
    path("list/<int:pk>/", views.UserDetailList.as_view()), # 유저 리스트 조회 (admin용)
    path("mypage/", views.Mypage.as_view()), # mypage 조회 및 삭제
    
    path("feedback/", views.FeedbackView.as_view()), # 피드백 등록
    
    ### 이메일 로그인 ###
    path("signup/",views.SignUp.as_view()), # 이메일 인증 필요 없음
    path("signup/email/",views.EmailSignUp.as_view()), # 이메일 인증 필요
    path("login/findpw/",views.FindPassword.as_view()), # 비밀번호 찾기
    path("login/resetpw/<int:pk>/",views.ResetPassword.as_view()), # 비밀번호 재설정
    path("login/",views.Login.as_view()),
    path("logout/",views.Logout.as_view()),

]
