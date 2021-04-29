import datetime
import json
import requests
import xmltodict

from django.conf import settings

from utils.debug import Debug  # noqa

from . import models


def destroy_attachment(instance):
    if instance.file:
        instance.file.delete()
    instance.delete()


def update_holiday(year, serializer_class):
    base_url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?serviceKey='  # noqa
    service_key = settings.HOLIDAY_SERVICE_KEY
    sol_year = '&solYear=%d' % year
    data = []

    for month in range(1, 12):
        sol_month = '&solMonth=%02d' % month
        url = base_url + service_key + sol_year + sol_month

        response = requests.get(url)
        body = json.loads(json.dumps(xmltodict.parse(response.text)))
        items = body.get('response').get('body').get('items')
        if not items:
            continue
        else:
            items = items.get('item')

        if not type(items) == list:
            items = [items]
        for item in items:
            if item.get('isHoliday') == 'Y':
                date = datetime.datetime.strptime(
                    item.get('locdate'), '%Y%m%d'
                )
                if not models.Holiday.objects.date_exist(date):
                    instance = models.Holiday.objects.create(
                        date=date.date(),
                        name=item.get('dateName')
                    )
                    serializer = serializer_class(instance)
                    data.append(serializer.data)
    if data:
        return data
    else:
        return None


def is_holiday(date):
    weekend = bool(date.isoweekday() == 6 or date.isoweekday() == 7)
    if weekend:
        return True
    else:
        return models.Holiday.objects.date_exist(date)
