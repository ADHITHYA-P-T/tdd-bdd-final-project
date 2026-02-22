import os

# Force SQLite in-memory BEFORE importing anything from the service
os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from service import app
from tests import test_models
import unittest

loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_models)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)# run_tests.py

import os

# Force SQLite in-memory BEFORE importing anything from the service
os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from service import app
from tests import test_models
import unittest

# Load the tests from test_models
loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_models)

# Run the tests
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
