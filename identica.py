class Identica(object):

    url = None

    def __init__(self, url=None):
        self.url = url or self.url

    def find_entity_by_id(self, entity, id):
        raise NotImplementedError

    def find_entity_by_property(self, entity, property, value):
        raise NotImplementedError


class Entity(object):

    entity = None

    def __init__(self, entity=None, **kwargs):
        self.entity = entity or self.entity
        self._properties = kwargs

    @property
    def id(self):
        return self.get('id')

    def get(self, property):
        """
        Entity property getter.
        """
        return self._properties.get(property, None)

    def set(self, property, value):
        """
        Entity property setter.
        """
        self._properties[property] = value
        return self.get(property)
