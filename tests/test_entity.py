import unittest
from identica import Entity


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
        self.assertEqual(Entity('tests').entity, 'tests')

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


if __name__ == '__main__':
    unittest.main()
