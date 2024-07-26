from datetime import datetime

class Todo:
    def __init__(self, _id, task, status, date):
        self.id = _id
        self.task = task
        self.status = status
        self.date = date

    @classmethod
    def from_mongo_doc(cls, doc):
        return cls(
            _id=str(doc['_id']),
            task=doc['task'],
            status=doc['status'],
            date=doc['date']
        )
