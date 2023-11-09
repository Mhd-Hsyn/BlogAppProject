from rest_framework import serializers
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import *
from Useable import usable as uc


class UserSignupSerializer(serializers.ModelSerializer):
    """ Signup Serializer with validation """
    class Meta:
        model = User
        fields = ['fname', 'lname', 'email', 'password', 'profile']

    def validate_email(self, email):
        """ Email validation for unique """
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError(f"{email} already exists")
        return email
    
    def validate_password(self, password):
        """ Password length validation and Password return in hash form """
        validator = uc.check_pass_len(password)
        if validator is False:
            raise serializers.ValidationError("password length must be greater than 8")
        # password convert to hash
        password = handler.hash(password)
        return password
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        fetch_user = User.objects.filter(email = email).first()
        if not fetch_user:
            raise serializers.ValidationError(f"{email} account not found")
        check_pass = handler.verify(password, fetch_user.password)
        if not check_pass:
            raise serializers.ValidationError("incorrect password")
        attrs['fetch_user'] = fetch_user
        return attrs