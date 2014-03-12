from identica import Identica, Entity
import httpretty
import unittest
import json


class TestIdentica(unittest.TestCase):

    def test_url(self):
        """Sanity checks on the 'url' property."""
        class ExtendedIdentica(Identica):
            url = 'http://localhost:3000/identica'

        self.assertEqual(ExtendedIdentica.url,
                         'http://localhost:3000/identica')
        self.assertEqual(ExtendedIdentica().url,
                         'http://localhost:3000/identica')
        self.assertEqual(Identica(url='http://localhost:3000/identica').url,
                         'http://localhost:3000/identica')

    @httpretty.activate
    def test_find_entity_by_id(self):
        mock_data = {'id': 1,
                     'first_name': 'Jesse',
                     'last_name': 'Panganiban'}

        httpretty.register_uri(httpretty.GET,
                               'http://localhost:3000/identica/users/1',
                               body=json.dumps(mock_data),
                               content_type='application/json')

        i = Identica(url='http://localhost:3000/identica')
        e = i.find_entity_by_id('users', 1)

        self.assertIsInstance(e, Entity)
        self.assertEqual(e._properties, mock_data)

    def test_construct_url(self):
        i = Identica(url='http://localhost:3000/identica')
        self.assertEqual(i._construct_url('entities'),
                         'http://localhost:3000/identica/entities')
        self.assertEqual(i._construct_url('entities/5'),
                         'http://localhost:3000/identica/entities/5')

    def test_entity(self):
        i = Identica(url='http://localhost:3000/identica')

        class User(i.Entity):
            entity = 'users'

        self.assertEqual(User.identica, i)
        self.assertEqual(User.identica.url, 'http://localhost:3000/identica')


if __name__ == '__main__':
    unittest.main()
