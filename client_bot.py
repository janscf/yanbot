from pyrogram import Client

api_id = 13003145
api_hash = '722364beb6c650617f6eaab0c3607f25'

app = Client('my_account', api_id, api_hash)

app.start()
app.send_message(182812766, 'Привет, это Ян! Тестирую телеграм бота')
app.stop()
