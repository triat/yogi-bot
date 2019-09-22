# Generated by Django 2.2.1 on 2019-09-22 12:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('WARMUP', 'Warm up'), ('KNIFE', 'Knife'), ('LIVE', 'Live'), ('PAUSED', 'Paused'), ('OVERTIME', 'Over time'), ('DONE', 'Done'), ('CANCELLED', 'Cancelled')], default='WARMUP', max_length=50)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('skip_veto', models.BooleanField(default=True)),
                ('team_1_score', models.IntegerField(default=0)),
                ('team_2_score', models.IntegerField(default=0)),
                ('veto_mappool', models.CharField(blank=True, max_length=500, null=True)),
                ('max_maps', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tag', models.CharField(blank=True, max_length=10, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ip', models.CharField(blank=True, max_length=15, null=True)),
                ('port', models.IntegerField(blank=True, null=True)),
                ('rcon_password', models.CharField(default=uuid.uuid4, max_length=36)),
                ('running_match', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogi_web.Match')),
            ],
            options={
                'verbose_name': 'Server',
                'verbose_name_plural': 'Servers',
            },
        ),
        migrations.AddField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_1', to='yogi_web.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_2', to='yogi_web.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to='yogi_web.Team'),
        ),
    ]
