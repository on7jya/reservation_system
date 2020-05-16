from apps.reservation.exceptions import AlreadyAccepted, AlreadyCanceled, SuccessAccepted, SuccessCanceled
from apps.reservation.models import Reservation
from config.log_action import log_change_mes


class ApproveReservationService:
    def __init__(self, request, reservation):
        self.request = request
        self.reservation = reservation

    def execute(self):
        res = self.reservation
        if res.state == '0':
            Reservation.accept(res)
            res.save()
            log_change_mes(self.request, res, "Successfully completed approve from API!")
            raise SuccessAccepted()
        elif res.state == '1':
            log_change_mes(self.request, res, "Failed approve. The reservation was already confirmed earlier!")
            raise AlreadyAccepted()
        elif res.state == '2':
            log_change_mes(self.request, res, "Failed approve. Your reservation has already been cancelled!")
            raise AlreadyCanceled()


class CancelReservationService:
    def __init__(self, request, reservation):
        self.request = request
        self.reservation = reservation

    def execute(self):
        res = self.reservation
        if res.state == '0':
            Reservation.manual_cancel(res)
            res.save()
            log_change_mes(self.request, res, "Successfully completed manual cancellation from API!")
            raise SuccessCanceled()
        elif res.state == '1':
            log_change_mes(self.request, res, "Failed cancellation. The reservation was already confirmed earlier!")
            raise AlreadyAccepted()
        elif res.state == '2':
            log_change_mes(self.request, res, "Failed cancellation. Your reservation has already been cancelled!")
            raise AlreadyCanceled()
