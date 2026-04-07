from django.test import TestCase
from transport.models import BusLine, Route
from stations.models import Station


class RouteTests(TestCase):

    def setUp(self):
        self.line = BusLine.objects.create(
            number='1',
            route_bus='Test Route'
        )

        self.stop1 = Station.objects.create(name='Stop 1', stop_id='S1')
        self.stop2 = Station.objects.create(name='Stop 2', stop_id='S2')

    def test_create_route(self):
        route = Route.objects.create(
            line=self.line,
            stop=self.stop1,
            position=1
        )

        self.assertEqual(route.position, 1)
        self.assertEqual(route.stop, self.stop1)

    def test_unique_position_per_line(self):
        Route.objects.create(line=self.line, stop=self.stop1, position=1)

        with self.assertRaises(Exception):
            Route.objects.create(line=self.line, stop=self.stop2, position=1)

    def test_unique_stop_per_line(self):
        Route.objects.create(line=self.line, stop=self.stop1, position=1)

        with self.assertRaises(Exception):
            Route.objects.create(line=self.line, stop=self.stop1, position=2)

    def test_auto_position_assignment(self):
        r1 = Route.objects.create(line=self.line, stop=self.stop1, position=1)
        r2 = Route.objects.create(line=self.line, stop=self.stop2)

        self.assertEqual(r2.position, 2)
