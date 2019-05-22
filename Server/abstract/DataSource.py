from abc import ABC, abstractmethod, abstractproperty
import json


class DataSource(ABC):

    def __init__(self, authentication_fields, user, id, location):
        super().__init__()
        self._authentication_fields = authentication_fields
        self._user=user
        self._id=id
        self._location=location

    @property
    def user(self):
        return self._user
    
    @property
    def id(self):
        return self._id

    @property
    def header(self):
        return json.loads(self._headerTemplate.replace("TOKEN", self._authentication_fields["token"]))

    @abstractproperty
    def refreshHeader(self):
        pass

    @abstractproperty
    def refreshData(self):
        pass

    def update(self, authentication_fields, location):
        self._authentication_fields = authentication_fields
        self._location = location

    @abstractproperty
    def metrics(self):
        return []

    @abstractproperty
    def _headerTemplate(self):
        return ""

    @abstractproperty
    def _refreshURL(self):
        return ""

    @abstractmethod
    def refreshToken(self):
        pass
