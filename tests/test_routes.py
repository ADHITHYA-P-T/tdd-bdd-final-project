######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
######################################################################
"""
Product API Service Test Suite
"""
import os
import logging
from decimal import Decimal
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, init_db, Product
from tests.factories import ProductFactory

# Disable logging for tests
# logging.disable(logging.CRITICAL)

# Use SQLite for testing to avoid PostgreSQL connection issues
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")

BASE_URL = "/products"


class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        # Remove old SQLite file for fresh start
        if os.path.exists("test.db"):
            os.remove("test.db")

        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()
        if os.path.exists("test.db"):
            os.remove("test.db")

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ############################################################
    # Basic tests
    ############################################################
    def test_index(self):
        """It should return the index page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Product Catalog Administration", response.data)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["message"], "OK")

    ############################################################
    # CREATE tests
    ############################################################
    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_with_no_name(self):
        """It should not Create a Product without a name"""
        product = self._create_products()[0]
        new_product = product.serialize()
        del new_product["name"]
        response = self.client.post(BASE_URL, json=new_product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ############################################################
    # READ tests
    ############################################################
    def test_get_product(self):
        """It should Read a Product by ID"""
        products = self._create_products(1)
        test_product = products[0]

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"], test_product.id)
        self.assertEqual(data["name"], test_product.name)
        self.assertEqual(data["description"], test_product.description)
        self.assertEqual(str(data["price"]), str(test_product.price))
        self.assertEqual(data["available"], test_product.available)
        self.assertEqual(data["category"], test_product.category.name)

    def test_get_product_not_found(self):
        """It should return 404 if Product not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # UPDATE tests
    ############################################################
    def test_update_product(self):
        """It should Update a Product"""
        products = self._create_products(1)
        test_product = products[0]

        updated_data = {
            "name": "Updated Name",
            "description": "Updated Description",
            "price": "99.99",
            "available": False,
            "category": test_product.category.name,
        }

        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["name"], updated_data["name"])
        self.assertEqual(data["description"], updated_data["description"])
        self.assertEqual(str(data["price"]), updated_data["price"])
        self.assertEqual(data["available"], updated_data["available"])

    def test_update_product_not_found(self):
        """It should return 404 when updating non-existent product"""
        updated_data = {"name": "Nothing"}
        response = self.client.put(f"{BASE_URL}/0", json=updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # DELETE tests
    ############################################################
    def test_delete_product(self):
        """It should Delete a Product"""
        products = self._create_products(1)
        test_product = products[0]

        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Confirm it no longer exists
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product_not_found(self):
        """It should return 404 when deleting non-existent product"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # LIST tests
    ############################################################
    def test_list_all_products(self):
        """It should List all Products"""
        self._create_products(3)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_list_products_by_name(self):
        """It should filter Products by name"""
        products = self._create_products(2)
        target_name = products[0].name
        response = self.client.get(f"{BASE_URL}?name={target_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["name"] == target_name for p in data))

    def test_list_products_by_category(self):
        """It should filter Products by category"""
        products = self._create_products(2)
        target_category = products[0].category.name
        response = self.client.get(f"{BASE_URL}?category={target_category}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["category"] == target_category for p in data))

    def test_list_products_by_availability(self):
        """It should filter Products by availability"""
        products = self._create_products(3)
        response = self.client.get(f"{BASE_URL}?available=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["available"] is True for p in data))