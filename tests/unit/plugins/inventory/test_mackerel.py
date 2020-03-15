from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible_collections.xcezx.mackerel.plugins.inventory.mackerel import InventoryModule


@pytest.fixture(scope='module')
def inventory():
    return InventoryModule()


@pytest.mark.parametrize('path,got', [
    ('mackerel.yml', True),
    ('mackerel.yaml', True),
    ('not_mackerel_config.yml', False),
])
def test_verify_file_bad_config(inventory, tmpdir, path, got):
    config_file = tmpdir.join(path)
    config_file.ensure()
    assert inventory.verify_file(str(config_file)) is got
