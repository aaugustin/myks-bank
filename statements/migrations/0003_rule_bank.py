from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("statements", "0002_line_bank")]

    operations = [
        migrations.AddField(
            model_name="rule",
            name="bank",
            field=models.CharField(
                choices=[
                    ("BB", "Boursorama Banque"),
                    ("CA", "Crédit Agricole"),
                    ("LCL", "Crédit Lyonnais"),
                ],
                default="LCL",
                max_length=20,
                verbose_name="banque",
            ),
            preserve_default=False,
        )
    ]
