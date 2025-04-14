from django.db import models


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