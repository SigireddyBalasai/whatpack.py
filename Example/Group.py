# Sending a Message to a Group

from whatpack.synchronous import whats

# Open WhatsApp Web
whats.open_web()

# Send a message to a group instantly
whats.send_what_msg_to_group_instantly(group_id="your_group_id", message="Hello, group!")
