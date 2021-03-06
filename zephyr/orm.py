#!/usr/bin/env python
#
# Copyright 2015-2016 zephyr
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import db


class BaseMapper(object):

    def load(self, data, o):
        return o(*data)


class PrimaryTrait(object):

    def findByKey(self, **kw):
        q = db.select(self.table)
        for k, v in kw.items():
            q.condition(k, v)
        data = q.query()
        if data:
            return self.load(data[0], self.model)
