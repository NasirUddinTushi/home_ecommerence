# Generated by Django 5.2.4 on 2025-07-29 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Forestland Linen', max_length=255)),
                ('site_tagline', models.CharField(blank=True, max_length=255)),
                ('logo_url', models.ImageField(blank=True, null=True, upload_to='site/logo/')),
                ('top_bar_message', models.CharField(blank=True, max_length=255)),
                ('default_currency', models.CharField(default='BDT', max_length=10)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20, null=True)),
                ('whatsapp_text', models.CharField(blank=True, help_text='Default message for WhatsApp pre-filled chat', max_length=255, null=True)),
                ('instagram_handle', models.CharField(blank=True, max_length=100)),
                ('copyright_text', models.CharField(blank=True, max_length=255)),
                ('footer_cert_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn'), ('youtube', 'YouTube'), ('whatsapp', 'WhatsApp')], max_length=50)),
                ('url', models.URLField(max_length=500)),
            ],
        ),
    ]
