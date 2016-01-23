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


from .model import Page

from zephyr.orm import BaseMapper
import db

__all__ = ['PageMapper']

class PageMapper(BaseMapper):

    table = 'pages'
    model = Page

    def find(self, pid):
        data = db.select(self.table).fields('parent', 'name', 'title', 'slug',
            'content', 'status', 'redirect', 'show_in_menu', 'pid').condition('pid', pid).execute()
        if data:
            return self.load(data[0], self.model)


    def find_by_redirect(self, redirect):
        data = db.select(self.table).fields('parent', 'name', 'title', 'slug',
            'content', 'status', 'redirect', 'show_in_menu', 'pid').condition('redirect', redirect).execute()
        if data:
            return self.load(data[0], self.model)

    def find_by_slug(self, slug):
        data = db.select(self.table).fields('parent', 'name', 'title', 'slug',
            'content', 'status', 'redirect', 'show_in_menu', 'pid').condition('slug', slug).execute()
        if data:
            return self.load(data[0], self.model)

    def menu(self, is_menu=False):
        q = db.select(self.table).fields('parent', 'name', 'title', 'slug',
            'content', 'status', 'redirect', 'show_in_menu', 'pid').condition('show_in_menu', 1)
        if not is_menu:
            res = q.execute()
        else:
            res = q.condition('status', 'published').order_by('menu_order').execute()
        return [self.load(data,self.model) for data in res]


    def dropdown(self, show_empty_option=True, exclude=[]):
        items = []
        if show_empty_option:
            items.append((0, '--'))

        pages = db.select(self.table).fields('pid', 'name').execute()
        for page in pages:
            if page[0] in exclude:
                continue
            items.append((page[0], page[1]))

        return items

    def count(self, status=None):
        q= db.select(self.table).fields(db.expr('COUNT(*)'))
        if status != 'all':
            q.condition('status', status)
        return q.execute()[0][0]


    def count_slug(self, slug):
        return db.select(self.table).fields(db.expr('COUNT(*)')).condition('slug', slug).execute()[0][0]

    def paginate(self, page=1, perpage=10, status='all'):
        q = db.select(self.table).fields('parent', 'name', 'title', 'slug',
            'content', 'status', 'redirect', 'show_in_menu', 'pid')
        if status != 'all':
            q.condition('status', status)
        results = q.limit(perpage).offset((page - 1) * perpage).order_by('title', 'desc').execute()
        pages = [self.load(page, self.model) for page in results]
        return pages

    def create(self, page):
        row = []
        for _ in ('parent', 'name', 'title', 'slug', 'content', 'status', 'redirect', 'show_in_menu'):
            row.append(getattr(page, _))
        return db.insert(self.table).fields('parent', 'name', 'title', 'slug',
            'content', 'status', 'redirect', 'show_in_menu').values(row).execute()
          
    def save(self, page):
        q = db.update(self.table)
        data = dict( (_, getattr(page, _)) for _ in ('parent', 'name', 
                'title', 'slug', 'content', 'status', 'redirect', 'show_in_menu'))
        q.mset(data)
        return q.condition('pid', page.pid).execute()

    def update_menu_order(self, pid, menu_order):
        return db.update(self.table).condition('pid', pid).set('menu_order', menu_order).execute()
        
    def delete(self, page_id):
        return db.delete(self.table).condition('pid', page_id).execute()
        