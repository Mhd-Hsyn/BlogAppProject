"""
Module : Views for User login Signup and creating a post
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    CategorySerializer,
    AddBlogPostSerializer,
    Get_All_BlogPostSerializer,
    Edit_My_Post_Serializer,
    Add_Comment_Serializer,
    Edit_My_Comment_Serializer
)
from .models import (
    User,
    Category,
    BlogPost,
    Comments
)
from Useable import usable as uc
from Useable import token as _auth
from Useable.permissions import UserPermission


class UserAuthViewset(ModelViewSet):
    @action(detail=False, methods=["post"])
    def signup(self, request):
        """
        User can Signuo or create account with required fields
        """
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
                        status=201,
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

    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        User can login with his specific credentials
        after successfull login it generate the JWT token
            - The JWT token is stored in a Database named UserJWTWhiteListToken
        """
        try:
            required_field = ["email", "password"]
            validator = uc.require_field_validation(request.data, required_field)
            if validator["status"]:
                serializer = UserLoginSerializer(data=request.data)
                if serializer.is_valid():
                    fetch_user = serializer.validated_data["fetch_user"]
                    user_token = _auth.UserGenerateToken(fetch_user)
                    if user_token["status"]:
                        return Response(
                            {
                                "status": True,
                                "message": "Login Successfully",
                                "token": user_token["token"],
                                "payload": user_token["payload"],
                            },
                            status=200,
                        )

                    return Response(
                        {"status": False, "error": user_token["message"]}, status=400
                    )
                return Response(
                    {"status": False, "error": serializer.errors}, status=400
                )
            return Response(validator, status=400)
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserApi(ModelViewSet):
    """
    User Apis when needs the token,
    Only Authorized and Authenticate Users can access the API
    Permission class Add to this Model View Set
        Permission Class
            1- check the users JWT token
            2- check and Query the JWT-token in User-Whitelist_JWT token table
    """

    permission_classes = [UserPermission]

    @action(detail=False, methods=["GET"])
    def logout(self, request):
        """User can Logout, his/her token will be deleted from table"""
        try:
            token = request.auth  # access from permission class after decode
            fetchuser = User.objects.filter(id=token["id"]).first()
            _auth.UserDeleteToken(fetchuser, request)
            return Response(
                {"status": True, "message": "Logout Successfully"}, status=200
            )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["GET"])
    def category(self, request):
        """
        User can fetch the all categories befory posting the Blog
        """
        try:
            fetch_categories = Category.objects.all()
            ser = CategorySerializer(fetch_categories, many=True)
            return Response({"status": True, "data": ser.data}, status=200)
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["POST", "GET", "PUT", "DELETE"])
    def blog_post(self, request):
        """
        User CRUD rights on His/Her Blog-post
        """
        try:
            if request.method == "POST":
                """
                User can add his post according to category
                """
                required_field = ["title", "content", "category_id"]
                validator = uc.require_field_validation(request.data, required_field)
                if validator["status"]:
                    fetch_cat = Category.objects.filter(
                        id=request.data["category_id"]
                    ).first()
                    if fetch_cat:
                        serializer = AddBlogPostSerializer(
                            data=request.data, context={"user_id": request.auth["id"]}
                        )
                        if serializer.is_valid():
                            serializer.save()
                            return Response(
                                {"status": True, "message": "Blog Added Successfully"},
                                status=201,
                            )
                        return Response(
                            {"status": False, "error": serializer.errors}, status=400
                        )
                    return Response(
                        {"status": False, "error": "Category doesnot exists"}
                    )
                return Response(validator, status=400)

            if request.method == "GET":
                """
                User can get the blog-post with different filteration
                    1- user can fetch all blog-post
                    2- user can fetch only specific category blog-post
                    3- user can fetch and see all detail of any specific blog-post
                """
                category_id = request.data.get("category_id", None)
                post_id = request.data.get("post_id", None)

                if category_id is None and post_id is None:
                    """
                    get all post
                    asscending order on Post category
                    descending order on created_at  =  new first
                    """
                    fetch_posts = BlogPost.objects.all().order_by(
                        "category_id", "-created_at"
                    )
                    serializer = Get_All_BlogPostSerializer(fetch_posts, many=True)
                    return Response(
                        {"status": True, "data": serializer.data}, status=200
                    )

                if category_id is not None:
                    """
                    get all specific category post decending order created_at
                    """
                    fetch_posts = BlogPost.objects.filter(
                        category_id=category_id
                    ).order_by("-created_at")
                    serializer = Get_All_BlogPostSerializer(fetch_posts, many=True)
                    return Response(
                        {"status": True, "data": serializer.data}, status=200
                    )

                if post_id is not None:
                    """
                    Get only 1 post
                    """
                    fetch_posts = BlogPost.objects.filter(id=post_id).first()
                    serializer = Get_All_BlogPostSerializer(fetch_posts)
                    return Response(
                        {"status": True, "data": serializer.data}, status=200
                    )

            if request.method == "PUT":
                """
                User can only edit his uploaded blog post
                User can edit his blog post category and BlogPost fields
                """
                required_field = ["title", "content", "category_id", "post_id"]
                validator = uc.require_field_validation(request.data, required_field)
                if not validator["status"]:
                    return Response(validator, status=400)

                fetch_user = User.objects.filter(id=request.auth["id"]).first()
                fetch_my_post = BlogPost.objects.filter(
                    id=request.data["post_id"], user_id=fetch_user
                ).first()
                if fetch_my_post:
                    serializer = Edit_My_Post_Serializer(
                        instance=fetch_my_post, data=request.data
                    )
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            {
                                "status": True,
                                "message": "updated successfully",
                                "data": serializer.data,
                            },
                            status=200,
                        )
                    return Response(
                        {"status": False, "error": serializer.errors}, status=400
                    )
                return Response(
                    {"status": False, "error": "you can't edit someone else post"},
                    status=400,
                )

            if request.method == "DELETE":
                """
                User can delete the blog-post
                but only the blog-post which specific to user
                """
                post_id = request.data.get("post_id", None)
                if post_id is not None:
                    fetch_user = User.objects.filter(id=request.auth["id"]).first()
                    fetch_my_post = BlogPost.objects.filter(
                        id=post_id, user_id=fetch_user
                    ).first()
                    if fetch_my_post:
                        fetch_my_post.delete()
                        return Response(
                            {
                                "status": True,
                                "message": f"Your Post {fetch_my_post.title} deleted Successfully",
                            },
                            status=200,
                        )
                    return Response(
                        {
                            "status": False,
                            "error": "you can't delete someone else post",
                        },
                        status=400,
                    )
                return Response(
                    {"status": False, "error": "id of post is not available"},
                    status=400,
                )

        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post", "get", "put", "delete"])
    def comments(self, request):
        """
        User rights to comment on the blog-post
        user can see the all comments of the perticular post
        """
        try:
            if request.method == "POST":
                """
                This API help user to Add the comment on every blog-post
                """
                required_field = ["blog_post_id", "content"]
                validator = uc.require_field_validation(request.data, required_field)
                if validator["status"]:
                    fetch_user = User.objects.filter(id=request.auth["id"]).first()
                    serializer = Add_Comment_Serializer(
                        data=request.data, context=fetch_user
                    )
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            {"status": True, "message": "Comment posted Successfully"},
                            status=201,
                        )
                    return Response(
                        {"status": False, "error": serializer.errors}, status=400
                    )
                return Response(validator, status=400)

            if request.method == "GET":
                """
                This API helps user to get all comments on the Specific Post
                """
                blog_post_id = request.data.get("blog_post_id", None)
                if blog_post_id is not None:
                    fetch_post = BlogPost.objects.filter(id=blog_post_id).first()
                    fetch_comments = Comments.objects.filter(blog_post_id=fetch_post)
                    serializer = Add_Comment_Serializer(fetch_comments, many=True)
                    return Response(
                        {"status": True, "message": serializer.data},
                        status=200,
                    )
                return Response(
                    {"status": False, "error": "id of post is not available"},
                    status=400,
                )

            if request.method == "PUT":
                """
                User can only edit his comments from every specific blog-post
                """
                required_field = ["comment_id", "content"]
                validator = uc.require_field_validation(request.data, required_field)
                if not validator["status"]:
                    return Response(validator, status=400)

                fetch_user = User.objects.filter(id=request.auth["id"]).first()
                fetch_comment = Comments.objects.filter(
                    id=request.data.get("comment_id"), user_id=fetch_user
                ).first()
                if fetch_comment:
                    serializer = Edit_My_Comment_Serializer(
                        instance=fetch_comment, data=request.data
                    )
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            {
                                "status": True,
                                "message": "Comment updated successfully",
                                "data": serializer.data,
                            },
                            status=200,
                        )
                    return Response(
                        {"status": False, "error": serializer.errors}, status=400
                    )
                return Response(
                    {
                        "status": False,
                        "error": "you can't edit someone else comment",
                    },
                    status=400,
                )

            if request.method == "DELETE":
                comment_id = request.data.get("comment_id", None)
                if comment_id is not None:
                    fetch_user = User.objects.filter(id=request.auth["id"]).first()
                    fetch_comment = Comments.objects.filter(
                        user_id=fetch_user, id=comment_id
                    ).first()
                    if fetch_comment:
                        fetch_comment.delete()
                        return Response(
                            {"status": True, "message": "Your comment deleted"},
                            status=200,
                        )
                    return Response(
                        {
                            "status": False,
                            "error": "you can't edit someone else comment",
                        },
                        status=400,
                    )
                return Response(
                    {
                        "status": False,
                        "error": "Comment id not found",
                    },
                    status=400,
                )

        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
