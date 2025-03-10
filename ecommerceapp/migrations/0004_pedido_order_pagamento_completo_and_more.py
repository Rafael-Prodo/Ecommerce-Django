# Generated by Django 5.1.6 on 2025-03-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0003_alter_pedido_order_cart_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido_order',
            name='pagamento_completo',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='pedido_order',
            name='pagamento_metodo',
            field=models.CharField(choices=[('Dinheiro na Entrega', 'Dinheiro na Entrega'), ('khalti', 'khalti')], default='Dinheiro na Entrega', max_length=20),
        ),
    ]
