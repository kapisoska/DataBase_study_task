from telebot import types

keyboard_1 = [
    [
        types.InlineKeyboardButton("Sign up", callback_data='reg'),
    ],
    [
        types.InlineKeyboardButton("Sign in", callback_data='log_in'),
        types.InlineKeyboardButton("Sign out", callback_data='log_out'),
    ],
    [
        types.InlineKeyboardButton("Delete my account", callback_data='delete_acc'),
    ],
]
kbrd_1 = types.InlineKeyboardMarkup(keyboard_1)
keyboard_2 = [
    [
        types.InlineKeyboardButton("OK", callback_data='ok'),
    ],
]
kbrd_2 = types.InlineKeyboardMarkup(keyboard_2)
keyboard_3 = [
    [
        types.InlineKeyboardButton("REPEAT", callback_data='rpt'),
    ],
]
kbrd_3 = types.InlineKeyboardMarkup(keyboard_3)
keyboard_login_ok = [
    [
        types.InlineKeyboardButton("OK", callback_data='ok_log_in'),
    ],
]
kbrd_login_ok = types.InlineKeyboardMarkup(keyboard_login_ok)
keyboard_login_repeat = [
    [
        types.InlineKeyboardButton("REPEAT", callback_data='rpt_log_in'),
    ],
]
kbrd_login_rpt = types.InlineKeyboardMarkup(keyboard_login_repeat)
