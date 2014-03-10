import requests


class Identica(object):

    url = None

    def __init__(self, url=None):
        self.url = url or self.url

    def find_entity_by_id(self, entity, id):
        """
        Finds a single instance of entity from the server
        given the id.
        """
        return Entity.find_by_id(self, entity, id)

    def _request(self, url, method='get', headers=None, data=None):
        return getattr(requests, method)(url, headers=headers, data=data)

    def _construct_url(self, endpoint):
        return "%s/%s" % (self.url, endpoint)


class Entity(object):

    entity = None
    identica = None

    def __init__(self, identica=None, entity=None, **kwargs):
        self.identica = identica or self.identica
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

    def save(self):
        """
        Synchronizes this entity with the identica server.
        """
        method = 'post'
        url = '%s/%s' % (self.identica.url, self.entity)

        if self.id:
            method = 'put'
            url = '%s/%s/%s' % (self.identica.url, self.entity, self.id)

        r = self.identica._request(url, method=method)
        self._properties = r.json()

        return self

    @classmethod
    def find_by_id(cls, identica, entity, id):
        r = identica._request("%s/%s/%s" % (identica.url, entity, id))
        return cls(entity, **r.json())
