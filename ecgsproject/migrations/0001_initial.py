# Generated by Django 3.2.5 on 2021-09-02 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ecgsproject.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', ecgsproject.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id_resultat', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nb_h_tot_prest_ann', models.PositiveIntegerField(blank=True, null=True)),
                ('utilisation_inutile', models.PositiveIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id_personne', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nom', models.CharField(max_length=200)),
                ('prenom', models.CharField(max_length=200)),
                ('mail', models.EmailField(max_length=200, unique=True)),
                ('tel', models.CharField(max_length=20)),
                ('entreprise', models.CharField(max_length=200)),
                ('fonction', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Integrateur',
            fields=[
                ('id_integrateur', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('adr_entreprise', models.CharField(max_length=250)),
                ('tva', models.CharField(max_length=14, unique=True)),
                ('lieu_fonction', models.CharField(max_length=250)),
                ('id_personne', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.personne')),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id_employe', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('lieu_fonction', models.CharField(max_length=250)),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_integrateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.integrateur')),
                ('id_personne', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.personne')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id_client', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('adr_entreprise', models.CharField(max_length=250)),
                ('num_contrat', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('num_licence', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('statut', models.CharField(choices=[('Interessé', 'Interessé'), ('Abonné', 'Abonné')], max_length=200)),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.employe')),
                ('id_personne', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.personne')),
                ('id_resultat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecgsproject.resultat')),
            ],
        ),
    ]
