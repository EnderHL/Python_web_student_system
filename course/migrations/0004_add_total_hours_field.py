from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0003_course_teaching_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="total_hours",
            field=models.IntegerField(default=0, verbose_name="总课时"),
            preserve_default=False,
        ),
    ]