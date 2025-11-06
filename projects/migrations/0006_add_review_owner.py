"""
Generated migration to add owner ForeignKey to Review (nullable).
This is created to bring the DB schema in sync with models.py where Review.owner exists.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_options'),
        ('users', '0002_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
