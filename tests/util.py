from flask.ext.testing import TestCase as FlaskTestCase

class TestCase(FlaskTestCase):
    def setUp(self):
        pass

    def setUpFixtures(self):
        pass
        
    def tearDown(self):
        pass
