from django.db import migrations, models
import django.db.models.deletion

def create_default_endereco(apps, schema_editor):
    Endereco = apps.get_model('core', 'Endereco')
    # Cria um endereço padrão para evitar erro de FK
    Endereco.objects.create(
        bairro='Bairro Padrão',
        rua='Rua Padrão',
        numero='0',
        cep='00000000',
        complemento=''
    )

def set_default_endereco(apps, schema_editor):
    Pessoa = apps.get_model('core', 'Pessoa')
    Endereco = apps.get_model('core', 'Endereco')
    default_endereco = Endereco.objects.first()  # Pega o primeiro endereço
    Pessoa.objects.all().update(endereco=default_endereco)  # Atualiza registros

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_pessoa_email_pessoa_nome_pessoa_telefone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bairro', models.CharField(default='', max_length=45, verbose_name='Bairro')),
                ('rua', models.CharField(default='', max_length=45, verbose_name='Rua')),
                ('numero', models.CharField(default='', max_length=10, verbose_name='Número')),
                ('cep', models.CharField(default='', max_length=10, verbose_name='CEP')),
                ('complemento', models.CharField(blank=True, default='', max_length=45, null=True, verbose_name='Complemento')),
            ],
        ),
        migrations.RunPython(create_default_endereco),  # Cria um endereço padrão
        migrations.AddField(
            model_name='pessoa',
            name='endereco',
            field=models.ForeignKey(
                null=True,  # Permite NULL temporariamente
                on_delete=django.db.models.deletion.PROTECT,
                to='core.endereco',
                verbose_name='Endereço'
            ),
        ),
        migrations.RunPython(set_default_endereco),  # Preenche registros existentes
        migrations.AlterField(
            model_name='pessoa',
            name='endereco',
            field=models.ForeignKey(
                null=False,  # Agora torna obrigatório
                on_delete=django.db.models.deletion.PROTECT,
                to='core.endereco',
                verbose_name='Endereço'
            ),
        ),
    ]