from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


class TestUserRegistration(TestCase):

  def setUp(self):
    self.client = APIClient()

  def test_register_user(self):
    payload = {
      'username': 'test',
      'email': 'test@gmail.com',
      'password': 'test@123'
    }

    # test registering with bad request
    response = self.client.post(reverse('register'), format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test registering 
    response = self.client.post(reverse('register'), payload, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['username'], payload['username'])
    self.assertEqual(response.data['email'], payload['email'])


class TestUserLogin(TestCase):

  def setUp(self):
    self.client = APIClient()
    self.username = 'test'
    self.email = 'test@gmail.com'
    self.password = 'test@123'
    payload = {'username':self.username, 'email':self.email,\
               'password':self.password}
    response = self.client.post(reverse('register'), payload, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
  def test_user_login(self):
    # test invalid login
    response = self.client.post(reverse('login'), {'username':'zzz', \
                                'password':'test123'})                             
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test valid login
    response = self.client.post(reverse('login'), {'username':self.username, \
                                'password':self.password})
    import pdb; pdb.set_trace()
    self.assertEqual(response.status_code, status.HTTP_200_OK)                                
    self.assertContains(response, 'id')
    self.assertContains(response, 'token')
    self.assertIsNotNone(response.data['user'])
    self.assertIsNotNone(response.data['token'])
    
