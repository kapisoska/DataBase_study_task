lis_of_msg = []
account_data = []
password = []
usr_login = []
to_delete = []


def list_to_del(ms_id, deleted_msg=None):
    if ms_id:
        lis_of_msg.append(ms_id)
    elif deleted_msg:
        lis_of_msg.remove(deleted_msg)
    else:
        return lis_of_msg
