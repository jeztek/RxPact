from django.db import models

from helpers import epochMilliToString


# Customized QuerySet and Manager adapted from:
# http://davyd.livejournal.com/262241.html
class SerializedQuerySet(models.query.QuerySet):
    def __init__ (self, model = None, *args, **kwargs):
        super(SerializedQuerySet, self).__init__ (model, *args, **kwargs)

    def serialize(self):
        return [e.serialize() for e in self]

    def with_timezone(self, timezone):
        return [e.with_timezone(timezone) for e in self]


class SerializedManager(models.Manager):
    def __init__ (self, *args, **kwargs):
        super(SerializedManager, self).__init__ (*args, **kwargs)
		
    def get_query_set(self):
        return SerializedQuerySet(self.model)
	
    def serialize(self):
        return self.get_query_set().serialize()


