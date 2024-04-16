import time

from business import sheets
from business.facebook import Facebook
from misc.models import Task
from misc.exceptions import LoginException, UnexpectedModeException


def execute(task: Task):
    facebook = Facebook(task=task)
    login_status = facebook.login()
    if not login_status:
        facebook.close()
        raise LoginException()
    if task.worker_in_group == '':
        """ Join the group """
        facebook.subscribe_group()
        sheets.update_subscription(task, False)

    elif task.worker_in_group == 'TRUE':
        """ Create post """
        facebook.create_post()
        sheets.mark_finished(task)

    elif task.worker_in_group == 'FALSE':
        """ Check group join status """
        subscription_status = facebook.check_subscription()
        print(subscription_status)
        sheets.update_subscription(task, subscription_status)
    else:
        """ Unexpected mode """
        facebook.close()
        raise UnexpectedModeException()
    facebook.close()
    return None


while True:
    t = sheets.get_random_task()
    if t is None:
        time.sleep(60)
        continue
    try:
        execute(t)
    except LoginException:

        sheets.mark_bad_account(t.worker, t.link)
    except (UnexpectedModeException, Exception) as e:
        print(e)
        print('Ошибка при обработке запроса в целом')
