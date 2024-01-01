#  Sending an Instant Message

from whatpack.synchronous import whats

# Open WhatsApp Web
whats.open_web()

# Send an instant message to a phone number
whats.send_what_msg_instantly(phone_no="+1234567890", message="Hello, this is an instant message!")
