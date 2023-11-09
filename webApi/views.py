"""
Module : Views for User login Signup and creating a post
"""
import random
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from passlib.hash import django_pbkdf2_sha256 as handler
from decouple import config
from operator import itemgetter
from django.conf import settings

from .serializers import *
from .models import *
from Useable import usable as uc

from Useable import token as _auth
# from Usable import emailpattern as verified
# from Usable.permissions import *


class UserAuthViewset(ModelViewSet):
    @action(detail=False, methods=["post"])
    def signup(self, request):
        try:
            required_field = ["fname", "lname", "email", "password"]
            validator = uc.require_field_validation(
                requestdata=request.data, requirefield=required_field
            )
            if validator["status"]:
                serializer = UserSignupSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"status": True, "message": "User created Successfully"},
                        status=200,
                    )
                return Response(
                    {"status": False, "error": serializer.errors}, status=400
                )
            return Response(
                {
                    "status": validator["status"],
                    "missing_fields": validator["require_field"],
                    "empty_fields": validator["empty_fields"],
                },
                status=400,
            )

        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail= False, methods=['post'])
    def login(self, request):
        try:
            required_field = ["email", "password"]
            validator = uc.require_field_validation(request.data, required_field)
            if validator['status']:
                serializer = UserLoginSerializer(data= request.data)
                if serializer.is_valid():
                    fetch_user = serializer.validated_data['fetch_user']
                    print(fetch_user.id)
                    admin_token = _auth.UserGenerateToken(fetch_user)
                    if admin_token["status"]:
                        return Response(
                            {
                                "status": True,
                                "msg": "Login Successfully",
                                "token": admin_token["token"],
                                "payload": admin_token["payload"],
                            },
                            status=200,
                        )
                    
                    return Response({"status": False, "error": admin_token['message']}, status=400)
                return Response({"status": False, "error": serializer.errors}, status=400)
            return Response(validator, status=400)
        except Exception as e :
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )