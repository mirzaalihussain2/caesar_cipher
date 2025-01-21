import pytest
from app import create_app

class TestConfig:
    TESTING = True
    SECRET_KEY = 'test-key'
    PROPAGATE_EXCEPTIONS = True

@pytest.fixture
def test_client():
    app = create_app(TestConfig)

    with app.test_client() as client:
        with app.app_context():
            yield client