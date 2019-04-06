import unittest
from flask import jsonify, Flask
from flask_sieve.exceptions import ValidationException, register_error_handler

class MockApp:
    def __init__(self):
        self.error_handlers = {}

    def register_error_handler(self, ExceptionClass, fn):
        self.error_handlers[ExceptionClass.__name__] = fn



class TestErrorHandler(unittest.TestCase):
    def test_error_handler(self):
        app = Flask(__name__)
        register_error_handler(app)
        self.assertIn(ValidationException, app.error_handler_spec[None][None])
        errors = {'field': 'Test error'}

        with app.app_context():
            response, status = app.error_handler_spec[None][None][ValidationException](
                ValidationException(errors)
            )
        self.assertEqual(400, status)
        self.assertIn('Test error', str(response.get_json()))
