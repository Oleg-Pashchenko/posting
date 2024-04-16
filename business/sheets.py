import random

from misc.models import Task, Worker
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('vitalik-418717-545018ff6fcd.json', scope)
client = gspread.authorize(credentials)

sheet = client.open('Facebook Autoposting')
accounts = sheet.worksheet('Accounts')
groups = sheet.worksheet('Groups')
banners = sheet.worksheet('Banners')


def get_random_banner_link():
    return random.choice(banners.get_all_values()[1::])[0]


def get_worker(email: str):
    if email == '':
        worker = Worker(*random.choice(accounts.get_all_values()[1::]))
        if worker.is_work is False:
            return get_worker(email)
        return worker
    else:
        for account in accounts.get_all_values()[1::]:
            account = Worker(*account)
            if account.email == email:
                return account
        return get_worker('')


def get_random_task():
    group = random.choice(groups.get_all_values()[1::])
    if group[1] == '':
        worker = get_worker(group[2])
        if worker.email != group[2]:
            update_task_worker(group[0], worker.email)
        return Task(
            link=group[0],
            finished=group[1],
            worker=worker,
            worker_in_group=group[3]
        )


def update_task_worker(link, email):
    groups_data = groups.get_all_values()
    for row_index, group_row in enumerate(groups_data):
        if group_row[0] == link:
            groups.update_cell(row_index + 1, 2, '')
            groups.update_cell(row_index + 1, 3, email)
            groups.update_cell(row_index + 1, 4, '')
            break


def update_subscription(task: Task, status: bool):
    groups_data = groups.get_all_values()
    for row_index, group_row in enumerate(groups_data):
        if group_row[0] == task.link:
            groups.update_cell(row_index + 1, 4, status)
            break


def mark_finished(task: Task):
    groups_data = groups.get_all_values()
    for row_index, group_row in enumerate(groups_data):
        if group_row[0] == task.link:
            groups.update_cell(row_index + 1, 2, True)
            break


def mark_bad_account(worker: Worker, link: str):
    accounts_data = accounts.get_all_values()
    for row_index, account_row in enumerate(accounts_data):
        if account_row[0] == worker.email:
            accounts.update_cell(row_index + 1, 4, False)

            groups_data = groups.get_all_values()
            for row_index, group_row in enumerate(groups_data):
                if group_row[0] == link:
                    groups.update_cell(row_index + 1, 2, '')
                    groups.update_cell(row_index + 1, 3, '')
                    groups.update_cell(row_index + 1, 4, '')
            return
