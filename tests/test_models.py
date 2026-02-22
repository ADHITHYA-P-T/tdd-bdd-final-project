# -----------------------------
# Force SQLite in-memory before importing models
# -----------------------------
from service import app
import unittest
import logging
from decimal import Decimal
from service.models import Product, Category, db
from tests.factories import ProductFactory

app.config["TESTING"] = True
app.config["DEBUG"] = False

######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # Initialize the database with SQLite in-memory
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should create a product and assert that it exists"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertIsNotNone(product)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()

        # Assert that it was assigned an id
        self.assertIsNotNone(product.id)

        products = Product.all()
        self.assertEqual(len(products), 1)

        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    def test_read_a_product(self):
        """It should read a product from the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        self.assertIsNotNone(product.id)

        found = Product.find(product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)
        self.assertEqual(found.available, product.available)
        self.assertEqual(found.category, product.category)

    def test_update_a_product(self):
        """It should update a product in the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        new_description = "Updated Description"
        product.description = new_description
        product.update()

        # Fetch product back
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.description, new_description)

    def test_delete_a_product(self):
        """It should delete a product from the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should list all products"""
        products = Product.all()
        self.assertEqual(products, [])

        for _ in range(5):
            p = ProductFactory()
            p.id = None
            p.create()

        all_products = Product.all()
        self.assertEqual(len(all_products), 5)

    def test_find_by_name(self):
        """It should find products by name"""
        products = []
        for _ in range(5):
            p = ProductFactory()
            p.id = None
            p.create()
            products.append(p)

        name_to_find = products[0].name
        found = Product.find_by_name(name_to_find).all()  # <-- .all() added
        count = sum(1 for p in products if p.name == name_to_find)
        self.assertEqual(len(found), count)
        for p in found:
            self.assertEqual(p.name, name_to_find)

    def test_find_by_availability(self):
        """It should find products by availability"""
        products = []
        for _ in range(10):
            p = ProductFactory()
            p.id = None
            p.create()
            products.append(p)

        avail = products[0].available
        found = Product.find_by_availability(avail).all()  # <-- .all() added
        count = sum(1 for p in products if p.available == avail)
        self.assertEqual(len(found), count)
        for p in found:
            self.assertEqual(p.available, avail)

    def test_find_by_category(self):
        """It should find products by category"""
        products = []
        for _ in range(10):
            p = ProductFactory()
            p.id = None
            p.create()
            products.append(p)

        cat = products[0].category
        found = Product.find_by_category(cat).all()  # <-- .all() added
        count = sum(1 for p in products if p.category == cat)
        self.assertEqual(len(found), count)
        for p in found:
            self.assertEqual(p.category, cat)