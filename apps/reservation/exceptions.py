from rest_framework.exceptions import APIException


class SuccessAccepted(APIException):
    status_code = 204
    default_detail = 'Успешно выполнено подтверждение бронирования!'
    default_code = 'success_accepted'


class SuccessCanceled(APIException):
    status_code = 204
    default_detail = 'Успешно выполнена отмена бронирования!'
    default_code = 'success_canceled'


class AlreadyAccepted(APIException):
    status_code = 400
    default_detail = 'Бронирование уже было подтверждено ранее!'
    default_code = 'already_accepted'


class AlreadyCanceled(APIException):
    status_code = 400
    default_detail = 'Бронирование уже было отменено ранее!'
    default_code = 'already_canceled'


class CreatedByAnotherUser(APIException):
    status_code = 400
    default_detail = 'Бронирование было создано другим пользователем!'
    default_code = 'created_by_another_user'
