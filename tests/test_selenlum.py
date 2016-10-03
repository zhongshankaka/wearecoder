#! usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            db.create_all()
            Role.insert_roles()

            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role)
            db.session.add(admin)
            db.session.commit()

            threading.Thread(target=cls.app.run).start()

            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.clent.close()
            db.drop_all()
            db.session.remove()
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser  not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://localhost:5000/')

        self.client.find_element_by_link_text(u'登录').click()
        self.assertTrue(u'登录' in self.client.page_source)

        self.client.find_element_by_name(u'邮箱').send_keys('john@example.com')
        self.client.find_element_by_name(u'密码').send_keys('cat')
        self.client.find_element_by_name(u'登录').click()
        self.assertTrue(re.search(u'发表', self.client.page_source))

        self.client.find_element_by_link_text(u'个人资料').click()
        self.assertTrue(u'john' in self.client.page_source)


