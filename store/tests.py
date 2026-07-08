from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Order, OrderItem


class StoreTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='shopper', email='shopper@example.com', password='shopperpass'
        )
        self.category = Category.objects.create(name='Gear')
        self.product = Product.objects.create(
            name='Training Gloves',
            category=self.category,
            price=Decimal('29.99'),
            stock=5,
        )

    def test_add_to_cart_and_checkout_reduces_stock(self):
        self.client.login(username='shopper', password='shopperpass')

        response = self.client.post(
            reverse('add-to-cart', kwargs={'slug': self.product.slug}),
            {'quantity': 2},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Added Training Gloves to your cart.')

        response = self.client.post(
            reverse('checkout'),
            {
                'full_name': 'Shopper One',
                'email': 'shopper@example.com',
                'phone': '+1234567890',
                'address': '123 Market Street',
                'city': 'City',
                'state': 'State',
                'zip_code': '12345',
                'country': 'United States',
                'payment_method': 'card',
                'notes': 'Please ship quickly.',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order')

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.item_count(), 2)
        self.assertEqual(order.subtotal, Decimal('59.98'))
        self.assertEqual(order.shipping_cost, Decimal('499.00'))
        self.assertEqual(order.total, Decimal('563.78'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_checkout_fails_when_insufficient_stock(self):
        self.product.stock = 1
        self.product.save()
        self.client.login(username='shopper', password='shopperpass')

        response = self.client.post(
            reverse('add-to-cart', kwargs={'slug': self.product.slug}),
            {'quantity': 2},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('checkout'),
            {
                'full_name': 'Shopper One',
                'email': 'shopper@example.com',
                'phone': '+1234567890',
                'address': '123 Market Street',
                'city': 'City',
                'state': 'State',
                'zip_code': '12345',
                'country': 'United States',
                'payment_method': 'card',
                'notes': 'Please ship quickly.',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Insufficient stock for Training Gloves')
        self.assertFalse(Order.objects.filter(user=self.user).exists())
