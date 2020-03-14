from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible_collections.xcezx.mackerel.plugins.inventory.mackerel import InventoryModule


@pytest.fixture(scope='module')
def inventory():
    return InventoryModule()


def verify_file_bad_config(inventory):
    assert inventory.verify_file('not_mackerel_config.yml') is False
