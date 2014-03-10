import unittest
from identica import Entity, Identica
import httpretty
import json


class TestEntity(unittest.TestCase):

    def setUp(self):
        self.e = Entity(test_prop='test prop')

    def tearDown(self):
        self.e = None

    def test_entity(self):
        """Sanity checks on the 'entity' property"""
        class User(Entity):
            entity = 'users'

        self.assertEqual(User.entity, 'users')
        self.assertEqual(User().entity, 'users')

        # Setting the entity name to 'tests'
        self.assertEqual(Entity(entity='tests').entity, 'tests')

    def test_identica(self):
        """Sanity checks on the 'identica' property"""
        class User(Entity):
            identica = Identica(url='test')

        self.assertEqual(User.identica.url, 'test')
        self.assertEqual(User().identica.url, 'test')
        self.assertEqual(User(identica=Identica('non-test')).identica.url,
                         'non-test')

    def test_properties(self):
        """Sanity checks on the Entity 'properties'."""
        data = {'first_name': 'First Name', 'last_name': 'Last Name'}
        self.assertEqual(Entity(**data)._properties, data)

    def test_get(self):
        self.assertEqual(self.e.get('test_prop'), 'test prop')

    def test_set(self):
        self.e.set('test_prop', 'new value')
        self.assertEqual(self.e.get('test_prop'), 'new value')

    def test_id(self):
        """
        If given an id as a property, it should be
        accessbile as an instance property as well.
        """
        e = Entity(id=5)
        self.assertEqual(e.id, 5)

    @httpretty.activate
    def test_find_by_id(self):
        mock_data = {'id': 1,
                     'first_name': 'Jesse',
                     'last_name': 'Panganiban'}

        httpretty.register_uri(httpretty.GET,
                               'http://localhost:3000/identica/users/1',
                               body=json.dumps(mock_data),
                               content_type='application/json')

        i = Identica(url='http://localhost:3000/identica')
        e = Entity.find_by_id(i, 'users', 1)

        self.assertIsInstance(e, Entity)
        self.assertEqual(e._properties, mock_data)


if __name__ == '__main__':
    unittest.main()
