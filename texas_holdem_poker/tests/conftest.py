import pytest
import logging


def pytest_configure(config):
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@pytest.fixture(autouse=True, scope="session")
def setup_session():
    # Setup code that runs once before any tests
    print("Test session setup")
    yield
    print("Test session teardown")

