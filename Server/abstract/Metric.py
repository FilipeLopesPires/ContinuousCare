from abc import ABC, abstractmethod, abstractproperty

class Metric(ABC):

    def __init__(self, dataSource):
        super().__init__()
        self.dataSource = dataSource

    @property
    def url(self):
        return self.URLTemplate.replace("UUID", self.dataSource._uuid)

    @abstractproperty
    def URLTemplate():
        return ""

    @abstractproperty
    def updateTime():
        return 0

    @abstractproperty
    def metricType():
        return ""

    @abstractproperty
    def metricLocation():
        return ""

    @abstractmethod
    def getData(self, latitude=None, longitude=None):
        pass

    @abstractmethod
    def normalizeData(self, jsonData):
        pass
