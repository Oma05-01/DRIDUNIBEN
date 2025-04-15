# Generated by Django 3.1.12 on 2025-04-15 14:30

import bson.objectid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, default=bson.objectid.ObjectId, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.TextField(blank=True, default='')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='contributors/profiles/')),
            ],
            options={
                'db_table': 'contributors',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='undrid.faculty')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, default=bson.objectid.ObjectId, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Research', 'Research'), ('Innovation', 'Innovation'), ('Development', 'Development')], max_length=50)),
                ('content', models.TextField(max_length=500)),
                ('cover_photo', models.ImageField(upload_to='articles/covers/')),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('contributors', models.ManyToManyField(related_name='articles', to='undrid.Contributor')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='undrid.department')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
