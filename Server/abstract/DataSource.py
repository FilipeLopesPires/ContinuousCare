from abc import ABC, abstractmethod, abstractproperty
import json


class DataSource(ABC):

    def __init__(self, token, refreshToken, uuid, user, id, location):
        super().__init__()
        self._token=token
        self._refreshToken=refreshToken
        self._uuid=uuid
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
        return json.loads(self._headerTemplate.replace("TOKEN", self._token))

    @property
    def refreshHeader(self):
        return json.loads(self._refreshHeaderTemplate.replace("REFRESH_TOKEN", self._refreshToken))

    @property
    def refreshData(self):
        return json.loads(self._refreshDataTemplate.replace("REFRESH_TOKEN", self._uuid))

    def update(self, token, refreshToken, uuid, user, id, location):
        self._token=token
        self._refreshToken=refreshToken
        self._uuid=uuid
        self._user=user
        self._id=id

    @abstractproperty
    def metrics(self):
        return []

    @abstractproperty
    def _headerTemplate(self):
        return ""

    @abstractproperty
    def _refreshHeaderTemplate(self):
        return ""

    @abstractproperty
    def _refreshURL(self):
        return ""

    @abstractproperty
    def _refreshDataTemplate(self):
        return ""


    @abstractmethod
    def refreshToken(self):
        pass
