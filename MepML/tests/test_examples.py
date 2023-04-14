# from datetime import date
# from unittest import skip, skipIf, skipUnless
# from unittest import mock
# from rest_framework.test import APIRequestFactory, APITestCase

# from rest_framework import status

# from MepML.models import Professor, User
# from MepML.serializers import ProfessorSerializer
# from MepML.views import getAllProfessors

# # https://www.20tab.com/en/blog/test-python-mocking/
# # https://www.django-rest-framework.org/api-guide/testing/
# # Create your tests here.

# class TestTesting(APITestCase):

#     @skip("Not implemented")
#     def test_testing(self):
#         self.assertTrue(True)

    
#     @skipIf(True, "Not implemented")
#     def test_testing2(self):
#         self.assertTrue(True)


# class test_get_all_professors(APITestCase):
#     def setUp(self):
#         self.client = APIRequestFactory()

#         #Create Professor
#         user = User.objects.create_user(username="João Mário", email="jm@ua.pt")
#         self.p1 = Professor.objects.create(user=user, name="João Mário", email="jm@ua,pt")

#         #Create Professor
#         user = User.objects.create_user(username="Rafa Silva", email="rs@ua.pt")
#         self.p2 = Professor.objects.create(user=user, name="Rafa Silva", email="rs@ua.pt")

#     def test_get_all_professors(self):
#         # Get professors from api call
#         request = self.client.get('/professors/')
#         response = getAllProfessors(request)

#         # Get Professors from directly from database
#         professors = Professor.objects.all()
#         serializer = ProfessorSerializer(professors, many=True)

#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # Mock the Professor.objects.all() method
#     @mock.patch('MepML.views.Professor.objects.all')
#     def test_get_all_professors(self, mock_professors):
#         # Define the return value for the mocked Professor.objects.all() method
#         mock_professors.return_value = [
#             Professor(name='João Mário', user=User(username="João Mário", email="jm@ua.pt")),
#             Professor(name='Rafa Silva', user=User(username="Rafa Silva", email="rs@ua.pt")),
#             Professor(name='Gonçalo Ramos', user=User(username="Gonçalo Ramos", email="gr@ua.pt")),
#         ]

#         # Create a GET request to the getAllProfessors view
#         request = self.client.get('/professors/')
#         response = getAllProfessors(request)

#         # Check that the response status code is 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check that the response data matches the expected serialized data
#         expected_data = ProfessorSerializer(mock_professors.return_value, many=True).data
#         self.assertEqual(response.data, expected_data)

#         # Check that the mock Professor.objects.all() method was called once
#         # mock_professors.assert_called_once()

    