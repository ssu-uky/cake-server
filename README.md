<div align="center">
 <br>
 
 ![logo](https://github.com/ssu-uky/cake-server/assets/101565486/54099092-0640-42e2-b130-bda0aabafb38)
 <br>

# 🎂 네가 꾸민 케이크
사용자의 생일에 축하메세지를 전해주는 롤링페이퍼 서비스입니다.

<br/>
 
</div>

---

## 목차
- [Intro](#intro)
- [Skills](#skills)
- [Installation](#installation)
- [API Documents](#api-documents)
- [Architecture](#architecture)
- [Function](#function)
- [Authors](#authors)
- [References](#references)

<br/>

---

## Intro

<https://www.naekkukae.store/>

"네가 꾸민 케이크"는 롤링페이퍼 형식의 생일 축하 서비스 입니다. <br>
방문자는 생일자의 테이블에 전시 할 케이크를 선택하고, 익명으로 편지를 작성합니다. <br>
작성한 편지는 생일자의 테이블에 전시되며 테이블 주인만 확인할 수 있습니다. <br>
이를 통해 생일자에게 축하와 응원 메시지를 전달하며, 특별하고 소중한 추억을 만들어 줍니다. <br>

---

## Skills
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) &nbsp;
![Django](https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=Django&logoColor=white) &nbsp;
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white) &nbsp;
![NCP](https://img.shields.io/badge/NCP-03C75A.svg?style=for-the-badge&logo=Naver&logoColor=white) &nbsp;
![Kakao](https://img.shields.io/badge/Kakao-FFCD00.svg?style=for-the-badge&logo=KakaoTalk&logoColor=black) &nbsp;


---

## Installation

```py
pip install -r requirements.txt
python manage.py runserver
```

---

## API-Documents 

[API 문서](https://birthday-cake.gitbook.io/naekkukae/)
<https://birthday-cake.gitbook.io/naekkukae/>

---

## Architecture

<img width="800" alt="cake-architecture" 
src="https://i.postimg.cc/BQHLx0YF/cake-architecture.png">

----

## Function

 #### 회원가입 
  ```
   - 회원가입 유형 구분 (Email or Kakao)
   - 회원의 고유 아이디를 uuid로 설정하여 보안 강화
   - 사용자 이름 글자 수 검사 (2자 이상) 
   - Email 중복 검사
   - Email 가입 시 인증 메일 확인 후 계정 활성화
   - 비밀번호 유효성 검사 
   - 관리자 회원인지 일반 사용자 인지 구분
   - DB 데이터 저장
  ```

    
 #### 로그인 & 로그아웃
  ```
   - DB 값 검증
   - Email 로그인
   - 카카오 로그인
   - ID, PW 일치 불일치 검증
   - PW 변경 시 Email로 전송된 링크에서만 변경 가능
   - Simple-JWT 토큰을 사용해서 사용자 보안 강화
   - 로그인 방식에 따라서 Session Storage / Local Storage 토큰 분리
  ```


 #### 메인 페이지
  ```
   - 메인 페이지에 Kakao/Email 로그인 버튼이 있음
        -> Kakao 로그인 클릭 시 회원이면 로그인 / 회원이 아니라면 회원가입 진행
        -> Email 로그인 클릭 시 회원가입 버튼 노출
  ```


 #### Sidebar
 ```
   - Sidebar에서 "내 테이블 보기" 클릭 시
        -> 테이블이 없을 경우, 테이블 생성 페이지로 이동
        -> 테이블이 존재할 경우, 만든 테이블로 이동
   - FeedBack 제출 가능 (로그인 한 유저만 가능)
        -> 로그인 한 이름, 이메일이 자동으로 채워져서 피드백 내용만 입력하면 됨.
  ```

   
 #### 사용자 페이지 (케이크를 놓을 테이블 생성)
  ```
   - 테이블에 사용할 닉네임 지정
   - 테이블 색 color 코드로 지정
   - 본인의 테이블 링크 복사 가능 -> 친구에게 복사한 링크 전달
   - 케이크 안에 쓰여있는 편지는 로그인 한 사용자(테이블 주인)만 확인 가능
   - 케이크 개수 확인 가능
  ```
 
 #### 방문자
  ```
   - 생일인 사용자의 테이블에는 누구나 방문 가능.
   - 방문자는 "방문자 닉네임","방문자 비밀번호"를 입력하고, 케이크를 선택 후, 편지를 쓰면 테이블에 전시가 되면서 테이블이 꾸며짐.
   - 익명으로 남길 수 있음.
   - 편지 작성 시 비속어를 작성하면 필터링 되어 편지 전송이 되지 않음.
  ```

---

## Authors

|position|name|profile|email|
|------|---|----|----|
|Front|이은빈|[@leeeunbin219](https://github.com/leeeunbin219)|leeeunbin219@gmail.com|
|Back+Front|이수현|[@ssu-uky](https://github.com/ssu-uky)|id_suhyun@naver.com|


Discord와 Github를 활용하여 협업

---

## References
[내 트리를 꾸며줘](https://colormytree.me/)