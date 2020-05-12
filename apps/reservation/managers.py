from django.db import models


class ReservationManager(models.Manager):
    def pending(self):
        return self.filter(state="0")

    def accepted(self):
        return self.filter(state="1")

    def canceled(self):
        return self.filter(state="2")
