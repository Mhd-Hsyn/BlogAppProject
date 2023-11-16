from rest_framework import serializers
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import *
from Useable import usable as uc


class UserSignupSerializer(serializers.ModelSerializer):
    """Signup Serializer with validation"""

    class Meta:
        model = User
        fields = ["fname", "lname", "email", "password", "profile"]

    def validate_email(self, email):
        """Email validation for unique"""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f"{email} already exists")
        return email

    def validate_password(self, password):
        """Password length validation and Password return in hash form"""
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
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        fetch_user = User.objects.filter(email=email).first()
        if not fetch_user:
            raise serializers.ValidationError(f"{email} account not found")
        check_pass = handler.verify(password, fetch_user.password)
        if not check_pass:
            raise serializers.ValidationError("incorrect password")
        attrs["fetch_user"] = fetch_user
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class AddBlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "category_id", "user_id"]

    def validate(self, attrs):
        user_id = self.context["user_id"]
        fetch_user = User.objects.filter(id=user_id).first()
        if not fetch_user:
            raise serializers.ValidationError(f"{user_id} not authenticate")
        attrs["user_id"] = fetch_user
        return super().validate(attrs)


class Get_All_BlogPostSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category_id.name", read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "content",
            "category_id",
            "category_name",
            "user_id",
            "full_name",
            "created_at",
        ]

    def get_full_name(self, obj):
        return f"{obj.user_id.fname} {obj.user_id.lname}"


class Edit_My_Post_Serializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category_id.name", read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "category_id", "category_name"]

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.content = validated_data["content"]
        instance.category_id = validated_data["category_id"]
        instance.save()
        return instance


class Add_Comment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "content", "blog_post_id", "created_at"]

    def create(self, validated_data):
        validated_data["user_id"] = self.context
        return super().create(validated_data)


class Edit_My_Comment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "content"]

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
