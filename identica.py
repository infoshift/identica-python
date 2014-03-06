import requests


def _construct_entity_url(identica_url, entity, id=None, suffix=None):
    """
    Constructs a url given an entity, id, and a suffix.

    /<entity>/<action>
    /<entity>/<id>/<action>
    """
    if id is None:
        url = "%s/%s" % (identica_url, entity)
    else:
        url = "%s/%s/%s" % (identica_url, entity, id)
    if suffix:
        url += suffix
    return url


class Entity(object):

    identica_url = None
    entity = None

    def __init__(self, identica_url=None, entity=None, id=None,
                 properties=None):
        self.identica_url = self.identica_url or identica_url
        self.entity = self.entity or entity
        self.id = id

        self._properties = properties

    def get(self, property):
        """
        Getter.
        """
        return self._properties.get(property, None)

    def set(self, property, value):
        """
        Setter.
        """
        self._properties[property] = value

    def delete(self):
        """
        Completely deletes this entity identica.
        """
        pass

    def update(self, *args, **kwags):
        """
        Updates this entity's properties.
        """
        pass

    def save(self, *args, **kwargs):
        """
        Syncs this entity with the identica server.
        """
        pass

    @classmethod
    def create(cls, entity, *args, **kwargs):
        """
        Creates an instance of this entity.
        """
        pass

    @classmethod
    def find_by_id(cls, identica_url, entity, id):
        """
        Queries a single instance of an entity.
        """
        url = _construct_entity_url(identica_url, entity, id, suffix='.json')
        response = requests.get(url)
        if response.status_code == 200:
            return cls(identica_url, entity, id, response.json())
        return None

    @classmethod
    def find_by_property(cls, entity, property, value):
        """
        Queries a single instance of an entity by a property.
        """
        pass


class Identica(object):

    def __init__(self, identica_url=None):
        self.identica_url = identica_url

    def find_entity_by_id(self, entity, id):
        """
        Finds an instance of an entity by id.
        """
        return Entity.find_by_id(self.identica_url, entity, id)

    def find_entity_by_property(self, entity, property, value):
        """
        Finds an instance of an entity by a property.
        """
        pass
