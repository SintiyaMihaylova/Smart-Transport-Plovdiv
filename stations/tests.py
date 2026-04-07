from django.test import TestCase
from stations.models import Station


class StationTests(TestCase):

    def test_create_station(self):
        station = Station.objects.create(
            name='Central',
            stop_id='C1'
        )

        self.assertEqual(station.name, 'Central')

    def test_unique_stop_id(self):
        Station.objects.create(name='A', stop_id='X1')

        with self.assertRaises(Exception):
            Station.objects.create(name='B', stop_id='X1')
