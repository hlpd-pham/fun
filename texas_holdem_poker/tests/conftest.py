import logging


def pytest_configure(config):
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def pytest_itemcollected(item):
    if item.obj.__doc__:
        # Replace newlines in docstrings with spaces to avoid breaking the output format
        item._nodeid = (
            f"{item._nodeid} - {' '.join(str(item.obj.__doc__).strip().split())}"
        )
