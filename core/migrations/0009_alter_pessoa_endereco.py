# Generated by Django 5.1.7 on 2025-06-01 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_endereco_pessoa_endereco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='endereco',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.endereco', verbose_name='Endereço'),
        ),
    ]
