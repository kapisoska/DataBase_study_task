import telebot
from keyboards import *
from sql_func import *
from service import *
import config

bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=["start", "menu"])
def inline(message):
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    print("has started")
    print(user_id, full_name)
    bot.send_message(message.chat.id, "Menu:", reply_markup=kbrd_1)
    if message.text == "/start":
        if search("id", user_id):
            bot.send_message(message.chat.id, "you in database")
        else:
            bot.send_message(message.chat.id, "you not in database")
            insert(user_id, full_name)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'reg':
        if search_user_account(c.from_user.id) == "default":
            msg = bot.send_message(c.message.chat.id, "Write your login:")
            list_to_del(msg.message_id)
            bot.register_next_step_handler(msg, wait_login)
        else:
            msg = bot.send_message(c.message.chat.id, "You are already registered")
            list_to_del(msg.message_id)

    if c.data == "ok":
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, "well done!")
        print(password, usr_login)
        bot.send_message(c.message.chat.id, "login: {} \npassword: {}".format(usr_login[0], password[0]))
        insert_to_accounts(usr_login[0], password[0])
        update_usr_login(c.from_user.id, usr_login[0])
        password.clear()
        usr_login.clear()
        delete_log(c)

    if c.data == "rpt":
        bot.delete_message(c.message.chat.id, c.message.message_id)
        msg = bot.send_message(c.message.chat.id, "write password 2 times")
        list_to_del(msg.message_id)
        bot.register_next_step_handler(msg, first_times)

    if c.data == "log_in":
        if get_state_login(c.from_user.id):
            bot.send_message(c.message.chat.id, "You are already logged in")
        else:
            msg = bot.send_message(c.message.chat.id, "Write your login:")
            list_to_del(msg.message_id)
            bot.register_next_step_handler(msg, sign_in_accept_login)

    if c.data == "ok_log_in":
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, "You are logged in!")
        update_usr_state(c.from_user.id, True)
        account_data.clear()
        delete_log(c)

    if c.data == "rpt_log_in":
        msg = bot.send_message(c.message.chat.id, "write password:")
        list_to_del(msg.message_id)
        bot.register_next_step_handler(msg, wait_pass)

    if c.data == "log_out":
        if not get_state_login(c.from_user.id):
            bot.send_message(c.message.chat.id, "You already logged out")
        else:
            update_usr_state(c.from_user.id, False)
            bot.send_message(c.message.chat.id, "You are logged out")

    if c.data == "delete_acc":
        if search_user_account(c.from_user.id) == "default":
            bot.send_message(c.message.chat.id, "You dont have account")
        else:
            delete_user_account(c.from_user.id)
            print("USER: {} delete account".format(c.from_user.id))


@bot.message_handler(content_types=["text"])
def zero_reaction(message):
    print("zero reaction")
    pass


def wait_login(message):
    if message.text in get_all_logins():
        msg_1 = bot.send_message(message.chat.id, "login is already taken\nWrite another login")
        list_to_del(msg_1.message_id)
        bot.register_next_step_handler(msg_1, wait_login)
    else:
        list_to_del(message.message_id)
        usr_login.append(message.text)
        msg = bot.send_message(message.chat.id, "write password 2 times")
        list_to_del(msg.message_id)
        bot.register_next_step_handler(msg, first_times)


def first_times(message):
    print(1)
    password.append(message.text)
    bot.delete_message(message.chat.id, message.message_id)
    msg = bot.send_message(message.chat.id, "*" * len(message.text))
    list_to_del(msg.message_id)
    bot.register_next_step_handler(msg, second_times)


def second_times(message):
    print(2)
    password.append(message.text)
    bot.delete_message(message.chat.id, message.message_id)
    tpas = bot.send_message(message.chat.id, "*" * len(message.text))
    list_to_del(tpas.message_id)
    if password[0] == password[1]:
        bot.send_message(message.chat.id, "successful, tap OK to final", reply_markup=kbrd_2)
    else:
        print("Passwords do not match")
        bot.send_message(message.chat.id, "Passwords do not match, tap REPEAT", reply_markup=kbrd_3)
        password.clear()


def delete_log(c):
    if list_to_del(None):
        for msg in list_to_del(None):
            bot.delete_message(c.message.chat.id, message_id=msg)
            list_to_del(None, msg)
        if list_to_del(None):
            delete_log(c)
        else:
            pass


def sign_in_accept_login(message):
    if message.text not in get_all_logins():
        msg_1 = bot.send_message(message.chat.id, "This account login not registered\n write another login")
        list_to_del(msg_1.message_id)
        bot.register_next_step_handler(msg_1, sign_in_accept_login)
    else:
        list_to_del(message.message_id)
        account_data.append(message.text)
        msg = bot.send_message(message.chat.id, "write password:")
        list_to_del(msg.message_id)
        bot.register_next_step_handler(msg, wait_pass)


def wait_pass(message):
    account_data.append(message.text)
    bot.delete_message(message.chat.id, message.message_id)
    tpas = bot.send_message(message.chat.id, "*" * len(message.text))
    list_to_del(tpas.message_id)
    # to_delete.append(tpas.message_id)
    if account_data[1] == get_account_pass(account_data[0]):
        bot.send_message(message.chat.id, "successful, tap OK to final", reply_markup=kbrd_login_ok)
    else:
        bot.send_message(message.chat.id, "Passwords do not match, tap REPEAT", reply_markup=kbrd_login_rpt)
        account_data.pop(1)
