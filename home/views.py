from django.shortcuts import render
from rest_framework.decorators import APIView
from .models import Student
from .serializers import StudentSerializer, UserSerializer
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Something went wrong'
            })
        else:
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 200,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'data': serializer.data
            })


class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)
        return Response({
            'status': 200,
            'payload': serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Something went wrong'
            })
        else:
            serializer.save()
            return Response({
                'status': 200,
                'data': serializer.data
            })

    def put(self, request):
        try:
            student = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(student, request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 403,
                    'errors': serializer.errors,
                    'message': 'Something went wrong'
                })
            else:
                serializer.save()
                return Response({
                    'status': 200,
                    'data': serializer.data
                })
        except Exception as e:
            return Response({
                'message': 'invalid id'
            })

    def patch(self, request):
        try:
            student = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(
                student, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'status': 403,
                    'errors': serializer.errors,
                    'message': 'Something went wrong'
                })
            else:
                serializer.save()
                return Response({
                    'status': 200,
                    'data': serializer.data
                })
        except Exception as e:
            return Response({
                'message': e
            })

    def delete(self, request):
        student = Student.objects.get(id=request.data['id'])
        student.delete()
        return Response({
            'status': 200,
            'message': 'The entry is deleted'
        })


# Create your views here.
# @api_view(['GET'])
# def home(request):
#     student_objs = Student.objects.all()
#     serializer = StudentSerializer(student_objs, many = True)
#     return Response({
#         'status': 200,
#         'payload': serializer.data
#     })

# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializer = StudentSerializer(data = data);
#     if not serializer.is_valid():
#         return Response({
#             'status':403,
#             'errors':serializer.errors,
#             'message': 'Something went wrong'
#         })
#     else:
#         serializer.save();
#         return Response({
#             'status': 200,
#             'data': serializer.data
#         })

# @api_view(['PUT'])
# def update_student(request, id):
#     # try:
#         student = Student.objects.get(id = id)
#         serializer = StudentSerializer(student, request.data)
#         if not serializer.is_valid():
#             return Response({
#                 'status':403,
#                 'errors':serializer.errors,
#                 'message': 'Something went wrong'
#             })
#         else:
#             serializer.save();
#             return Response({
#                 'status': 200,
#                 'data': serializer.data
#             })
#     # except Exception as e:
#     #     return Response({
#     #         'message': 'invalid id'
#     #     })


# @api_view(['DELETE'])
# def delete_student(request, slug):
#     student = Student.objects.get(id = slug)
#     student.delete()
#     return Response({
#         'status':200,
#         'message':'The entry is deleted'
#     })
