# Scheduling a Message

from whatpack.synchronous import whats

# Schedule a message to be sent at a specific time
whats.send_what_msg(phone_no="+1234567890", message="Scheduled message at 15:30", time_hour=15, time_min=30)
