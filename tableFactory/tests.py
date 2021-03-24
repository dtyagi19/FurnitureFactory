from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestTable(APITestCase):

    def setUp(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 5, 'length': None,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])
        url = reverse('table_view')
        data = {'name': 'Unittest1', 'leg_id': 1}
        # response = self.client.post('http://localhost:8000/furnitureFactory/tableFactory/table/', data, format='json')
        response = self.client.post(url, data, format='json')
        # print(response.data)
        # response = self.client.post('/furnitureFactory/tableFactory/table/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['leg'], data['leg_id'])

    def test_create(self):
        """
        Ensure we can create a new Table object.
        """
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 10, 'length': None,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])

        # Tables can have legs
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])
        url = reverse('table_view')
        data = {'name': 'Unittest2', 'leg_id': 2}
        # response = self.client.post('http://localhost:8000/furnitureFactory/tableFactory/table/', data, format='json')
        response = self.client.post(url, data, format='json')
        # print(response.data)
        # response = self.client.post('/furnitureFactory/tableFactory/table/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['leg'], data['leg_id'])

        # Legs cannot be shared between tables

        data = {'name': 'Unittest3', 'leg_id': 2}
        with transaction.atomic():
            try:
                response = self.client.post(url, data, format='json')
            except IntegrityError as i:
                self.assertEqual(i.__str__(),
                                 'UNIQUE constraint failed: tableFactory_table.leg_id')

        # Tables have unique names

        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])
        url = reverse('table_view')
        data = {'name': 'Unittest2', 'leg_id': 3}
        with transaction.atomic():
            try:
                response = self.client.post(url, data, format='json')
            except IntegrityError as i:
                self.assertEqual(i.__str__(),
                                 'UNIQUE constraint failed: tableFactory_table.name')

    def test_list(self):
        url = reverse('table_view')
        data = {'name': 'Unittest1', 'leg_id': 1}
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['name'], data['name'])
        self.assertEqual(response_data[0]['leg'], data['leg_id'])

    def test_detail(self):
        url = reverse('table_view')
        data = {'name': 'Unittest1', 'leg_id': 1}
        table_id = 1
        url = url + f"{table_id}/"
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['leg'], data['leg_id'])

    def test_update(self):
        url = reverse('table_view')
        data = {'name': 'Unittest2', 'leg_id': 1}
        table_id = 1
        url = url + f"{table_id}/"
        response = self.client.patch(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['leg'], data['leg_id'])

    def test_update_partial(self):
        url = reverse('table_view')
        data = {'name': 'Unittest2', 'leg_id': 1}
        partial_data = {'name': 'Unittest2'}
        table_id = 1
        url = url + f"{table_id}/"
        response = self.client.patch(url, partial_data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['leg'], data['leg_id'])

    def test_delete(self):
        url = reverse('table_view')
        table_id = 1
        url = url + f"{table_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestLeg(APITestCase):

    def setUp(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 5, 'length': None,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])
        url = reverse('table_view')
        data = {'name': 'Unittest1', 'leg_id': 1}
        # response = self.client.post('http://localhost:8000/furnitureFactory/tableFactory/table/', data, format='json')
        response = self.client.post(url, data, format='json')
        # print(response.data)
        # response = self.client.post('/furnitureFactory/tableFactory/table/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['leg'], data['leg_id'])

    def test_create(self):
        """
        Ensure we can create a new Leg object.
        """
        # Legs can have feet
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 10, 'length': None,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])
        # Feet can be shared between legs
        data = {'name': 'Unittest2', 'feet_id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])

    def test_list(self):
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 1}
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['name'], data['name'])
        self.assertEqual(response_data[0]['feet'], data['feet_id'])

    def test_detail(self):
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 1}
        leg_id = 1
        url = url + f"{leg_id}/"
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['feet'], data['feet_id'])

    def test_update(self):
        url = reverse('leg_view')
        data = {'name': 'Unittest2', 'feet_id': 1}
        leg_id = 1
        url = url + f"{leg_id}/"
        response = self.client.patch(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['feet'], data['feet_id'])

    def test_update_partial(self):
        url = reverse('leg_view')
        data = {'name': 'Unittest2', 'feet_id': 1}
        partial_data = {'name': 'Unittest2'}
        leg_id = 1
        url = url + f"{leg_id}/"
        response = self.client.patch(url, partial_data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['feet'], data['feet_id'])

    def test_delete(self):
        url = reverse('leg_view')
        leg_id = 1
        url = url + f"{leg_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestFeet(APITestCase):

    def setUp(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 5, 'length': None,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])
        url = reverse('leg_view')
        data = {'name': 'Unittest1', 'feet_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['feet'], data['feet_id'])
        url = reverse('table_view')
        data = {'name': 'Unittest1', 'leg_id': 1}
        # response = self.client.post('http://localhost:8000/furnitureFactory/tableFactory/table/', data, format='json')
        response = self.client.post(url, data, format='json')
        # print(response.data)
        # response = self.client.post('/furnitureFactory/tableFactory/table/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['leg'], data['leg_id'])

    def test_create(self):
        """
        Ensure we can create a new Feet object.
        """
        # Feet have optional width, optional length, and optional radius fields
        url = reverse('feet_view')
        data = {'name': 'Unittest2', 'radius': 10, 'length': None,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])

        """
        1. A foot with a radius must not have length or width
        2. A foot with a length must also have a width
        3. A foot with a width must also have a length 
        """

        data = {'name': 'Unittest2', 'radius': 10, 'length': 10,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'name': 'Unittest2', 'radius': 10, 'length': None,
                'width': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'name': 'Unittest2', 'radius': None, 'length': 10,
                'width': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'name': 'Unittest2', 'radius': None, 'length': None,
                'width': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 5, 'length': None,
                'width': None}
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['name'], data['name'])
        self.assertEqual(response.data[0]['radius'], data['radius'])
        self.assertEqual(response.data[0]['length'], data['length'])
        self.assertEqual(response.data[0]['width'], data['width'])

    def test_detail(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 5, 'length': None,
                'width': None}
        feet_id = 1
        url = url + f"{feet_id}/"
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])

    def test_update(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest1', 'radius': 5}
        feet_id = 1
        url = url + f"{feet_id}/"
        response = self.client.patch(url, data)
        print(response)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])

    def test_update_partial(self):
        url = reverse('feet_view')
        data = {'name': 'Unittest2', 'radius': 5, 'length': None,
                'width': None}
        partial_data = {'name': 'Unittest2'}
        feet_id = 1
        url = url + f"{feet_id}/"
        response = self.client.patch(url, partial_data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response.data['radius'], data['radius'])
        self.assertEqual(response.data['length'], data['length'])
        self.assertEqual(response.data['width'], data['width'])

    def test_delete(self):
        url = reverse('feet_view')
        feet_id = 1
        url = url + f"{feet_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
