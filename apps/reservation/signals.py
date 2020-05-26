from config.log_action import log_change, log_addition, log_delete


def post_save_handler(sender, instance, created, using, **kwargs):
    """Журналирование сохранений и изменений"""
    if created:
        log_addition(instance)
    else:
        log_change(instance)


def post_delete_handler(sender, instance, using, **kwargs):
    """Журналирование удалений"""
    log_delete(instance)
