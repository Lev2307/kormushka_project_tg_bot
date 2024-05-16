import sqlite3

DB_NAME = "db/database.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

def DB_table_val(telegram_id: str, downloaded_photo_names: str):
	cursor.execute('INSERT INTO db (telegram_id, downloaded_photo_names) VALUES (?, ?)', (telegram_id, downloaded_photo_names))
	conn.commit()

def DB_get_user_by_telegram_id(telegram_id: str):
    # получение пользователя по тг айди
    cursor.execute("SELECT * FROM db WHERE telegram_id = ?", (telegram_id, ))
    return cursor.fetchall()

def DB_add_image_to_list(tg_user: str, latest_image_name: str):
    # добавление названия скаченного изображения в поле downloaded_photo_names
    all_prev_images = DB_get_user_by_telegram_id(telegram_id=tg_user)[0][1]
    if len(all_prev_images) > 0:
        all_prev_images = all_prev_images + ' ' + latest_image_name
    else:
        all_prev_images = latest_image_name
    cursor.execute('Update db set downloaded_photo_names = ? WHERE telegram_id = ?', (all_prev_images, tg_user))
    conn.commit()

def DB_add_telegram_user(telegram_id):
    # запись пользователя в бд ( его тг айди )
    DB_table_val(telegram_id=telegram_id, downloaded_photo_names="")