# Generated by Django 3.2.16 on 2022-11-06 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadastro',
            name='ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Preferencias_Paises',
            fields=[
                ('ID_Cadastro', models.AutoField(primary_key=True, serialize=False)),
                ('cod_pais', models.CharField(max_length=10)),
                ('cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cadastro')),
            ],
        ),
        migrations.CreateModel(
            name='Preferenciais_Tempo',
            fields=[
                ('ID_Cadastro', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_templo', models.CharField(max_length=50)),
                ('cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cadastro')),
            ],
        ),
    ]