from google.cloud import ndb
from datetime import datetime

try:
    client = ndb.Client.from_service_account_json("datastore-services.json")
except:
    client = ndb.Client()


class HistoricalData(ndb.Model):
    createdOn = ndb.DateTimeProperty(auto_now_add=True)
    fileLink = ndb.StringProperty()
    processedText = ndb.StringProperty()

    @classmethod
    def create_new(cls, **kwargs):
        with client.context():
            obj = cls()
            for attribute, value in kwargs.items():
                setattr(obj, attribute, value)
            obj.createdOn = datetime.today()
            key = obj.put()
            return key

    @classmethod
    def get_historical_data(cls, limit=5, offset=0):
        return_list = []
        new_offset = 0
        with client.context():
            historical_obj = HistoricalData.gql("ORDER BY createdOn desc").fetch(limit=int(limit), offset=int(offset))
            for a_obj in historical_obj:
                return_list.append({
                    "imageUrl": a_obj.fileLink,
                    "processedText": a_obj.processedText
                })
            if len(historical_obj) == limit:
                new_offset = limit + offset
        return return_list, new_offset
