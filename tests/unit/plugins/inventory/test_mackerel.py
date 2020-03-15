from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import string

import pytest
from ansible.inventory.data import InventoryData
from ansible.template import Templar
# noinspection PyUnresolvedReferences
from ansible_collections.xcezx.mackerel.plugins.inventory.mackerel import InventoryModule


# noinspection PyUnresolvedReferences
@pytest.fixture(scope='module')
def inventory():
    inventory = InventoryModule()
    inventory.inventory = InventoryData()
    inventory.templar = Templar(None)
    return inventory


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize('path,got', [
    ('mackerel.yml', True),
    ('mackerel.yaml', True),
    ('not_mackerel_config.yml', False),
])
def test_verify_file_bad_config(inventory, tmpdir, path, got):
    config_file = tmpdir.join(path)
    config_file.ensure()
    assert inventory.verify_file(str(config_file)) is got


@pytest.mark.skip()
def test_parse(inventory):
    pass


def test__populate(inventory, faker):
    inventory._options = {
        'strict': False,
        'compose': {
            'ansible_host': 'interfaces[0].ipAddress',
        },
        'groups': {
            'dbservers': "inventory_hostname.startswith('db-')",
        },
        'keyed_groups': [
            {'key': 'status', 'prefix': 'status'},
        ],
    }
    inventory._populate({
        'hosts': [
            {
                'createdAt': faker.unix_time(),
                'id': faker.lexify('???????????', letters=string.ascii_letters + string.digits),
                'name': 'db-master',
                'interfaces': [
                    {'ipAddress': faker.ipv4_private()},
                ],
                'roles': {'my-service': ['db', 'master']},
                'type': 'agent',
                'status': 'working',
            },
            {
                'createdAt': faker.unix_time(),
                'id': faker.lexify('???????????', letters=string.ascii_letters + string.digits),
                'name': 'db-slave01',
                'interfaces': [
                    {'ipAddress': faker.ipv4_private()},
                ],
                'roles': {'my-service': ['db', 'slave']},
                'type': 'agent',
                'status': 'working',
            },
            {
                'createdAt': faker.unix_time(),
                'id': faker.lexify('???????????', letters=string.ascii_letters + string.digits),
                'name': 'db-slave02',
                'interfaces': [
                    {'ipAddress': faker.ipv4_private()},
                ],
                'roles': {'my-service': ['db', 'slave']},
                'type': 'agent',
                'status': 'standby',
            },
        ],
    })

    assert 'mackerel' in inventory.inventory.groups
    assert 'dbservers' in inventory.inventory.groups
    assert 'status_working' in inventory.inventory.groups
    assert 'status_standby' in inventory.inventory.groups

    assert 'db-master' in inventory.inventory.hosts
    host_vars = inventory.inventory.get_host('db-master').get_vars()
    assert 'ansible_host' in host_vars

    assert 'db-slave01' in inventory.inventory.hosts
    host_vars = inventory.inventory.get_host('db-slave01').get_vars()
    assert 'ansible_host' in host_vars

    assert 'db-slave02' in inventory.inventory.hosts
    host_vars = inventory.inventory.get_host('db-slave02').get_vars()
    assert 'ansible_host' in host_vars
