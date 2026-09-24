from django.conf import settings
from django.db import migrations, models
from django.utils import timezone
import django.db.models.deletion


def assign_existing_entries(apps, schema_editor):
    Entry = apps.get_model('emotion_logs', 'Entry')

    for entry in Entry.objects.select_related('topic').filter(user__isnull=True):
        entry.user_id = entry.topic.owner_id
        entry.save(update_fields=['user'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emotion_logs', '0004_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='text',
            new_name='experience',
        ),
        migrations.AddField(
            model_name='entry',
            name='date',
            field=models.DateField(default=timezone.localdate),
        ),
        migrations.AddField(
            model_name='entry',
            name='emotion',
            field=models.CharField(default='Other', max_length=20),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RunPython(assign_existing_entries, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
