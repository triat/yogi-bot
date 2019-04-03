# Allow pytest to access the DB
import pytest


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass
