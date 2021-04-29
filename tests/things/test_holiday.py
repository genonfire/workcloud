from django.utils import timezone

from core.response import Response
from things.tests import TestCase


class HolidayTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def nottest_data_go_kr_get_holidays(self):  # name prefix to test to test
        year = timezone.localtime().year
        response = self.post(
            '/api/things/holidays/%d/' % year,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        holidays = self.data

        response = self.get(
            '/api/things/holidays/%d/' % year,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        for index, holiday in enumerate(reversed(holidays)):
            assert (
                holiday.get('date') == self.data[index].get('date') and
                holiday.get('name') == self.data[index].get('name')
            )

    def test_data_edit_holiday(self):
        self.create_holiday()
        response = self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'date': '2021-12-24',
                'name': 'Christmas Eve'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('date') == '2021-12-24' and
            self.data.get('name') == 'Christmas Eve'
        )

        response = self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'date': '2021-11-31',
                'name': 'Christmas Eve'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'date': '',
                'name': ''
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'name': 'Christmas Eve'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('name') == 'Christmas Eve'
        )

    def test_data_delete_holiday(self):
        self.create_holiday()
        response = self.delete(
            '/api/things/holiday/%d/' % self.holiday.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/things/holidays/%d/' % timezone.localtime().year,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 0
        )
