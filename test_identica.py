from identica import Identica, Entity
import unittest


class TestIdentica(unittest.TestCase):

    def setUp(self):
        self.i = Identica('http://localhost:3000/identica')

    def tearDown(self):
        self.i = None

    def test_find_entity_by_id(self):
        # TODO: Mock this
        user = self.i.find_entity_by_id('users', 1)
        self.assertIsNotNone(user)

        user = self.i.find_entity_by_id('users', 0)
        self.assertIsNone(user)


class TestEntity(unittest.TestCase):

    def setUp(self):
        self.e = Entity(entity='users', id=1, properties={'name': 'awesome'})

    def tearDown(self):
        self.e = None

    def test_get(self):
        self.assertEqual(self.e.get('name'), 'awesome')
        self.assertIsNone(self.e.get('nonexistent'))

    def test_set(self):
        self.e.set('name', 'newname')
        self.assertEqual(self.e.get('name'), 'newname')


if __name__ == '__main__':
    unittest.main()
