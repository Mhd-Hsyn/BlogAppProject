"""
module : Models.py for creating and initilizing table
"""

from django.db import models
import uuid


class BaseModel(models.Model):
    """
    BaseModel inherit by all tables which has same key,  
    This table and its fields are abstract (hidden)
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True, blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, auto_now_add=False, null=True, blank=True
    )

    class Meta:
        abstract = True


class User(BaseModel):
    """User Table For Their Information"""

    fname = models.CharField(max_length=50, default="")
    lname = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    profile = models.ImageField(
        upload_to="User/Profile", default="User/Profile/dummy.png"
    )

    def __str__(self) -> str:
        return str(self.email)
    
class UserJWTWhiteListToken(models.Model):
    """
    JWT token store in this table for perticular user
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank= True)
    token = models.TextField(default="")
    created_at = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True, blank=True
    )


class Category(BaseModel):
    """Category table for BlogPost belongs to which category"""

    name = models.CharField(max_length=50, default="")
    description = models.TextField(default="")

    def __str__(self) -> str:
        return str(self.name)


class BlogPost(BaseModel):
    """
    Blog Post where title and Content of post
    add category forienkey to identify the blog post category
    and add user foreign key
    """

    title = models.CharField(max_length=50, default="")
    content = models.TextField(default="")
    image = models.ImageField(upload_to="Blog/", default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self) -> str:
        return str(self.title)


class Comments(BaseModel):
    """Comments on Blog Post"""

    content = models.TextField(default="")
    blog_post_id = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, blank=True, null=True
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f"Comment by {self.user_id.fname} on {self.blog_post_id.title} Blog Post"
