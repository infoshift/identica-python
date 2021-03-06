import unittest
from identica import Entity, Identica
import httpretty
import json


@httpretty.activate
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
        self.assertEqual(User(identica=Identica(url='non-test')).identica.url,
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

    def test_find_by_id(self):
        mock_data = {'id': 1,
                     'first_name': 'Jesse',
                     'last_name': 'Panganiban'}

        httpretty.register_uri(httpretty.GET,
                               'http://localhost:3000/identica/users/1',
                               body=json.dumps(mock_data),
                               content_type='application/json')

        i = Identica(url='http://localhost:3000/identica')
        Entity.entity = 'users'
        Entity.identica = i
        e = Entity.find_by_id(1)

        self.assertIsInstance(e, Entity)
        self.assertEqual(e._properties, mock_data)
        self.assertEqual(e.identica, i)

    def test_find_by_id_not_found(self):
        httpretty.register_uri(httpretty.GET,
                               'http://localhost:3000/identica/users/1',
                               body=None,
                               content_type='application/json',
                               status=404)

        i = Identica(url='http://localhost:3000/identica')
        Entity.entity = 'users'
        Entity.identica = i
        e = Entity.find_by_id(1)
        self.assertIsNone(e)

    def test_save_new(self):
        mock_data = {
            'id': 1,
            'email': 'testing@testing.com',
            'passsword': 'blahblah',
            'password_confirmation': 'blahblah',
            'first_name': 'Jesse',
            'last_name': 'Panganiban'
        }

        httpretty.register_uri(httpretty.POST,
                               'http://localhost:3000/identica/users',
                               body=json.dumps(mock_data),
                               content_type='application/json')

        i = Identica(url='http://localhost:3000/identica')
        e = Entity(identica=i, entity='users',
                   first_name='Jesse',
                   last_name='Panganiban',
                   email='test@testing.com',
                   password='blahblah')
        e.save()

    def test_save_existing(self):
        mock_data = {
            'id': 1,
            'first_name': 'Jesse',
            'last_name': 'Panganiban'
        }

        httpretty.register_uri(httpretty.PUT,
                               'http://localhost:3000/identica/users/1',
                               body=json.dumps(mock_data),
                               content_type='application/json')

        i = Identica(url='http://localhost:3000/identica')
        e = Entity(identica=i, entity='users', id=1,
                   first_name='Jesse', last_name='PanganibanNew')
        e.save()

    def test_destroy(self):
        mock_data = {
            'id': 6,
            'first_name': 'Jesse',
            'last_name': 'Panganiban'
        }

        httpretty.register_uri(httpretty.DELETE,
                               'http://localhost:3000/identica/users/6',
                               body=json.dumps(mock_data),
                               content_type='application/json')

        i = Identica(url='http://localhost:3000/identica')
        e = Entity(identica=i, entity='users', id=6,
                   first_name='Jesse', last_name='Panganiban')
        e.destroy()

    def test_query(self):
        mock_data = {
            'collection': [
                {
                    'id': 1,
                    'first_name': 'Jesse',
                    'last_name': 'Panganiban'
                }
            ]
        }

        httpretty.register_uri(httpretty.GET,
                               'http://localhost:3000/identica/users',
                               body=json.dumps(mock_data),
                               content_type='application/json')
        i = Identica(url='http://localhost:3000/identica')
        Entity.identica = i
        Entity.entity = 'users'
        entities = Entity.query(first_name="Jesse", last_name="Panganiban")
        self.assertIsInstance(entities, list)
        self.assertEqual(len(entities), 1)

    def test_santized_properties(self):
        e = Entity(first_name='Jesse', last_name='Panganiban')
        self.assertEqual(e._sanitized_properties,
                         {'first_name': 'Jesse', 'last_name': 'Panganiban'})

    def test_exclude_properties(self):
        class User(Entity):
            excluded_properties = ['created_at', 'updated_at']

        e = User(first_name='Jesse', last_name='Panganiban',
                 created_at='now', updated_at='now')

        self.assertEqual(e._sanitized_properties,
                         {'first_name': 'Jesse', 'last_name': 'Panganiban'})


if __name__ == '__main__':
    unittest.main()
