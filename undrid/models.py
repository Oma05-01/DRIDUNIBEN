
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from djongo import models as djongo_models
from bson import ObjectId


CATEGORY_CHOICES = [
    ('Research', 'Research'),
    ('Innovation', 'Innovation'),
    ('Development', 'Development'),
]


class Faculty(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.title}"

    class Meta:
        verbose_name_plural = "Faculties"
        ordering = ['code']


class Department(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.code} - {self.title}"

    class Meta:
        ordering = ['code']


class Contributor(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, null=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, default='')
    profile_image = models.ImageField(
        upload_to='contributors/profiles/',
        blank=True,
        null=True
    )

    def delete(self, *args, **kwargs):
        # Clear the M2M relationships first
        if hasattr(self, 'articles'):
            self.articles.clear()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.email} | {self._id}"

    class Meta:
        db_table = 'contributors'  # Explicit collection name

    @classmethod
    def to_python(cls, value):
        """Convert string to ObjectId for proper form handling"""
        if isinstance(value, str):
            return ObjectId(value)
        return value

    def get_id(self):
        return str(self._id)


class Article(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, null=False)

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField(max_length=500)
    cover_photo = models.ImageField(upload_to='articles/covers/')
    contributors = models.ManyToManyField(Contributor, related_name='articles')
    researcher = models.ForeignKey(
        Contributor,
        on_delete=models.SET_NULL,
        related_name='researched_articles',
        null=True,
        blank=True,
        default=""
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        # Clear the M2M relationships first
        self.contributors.clear()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | {self._id}"

    @property
    def id(self):
        return str(self._id)