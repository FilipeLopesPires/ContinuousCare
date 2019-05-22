from abc import ABC, abstractmethod, abstractproperty

class Metric(ABC):

    def __init__(self, dataSource):
        super().__init__()
        self.dataSource = dataSource

    @property
    def url(self):
        uuid = self.dataSource._authentication_fields.get("uuid")
        if uuid:
            return self.URLTemplate.replace("UUID", uuid)
        return self.URLTemplate

    @abstractproperty
    def URLTemplate(self):
        return ""

    @abstractproperty
    def updateTime(self):
        return 0

    @abstractproperty
    def metricType(self):
        return ""

    @abstractproperty
    def metricLocation(self):
        return ""

    @abstractmethod
    def getData(self, latitude=None, longitude=None):
        pass

    @abstractmethod
    def normalizeData(self, jsonData):
        pass

    def checkEvent(self, normalJsonData):
        return None
