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
