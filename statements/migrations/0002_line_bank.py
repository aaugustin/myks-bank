from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='bank',
            field=models.CharField(default='LCL', max_length=20, verbose_name='banque', choices=[('CA', 'Cr\xe9dit Agricole'), ('LCL', 'Cr\xe9dit Lyonnais')]),
            preserve_default=False,
        ),
    ]
