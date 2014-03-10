from identica import Identica, Entity
from mock import Mock
import unittest


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

    def test_entity(self):
        """Must be able to do awesome stuff with the
        identica instance right away."""
        i = Identica()

        i.find_entity_by_id = Mock(return_value=Entity(entity='users', id=1))
        i.find_entity_by_property = \
            Mock(return_value=Entity(entity='users', first_name='Jesse'))

        self.assertIsInstance(i.find_entity_by_id('users', 1), Entity)
        self.assertIsInstance(
            i.find_entity_by_property('users', 'first_name', 'Jesse'),
            Entity
        )

    def test_construct_url(self):
        i = Identica(url='http://localhost:3000/identica')
        self.assertEqual(i._construct_url('entities'),
                         'http://localhost:3000/identica/entities')
        self.assertEqual(i._construct_url('entities/5'),
                         'http://localhost:3000/identica/entities/5')


if __name__ == '__main__':
    unittest.main()
