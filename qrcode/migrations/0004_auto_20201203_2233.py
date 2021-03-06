# Generated by Django 3.1.4 on 2020-12-03 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode', '0003_auto_20201203_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='logo',
            name='logo_host',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Black',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('black_host', models.CharField(max_length=100, unique=True)),
                ('black_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qrcode.level')),
            ],
        ),
    ]
