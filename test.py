import unittest
from unittest.mock import patch, MagicMock
from main import app, markers, existing_markers
import requests
from geopy.geocoders import Nominatim

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        # reset `existing_markers` and `markers` before each test so they are independent
        existing_markers.clear()
        markers.clear()

    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_update_counseling_route(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for 'Counseling'
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': '200 Varick St, New York, NY 10014',
                    'Name': 'Emergency Shelter Access',
                    'City': 'New York',
                    'Description': 'Provide information and assistance for accessing shelters.',
                    'ContactInfo': 'Sarah Johnson, sarah@email.com',
                    'HoursOfOperation': '05/01/24 - 12/31/24'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = MagicMock(latitude=40.7283, longitude=-74.0047)

            # send the POST request to update counseling markers
            response = client.post('/update/counseling')

            self.assertEqual(response.status_code, 200)
            self.assertIn('status', response.json)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['message'], 'Counseling markers updated')

            self.assertIn((40.7283, -74.0047), existing_markers)
            self.assertEqual(len(markers), 1) 

    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_update_food_route(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for 'Food'
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': '39 Broadway, New York, NY 10006',
                    'Name': 'Food Bank For New York City',
                    'City': 'Somewhere, TX',
                    'Description': 'Food distribution center serving NYC’s hungry.',
                    'ContactInfo': '212-555-3456',
                    'HoursOfOperation': 'Mon-Fri: 8am - 6pm'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = MagicMock(latitude=40.7064, longitude=-74.0132)

            # send the POST request to update food markers
            response = client.post('/update/food')

            self.assertEqual(response.status_code, 200)
            self.assertIn('status', response.json)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['message'], 'Food markers updated')

            print("Markers list after update:", markers)

            self.assertIn((40.7064, -74.0132), existing_markers)
            self.assertEqual(len(markers), 1)  

            # simulate another update to ensure marker is added only once
            response = client.post('/update/food')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(markers), 1)  # marker count should still be 1 since it's already added

    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_duplicate_food_marker_prevention(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for 'Food'
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': '39 Broadway, New York, NY 10006',
                    'Name': 'Food Bank For New York City',
                    'City': 'Somewhere, TX',
                    'Description': 'Food distribution center serving NYC’s hungry.',
                    'ContactInfo': '212-555-3456',
                    'HoursOfOperation': 'Mon-Fri: 8am - 6pm'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = MagicMock(latitude=40.7064, longitude=-74.0132)

            # 1. request should add the marker
            response = client.post('/update/food')
            self.assertEqual(response.status_code, 200)
            self.assertIn((40.7064, -74.0132), existing_markers)
            self.assertEqual(len(markers), 1)  

            # 2. request should not add the marker again
            response = client.post('/update/food')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(markers), 1)  
            self.assertIn((40.7064, -74.0132), existing_markers)  # same marker should still be there


    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_update_healthcare_route(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for 'Healthcare'
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': '462 First Ave, New York, NY 10016',
                    'Name': 'Bellevue Hospital Center',
                    'City': 'New York',
                    'Description': 'Comprehensive health services including mental health care and addiction treatment.',
                    'ContactInfo': '(212) 555-5678',
                    'HoursOfOperation': '24/7'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = MagicMock(latitude=40.7396, longitude=-73.9743)

            # send the POST request to update healthcare markers
            response = client.post('/update/healthcare')

            self.assertEqual(response.status_code, 200)
            self.assertIn('status', response.json)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['message'], 'Healthcare markers updated')

            self.assertIn((40.7396, -73.9743), existing_markers)
            self.assertEqual(len(markers), 1) 

    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_update_outreach_route(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for 'Outreach'
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': '200 Varick St, New York, NY 10014',
                    'Name': 'Project Renewal Outreach',
                    'City': 'New York',
                    'Description': 'Provides outreach services to homeless individuals across NYC.',
                    'ContactInfo': '(212) 555-7890',
                    'HoursOfOperation': 'Mon-Sun: 9am - 7pm'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = MagicMock(latitude=40.7283, longitude=-74.0047)

            # send the POST request to update outreach markers
            response = client.post('/update/outreach')

            self.assertEqual(response.status_code, 200)
            self.assertIn('status', response.json)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['message'], 'Outreach markers updated')

            self.assertIn((40.7283, -74.0047), existing_markers)
            self.assertEqual(len(markers), 1)  

    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_update_shelter_route(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for 'Shelter'
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': '309 W 108th St, New York, NY 10029',
                    'Name': 'Good Shepherd Services Shelter',
                    'City': 'New York',
                    'Description': 'A shelter and resource center for women and children escaping domestic violence.',
                    'ContactInfo': '(212) 555-2346',
                    'HoursOfOperation': 'Mon-Fri: 8am - 6pm'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = MagicMock(latitude=40.7956, longitude=-73.9573)

            # send the POST request to update shelter markers
            response = client.post('/update/shelter')

            self.assertEqual(response.status_code, 200)
            self.assertIn('status', response.json)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['message'], 'Shelter markers updated')

            self.assertIn((40.7956, -73.9573), existing_markers)
            self.assertEqual(len(markers), 1)  

    @patch('requests.get')
    @patch.object(Nominatim, 'geocode')
    def test_invalid_geocode(self, mock_geocode, mock_get):
        with app.test_client() as client:
            # mock the API response for an invalid address
            mock_response = MagicMock()
            mock_response.json.return_value = [
                {
                    'Address': 'Invalid Address, Nowhere, XX 00000',  
                    'Name': 'Nonexistent Location',
                    'City': 'Nowhere, XX',
                    'Description': 'Nonexistent place',
                    'ContactInfo': '000-000-0000',
                    'HoursOfOperation': 'N/A'
                }
            ]
            mock_get.return_value = mock_response
            mock_geocode.return_value = None  #  geocoding fail

            # send the POST request to update counseling markers
            response = client.post('/update/counseling')

            print("Response status code:", response.status_code)
            print("Response JSON:", response.json)

            self.assertEqual(response.status_code, 400)
            self.assertIn('status', response.json)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['message'], "Address 'Invalid Address, Nowhere, XX 00000' could not be found or geocoded.") 

if __name__ == '__main__':
    unittest.main()
