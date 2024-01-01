# Sending a Document

from whatpack.synchronous import whats

# Open WhatsApp Web
whats.open_web()

# Send a document instantly
whats.send_whats_doc_immediately(phone_no="+1234567890", path="/path/to/document.pdf", message="Check this document!")
