from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
)
from .models import UserTable, Visitor

from .serializers import (
    CreateTableSerializer,
    TableShowSerializer,
    VisitorSerializer,
    LetterSerializer,
    UserTableSerializer,
)


# 사용자의 tablelist // admin 만 가능 == OK
class TableShowView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        caketables = UserTable.objects.all()
        caketables_serializer = TableShowSerializer(caketables, many=True)

        response_data = "caketables", caketables_serializer.data

        return Response(response_data, status=HTTP_200_OK)


# 사용자의 테이블(user pk로 구별)
# [get] ALLOWANY - nickname, tablecolor, pickcake, visitor_name
# [post] 테이블 주인만 가능 (본인의 table 생성)
# [delete] 테이블 주인만 가능
class UserTableView(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # owner의 pk로 조회 == OK
    def get_object(self, pk):
        try:
            return UserTable.objects.get(owner=pk)
        except UserTable.DoesNotExist:
            raise NotFound

    # user의 pk로 테이블 조회 == OK
    def get(self, request, pk):
        caketables = UserTable.objects.filter(owner=pk)
        caketables_serializer = TableShowSerializer(caketables, many=True)
        print(caketables_serializer.data)
        return Response(caketables_serializer.data, status=HTTP_200_OK)

    # 로그인 한 유저 테이블 생성 == OK
    def post(self, request, pk):
        user_table = UserTable.objects.filter(owner=pk)
        if user_table:
            return Response(
                data={"message": "이미 생성 된 테이블이 있습니다!"}, status=HTTP_400_BAD_REQUEST
            )
        serializer = CreateTableSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)  # owner 필드 설정
            return Response(data=serializer.data, status=HTTP_201_CREATED)

    # table owner만 table 삭제 가능 == OK
    def delete(self, request, pk):
        try:
            caketable = self.get_object(pk)
        except UserTable.DoesNotExist:
            return Response(
                data={"message": "테이블을 찾을 수 없습니다"}, status=HTTP_404_NOT_FOUND
            )

        if caketable.owner != request.user:
            raise PermissionDenied
        caketable.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# [post] 테이블 주인만 가능 (본인의 table 생성)
class NewTableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        user_table = UserTable.objects.filter(owner=pk)
        if user_table:
            return Response(
                data={"message": "이미 생성 된 테이블이 있습니다!"}, status=HTTP_400_BAD_REQUEST
            )
        request.data["owner"] = request.user.id
        serializer = CreateTableSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)  # owner 필드 설정
            return Response(data=serializer.data, status=HTTP_201_CREATED)


# 로그인 안해도 케이크 고르기 가능 == OK
class VisitorView(APIView):
    # permission_classes = [AllowAny]
    try:
        def get_object(self, pk):
            try:
                return UserTable.objects.get(owner=pk)
            except UserTable.DoesNotExist:
                raise NotFound

        def get(self, request, pk):
                serializer = UserTableSerializer(self.get_object(pk))
                return Response(serializer.data)
        
        def post(self, request, pk):
            user = self.get_object(pk)
            serializer = VisitorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=user)
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    except Exception as e:
            print(e)
            raise Response(status=HTTP_400_BAD_REQUEST)


# visitor 가 쓴 cake를 pk로 letter 조회 및 삭제 가능 == OK
# table owner만 편지 삭제 가능 == OK
class LetterView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, visitor_pk):
        return get_object_or_404(Visitor, pk=visitor_pk)

    def get(self, request, pk, visitor_pk):
        visitor = self.get_object(visitor_pk)
        if request.user == visitor.owner.owner:
            serializer = LetterSerializer(visitor)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({"detail": "접근 권한이 없습니다."}, status=HTTP_403_FORBIDDEN)

    def delete(self, request, pk, visitor_pk):
        visitor = self.get_object(visitor_pk)

        if request.user == visitor.owner.owner:
            visitor.delete()
            return Response(status=HTTP_204_NO_CONTENT)