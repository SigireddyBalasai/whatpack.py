"""All the exceptions will be stored here"""


class CountryCodeException(Exception):
    """
    Country Code is not present in the Phone Number
    """


class CallTimeException(Exception):
    """
    Wait time is too short for WhatsApp Web to Open
    """


class ImageNotFoundException(Exception):
    """
    No image was found while searching with template matching algorithm
    """


class InternetException(Exception):
    """
    Host machine is not connected to the Internet or the connection Speed is Slow
    """


class InvalidPhoneNumber(Exception):
    """
    Phone number given is invalid
    """


class UnsupportedEmailProvider(Exception):
    """
    Email provider used to send the Email is not supported
    """


class UnableToAccessApi(Exception):
    """unable to access whatpack api"""


class CannotFindTheSolution(Exception):
    """We are unable to help sorry for it"""
