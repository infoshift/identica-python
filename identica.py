import requests
import json


def nested_object(name, mapping):
    return [(u'{}[{}]'.format(name, key), value) for key, value
            in mapping.iteritems()]


class Identica(object):

    url = None
    default_headers = {
        'content-type': 'application/json'
    }

    def __init__(self, url=None):
        self.url = url or self.url

    def find_entity_by_id(self, entity, id):
        """
        Finds a single instance of entity from the server
        given the id.
        """
        cls = Entity
        cls.entity = entity
        cls.identica = self
        return cls.find_by_id(id)

    def _request(self, url, method='get', headers={}, data={},
                 params={}):
        headers.update(self.default_headers)
        return getattr(requests, method)(url, headers=headers, data=data,
                                         params=nested_object('query', params))

    def _construct_url(self, endpoint):
        return "%s/%s" % (self.url, endpoint)

    def configure(self, url=None):
        self.url = url

    @property
    def Entity(self):
        Entity.identica = self
        return Entity


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

        r = self.identica._request(url, method=method,
                                   data=json.dumps({
                                       'resource': self._properties
                                   }))
        self._properties = r.json()

        return self

    def destroy(self):
        """
        Destroys this entity in the identica server.
        """
        url = '%s/%s/%s' % (self.identica.url, self.entity, self.id)
        self.identica._request(url, method='delete')
        return self

    @classmethod
    def find_by_id(cls, id):
        r = cls.identica._request("%s/%s/%s" %
                                  (cls.identica.url, cls.entity, id))
        if r.status_code != 200:
            return None
        return cls(**r.json())

    @classmethod
    def query(cls, identica, entity=None, **query):
        r = identica._request("%s/%s" % (identica.url, entity or cls.entity),
                              params=query)
        data = r.json()
        return [cls(**d) for d in data.get('collection', [])]
