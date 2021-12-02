from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from company.models import Company, Product, Category, Card, Table, Cart, Formula


class CompanyModelTest(TestCase):
    """Tests for the Company model."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Restaurant",
            address1="123 Main St",
            city="Paris",
            country="France",
            zip_code=75001,
            _location=Point(2.3522, 48.8566),
            slug="test-restaurant-75001",
            company_code="4ZZZ",
        )

    def test_company_str(self):
        self.assertEqual(str(self.company), "Test Restaurant")

    def test_company_slug(self):
        self.assertEqual(self.company.slug, "test-restaurant-75001")

    def test_company_location(self):
        location = self.company.get_location()
        self.assertEqual(location[0], 2.3522)
        self.assertEqual(location[1], 48.8566)

    def test_company_code_is_set(self):
        self.assertEqual(len(self.company.company_code), 4)


class ProductModelTest(TestCase):
    """Tests for the Product model."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Restaurant",
            address1="123 Main St",
            city="Paris",
            zip_code=75001,
            _location=Point(0, 0),
            slug="test-restaurant-75001",
            company_code="4ZZZ",
        )
        self.product = Product.objects.create(
            name="Steak Frites",
            price=Decimal("18.50"),
            description="Grilled steak with french fries",
            company=self.company,
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Steak Frites")

    def test_product_slug_auto_generated(self):
        self.assertEqual(self.product.slug, "steak-frites")

    def test_product_price(self):
        self.assertEqual(self.product.price, Decimal("18.50"))

    def test_product_default_available(self):
        self.assertTrue(self.product.available)


class CategoryModelTest(TestCase):
    """Tests for the Category model."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Restaurant",
            address1="123 Main St",
            city="Paris",
            zip_code=75001,
            _location=Point(0, 0),
            slug="test-restaurant-75001",
            company_code="4ZZZ",
        )
        self.category = Category.objects.create(
            name="Entrees",
            company=self.company,
            vat=Decimal("20.00"),
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Entrees")

    def test_category_slug_auto_generated(self):
        self.assertEqual(self.category.slug, "entrees")


class CardModelTest(TestCase):
    """Tests for the Card model."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Restaurant",
            address1="123 Main St",
            city="Paris",
            zip_code=75001,
            _location=Point(0, 0),
            slug="test-restaurant-75001",
            company_code="4ZZZ",
        )
        self.card = Card.objects.create(
            name="Lunch Menu",
            description="Available Mon-Fri",
            company=self.company,
        )

    def test_card_str(self):
        self.assertEqual(str(self.card), "Lunch Menu")

    def test_card_slug_auto_generated(self):
        self.assertEqual(self.card.slug, "lunch-menu")


class TableModelTest(TestCase):
    """Tests for the Table model."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Restaurant",
            address1="123 Main St",
            city="Paris",
            zip_code=75001,
            _location=Point(0, 0),
            slug="test-restaurant-75001",
            company_code="4ZZZ",
        )
        self.table = Table.objects.create(
            table_no=1,
            table_code="A1",
            company=self.company,
        )

    def test_table_str(self):
        self.assertEqual(str(self.table), "Table:1")

    def test_table_belongs_to_company(self):
        self.assertEqual(self.table.company, self.company)


class CartModelTest(TestCase):
    """Tests for the Cart model."""

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Restaurant",
            address1="123 Main St",
            city="Paris",
            zip_code=75001,
            _location=Point(0, 0),
            slug="test-restaurant-75001",
            company_code="4ZZZ",
        )
        self.table = Table.objects.create(
            table_no=1,
            table_code="A1",
            company=self.company,
        )
        self.cart = Cart.objects.create(
            person_name="John Doe",
            total_amount=Decimal("25.00"),
            paid_amount=Decimal("25.00"),
            discount=Decimal("0.00"),
            payment_method="CB",
            company=self.company,
            table=self.table,
        )

    def test_cart_slug_auto_generated(self):
        self.assertEqual(self.cart.slug, "john-doe")

    def test_cart_payment_method(self):
        self.assertEqual(self.cart.payment_method, "CB")

    def test_cart_belongs_to_table(self):
        self.assertEqual(self.cart.table, self.table)
