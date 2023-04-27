# Generated by Django 4.2 on 2023-04-27 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_blog_description_alter_blog_procedure'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='dp',
            field=models.FileField(default='default.png', upload_to='photos/userdp'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=150)),
                ('time', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.blog')),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]