import logging

import pytest


def pytest_configure(config):
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@pytest.fixture(autouse=True, scope="session")
def setup_session():
    # Setup code that runs once before any tests
    logging.info("Test session setup")
    yield
    logging.info("Test session teardown")


@pytest.fixture(autouse=True, scope="function")
def setup_teardown_module():
    logging.info("Setup for function")
    yield
    logging.info("Teardown for function")
