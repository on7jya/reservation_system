from apps.reservation.exceptions import AlreadyAccepted, AlreadyCanceled, SuccessAccepted, SuccessCanceled
from apps.reservation.models import Reservation


class ApproveReservationService:
    def __init__(self, reservation):
        self.reservation = reservation

    def execute(self):
        res = self.reservation
        if res.state == '0':
            Reservation.accept(res)
            res.save()
            raise SuccessAccepted()
        elif res.state == '1':
            raise AlreadyAccepted()
        elif res.state == '2':
            raise AlreadyCanceled()


class CancelReservationService:
    def __init__(self, reservation):
        self.reservation = reservation

    def execute(self):
        res = self.reservation
        if res.state == '0':
            Reservation.manual_cancel(res)
            res.save()
            raise SuccessCanceled()
        elif res.state == '1':
            raise AlreadyAccepted()
        elif res.state == '2':
            raise AlreadyCanceled()

