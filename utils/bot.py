import threading

from django.utils import timezone

from core.permissions import IsAdminUser
from core.response import Response
from core.viewsets import APIView

from utils.debug import Debug  # noqa


def daily_task():
    now = timezone.localtime()
    today = now.date()

    Debug.trace(
        'Staring %s daily task...' % today
    )

    Debug.trace(
        '%s daily task finished.' % today
    )

    if today.day == 1:
        monthly_task()


def monthly_task():
    Debug.trace('Staring monthly task...')
    Debug.trace('monthly task finished.')


class DailyBotView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        daily_task()
        return Response(status=Response.HTTP_200)


class MonthlyBotView(DailyBotView):
    def post(self, request, *args, **kwargs):
        monthly_task()
        return Response(status=Response.HTTP_200)


def run_thread(cls, target):
    thread = threading.Thread(target=target)
    thread.start()


def bot_daily():
    run_thread(daily_task)
