from config.log_action import log_change, log_addition, log_delete


def post_save_handler(sender, instance, created, using, **kwargs):
    if created:
        log_addition(instance)
    else:
        log_change(instance)


def post_delete_handler(sender, instance, using, **kwargs):
    log_delete(instance)
