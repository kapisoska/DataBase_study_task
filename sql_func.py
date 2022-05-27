import psycopg2
import config

con = psycopg2.connect(
    database="postgres",
    user=config.db_user,
    password=config.db_password,
    # host="127.0.0.1",
    # port="5432"
)
print("Database opened successfully")


def search_user_account(user_id):
    sql = "SELECT account_id from users WHERE id={}".format(user_id)
    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchall()[0][0]


def get_state_login(user_id):
    sql = "SELECT state from users WHERE id={}".format(user_id)
    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchall()[0][0]


def get_account_pass(login):
    sql = "SELECT password from accounts WHERE login='{}'".format(login)
    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchall()[0][0]


def search(column, value):
    sql = "SELECT 1 FROM users WHERE {}={} LIMIT 1".format(column, value)
    cur = con.cursor()
    cur.execute(sql)
    try:
        print(cur.fetchall()[0][0])
        print("found")
        return True
    except IndexError:
        print(cur.fetchall())
        print("not found")
        return False


def insert(user_id, full_name):
    sql = "INSERT INTO public.users (id, name, account_id, state) VALUES ({}, '{}', DEFAULT, DEFAULT)" \
        .format(user_id, full_name)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    print("Operation done successfully")


def update_usr_login(user_id, login):
    sql = "UPDATE public.users SET account_id = '{}' WHERE id = {}".format(login, user_id)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    print("Operation done successfully")


def update_usr_state(user_id, state):
    sql = "UPDATE public.users SET state = {} WHERE id = {}".format(state, user_id)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    print("Operation done successfully")


def get_all_logins():
    logins = []
    sql = "SELECT DISTINCT login FROM accounts"
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        logins.append(row[0])
    return logins


def insert_to_accounts(login, password):
    sql = "INSERT INTO public.accounts (login, password) VALUES ('{}', '{}')".format(login, password)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    print("Operation done successfully")


def delete_user_account(user_id):
    sql = "SELECT account_id from users WHERE id={}".format(user_id)
    cur = con.cursor()
    cur.execute(sql)
    login = cur.fetchall()[0][0]
    update_usr_login(user_id, "default")
    update_usr_state(user_id, False)
    sql2 = "DELETE FROM public.accounts WHERE login LIKE '{}' ESCAPE '#'".format(login)
    cur.execute(sql2)
    con.commit()

# delete_user_account(240077398)
# print(search_user_account(240077398))
# print(get_all_logins())
# insert(11,"egooor")
# search("user_id", 3424253)
# con.close()
# print(get_state_login(240077398))
# print( get_account_pass("eos"))
# update_usr_state(234651346, True)
