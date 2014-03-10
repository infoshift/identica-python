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
        response = self._request("%s/%s/%s" % (self.url, entity, id))
        return Entity(**response.json())

    def _request(self, url, method='get', headers=None, data=None):
        return getattr(requests, method)(url, headers=headers, data=data)

    def _construct_url(self, endpoint):
        return "%s/%s" % (self.url, endpoint)


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
