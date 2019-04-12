from pyrogram import Client

app = Client(
    "edge_bot",
    api_id=651197,
    api_hash="ae242b414b728a67a775da6b296d5217"
)

@app.on_message()
def my_handler(client, message):
    print(message.text)

app.run()

