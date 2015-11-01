
from zephyr.orm import BaseMapper
import db
from .model import Pair

__all__ = ['PairMapper']

class PairMapper(BaseMapper):

    model = Pair
    table = 'storage'

    def lists(self, exclude=None, sorted=False):
        q = db.select(self.table)
        if sorted:
            q.sort_by('key')
        if exclude:
            db.condition('key', exculde, '<>')
        res = q.execute()
        return [self.load(row, self.model) for row in res]

    def find(self, key):
        data = db.select(self.table).condition('key', key).execute()
        if data:
            return self.load(data[0], self.model)

    def save(self, pair):
        return db.insert(self.table).values((pair.key, pair.value, pair.type)).execute()

    def update(self, pair):
        return db.update(self.table).set('value', pair.value).condition('key', pair.key).execute()

    def delete(self, pair):
        return db.delete(self.table).condition('key', pair.key).condition('type', pair.type).execute()
