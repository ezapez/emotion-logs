from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('emotion_logs', '0005_simplify_to_emotion_entries'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={
                'ordering': ['-date', '-date_added'],
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.AlterField(
            model_name='entry',
            name='emotion',
            field=models.CharField(
                choices=[
                    ('Happy', 'Happy'),
                    ('Sad', 'Sad'),
                    ('Angry', 'Angry'),
                    ('Anxious', 'Anxious'),
                    ('Calm', 'Calm'),
                    ('Excited', 'Excited'),
                    ('Other', 'Other'),
                ],
                max_length=20,
            ),
        ),
    ]
