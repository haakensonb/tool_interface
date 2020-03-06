# Generated by Django 2.2.6 on 2020-03-06 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_auto_20191117_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrypRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('secret', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RoleEdges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('secret', models.CharField(max_length=100)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='interface.CrypRole')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='interface.CrypRole')),
            ],
        ),
    ]
