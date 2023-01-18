from django.utils import timezone

from things.tests import TestCase


class HolidayTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def nottest_data_go_kr_get_holidays(self):  # name prefix to test to test
        year = timezone.localtime().year
        self.post(
            '/api/things/holidays/%d/' % year,
            auth=True
        )
        self.status(200)

        holidays = self.data
        self.get(
            '/api/things/holidays/%d/' % year,
            auth=True
        )
        self.status(200)

        for index, holiday in enumerate(reversed(holidays)):
            self.check(holiday.get('date'), self.data[index].get('date'))
            self.check(holiday.get('name'), self.data[index].get('name'))

    def test_data_edit_holiday(self):
        self.create_holiday()
        self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'date': '2021-12-24',
                'name': 'Christmas Eve'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('date'), '2021-12-24')
        self.check(self.data.get('name'), 'Christmas Eve')

        self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'date': '2021-11-31',
                'name': 'Christmas Eve'
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'date': '',
                'name': ''
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/things/holiday/%d/' % self.holiday.id,
            {
                'name': 'Christmas Eve'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('name'), 'Christmas Eve')

    def test_data_delete_holiday(self):
        self.create_holiday()
        self.delete(
            '/api/things/holiday/%d/' % self.holiday.id,
            auth=True
        )
        self.status(204)

        self.get(
            '/api/things/holidays/%d/' % timezone.localtime().year,
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 0)
