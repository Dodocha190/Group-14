#assert what is in controllers.py
#python -m unittest unitTests.py

from app import create_application
from app.config import TestConfig
# need to add 

class UnitTests(unittest.TestCase):
    def setUp(self):
        testApplication = create_application(TestConfig)
        return super().setUp()
    
    def test_add_unit_form(self):
        #PLACEHOLDER: to update
        form = AddUnitForm()
        self.assertIsInstance(form, AddUnitForm)

    def tearDown(self):
        return super().tearDown()