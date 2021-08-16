import unittest
import sys
from flask import Flask
from app import create_app, db
from app.models import User, Student, Teacher, Admin

app = create_app('testing')


class TestCaseBase(unittest.TestCase):

  def setUp(self):
    ctx = app.app_context()
    ctx.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def login(client, email, password):
    return client.post('/login', data=dict(
      email=email,
      password=password), follow_redirects=True)


class MainTesting(TestCaseBase, unittest.TestCase):

  def test_homepage(self):
    tester = app.test_client(self)
    response = tester.get('/', content_type='html/text')
    self.assertEqual(response.status_code, 200)

  def test_teacher_page(self):
    tester = app.test_client(self)
    response = tester.get('/teachers', content_type='html/text')
    self.assertEqual(response.status_code, 200)

  def test_schedule_page(self):
    tester = app.test_client(self)
    response = tester.get('/schedule', content_type='html/text')
    self.assertEqual(response.status_code, 200)

  def test_login(self):
    tester = app.test_client(self)
    response = tester.post('/login',
                           data=dict(username="user", password="user"),
                           follow_redirects=True)
    self.assertTrue(b'You were logged in!', response.data)

class AdminTesting(TestCaseBase, unittest.TestCase):

  def test_user(self):
    user = Admin(password="admin", email="admin@admin.com")
    db.session.add(user)
    db.session.commit()

    assert user in db.session
