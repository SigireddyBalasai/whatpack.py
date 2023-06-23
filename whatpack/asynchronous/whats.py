"""This is the main whatsapp module for the asynchronous version of the package"""
import typing
import time
import asyncio
import pathlib
import webbrowser as web
from datetime import datetime
from re import fullmatch
from typing import List
from urllib.parse import quote
import pyperclip
import pyautogui as pg
from .core import core_, exceptions


async def send_what_msg_instantly(
        phone_no: str,
        message: str,
        **kwargs
) -> None:
    """Send a WhatsApp message instantly.
    
    This function opens a new tab in the default web browser,
    navigates to the WhatsApp web page,
    and sends a message to the specified phone number.
    
    Parameters:
    message: The message to be sent.
    phone_no: The phone number to send the message to.
    wait_time: The time to wait before sending the message (in seconds).
    tab_close: A flag indicating whether to close the tab after sending the message.
    close_time: The time to wait before closing the tab (in seconds).
    
    Returns:
    None.
    """
    waiting_ = {
        'wait_time': kwargs.get('wait_time', 15),
        'tab_close': kwargs.get('tab_close', False),
        'close_time': kwargs.get('close_time', 3)
    }
    print(phone_no)
    print(await core_.check_number(number=phone_no))
    if not await core_.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")
    phone_no = phone_no.replace(" ", "")
    print(phone_no)
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")
    phone_no = phone_no.replace(" ", "")
    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}", new=0)
    await asyncio.sleep(waiting_['wait_time'])
    pg.press('enter')
    await asyncio.sleep(waiting_['close_time'])
    if waiting_['tab_close']:
        await core_.close_tab(wait_time=waiting_['close_time'])


async def send_what_msg(
        phone_no: typing.Union[str, None] = None,
        message: typing.Union[str, None] = None,
        **kwargs
) -> None:
    """Send a WhatsApp message at a certain time.
    
    This function schedules the sending of a WhatsApp message
    to a specified phone number at a specified time.
    
    Parameters:
    phone_no: The phone number to send the message to.
    message: The message to be sent.
    wait_time: The time to wait before sending the message (in seconds).
    tab_close: A flag indicating whether to close the tab after sending the message.
    close_time: The time to wait before closing the tab (in seconds).
    
    Returns:
    None.
    """
    time_ = {"hour": kwargs.get('time_hour', 0), "min": kwargs.get('time_min', 0)}
    waiting_ = {
        'wait_time': kwargs.get('wait_time', 15),
        'tab_close': kwargs.get('tab_close', False),
        'close_time': kwargs.get('close_time', 3)
    }
    if not core_.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    if time_['hour'] not in range(25) or time_["min"] not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_['hour']}:{time_['min']}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < time_['wait_time']:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - waiting_['wait_time']
    print(
        f"In {waiting_['sleep_time']} Seconds WhatsApp will open and after\
        {waiting_['wait_time']} Seconds Message will be Delivered!"
    )
    await asyncio.sleep(sleep_time)
    await send_what_msg_instantly(phone_no, message, **kwargs)
    if waiting_['tab_close']:
        await core_.close_tab(wait_time=waiting_['close_time'])


async def send_what_msg_to_group(
        group_id: str,
        message: str,
        **kwargs
) -> None:
    """Send a WhatsApp message to a group at a certain time.
    
    This function schedules 
    the sending of a WhatsApp message to 
    a specified group at a specified time.
    
    Parameters:
    group_id: The ID of the group to send the message to.
    message: The message to be sent.
    time_hour: The hour at which to send the message (in 24-hour format).
    time_min: The minute at which to send the message.
    wait_time: The time to wait before sending the message (in seconds).
    tab_close: A flag indicating whether to close the tab after sending the message.
    close_time: The time to wait before closing the tab (in seconds).
    
    Returns:
    None.
    """
    time_ = {"hour": kwargs.get('time_hour', 0), "min": kwargs.get('time_min', 0)}
    waiting_ = {
        'wait_time': kwargs.get('wait_time', 15),
        'tab_close': kwargs.get('tab_close', False),
        'close_time': kwargs.get('close_time', 3)
    }
    if time_['hour'] not in range(25) or time_['min'] not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_['hour']}:{time_['min']}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < waiting_["wait_time"]:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - waiting_['wait_time']
    print(
        f"In {sleep_time} Seconds WhatsApp will open\
            and after {waiting_['wait_time']} Seconds Message will be Delivered!"
    )
    await asyncio.sleep(sleep_time)
    await send_what_msg_instantly(group_id, message)
    if waiting_['tab_close']:
        await core_.close_tab(wait_time=waiting_["close_time"])


async def send_what_msg_to_group_instantly(
        group_id: str,
        message: str,
        **kwargs
) -> None:
    """Send a WhatsApp message to a group instantly.
    
    This function opens the WhatsApp Web page
    in a new tab and sends a message to the specified group.
    
    Parameters:
    group_id: The ID of the group to send the message to.
    message: The message to be sent.
    wait_time: The time to wait before sending the message (in seconds).
    tab_close: A flag indicating whether to close the tab after sending the message.
    close_time: The time to wait before closing the tab (in seconds).
    
    Returns:
    None.
    """
    waiting_ = {
        'wait_time': kwargs.get('wait_time', 15),
        'tab_close': kwargs.get('tab_close', False),
        'close_time': kwargs.get('close_time', 3)
    }
    await asyncio.sleep(4)
    await send_what_msg_instantly(group_id, message, **kwargs)

    if waiting_['tab_close']:
        await core_.close_tab(wait_time=waiting_['close_time'])


async def send_whats_msg_to_all(
        phone_nos: List[str],
        message: str,
        **kwargs
) -> None:
    """Send a WhatsApp message to a list of phone numbers 
    at a certain time.
    This function schedules the sending of a WhatsApp message
    to a list of specified phone numbers at a specified time.
    
    Parameters:
    phone_nos: The list of phone numbers to send the message to.
    message: The message to be sent.
    time_hour: The hour at which to send the message (in 24-hour format).
    time_min: The minute at which to send the message.
    wait_time: The time to wait before sending the message (in seconds).
    tab_close: A flag indicating whether to close the tab after sending the message.
    close_time: The time to wait before closing the tab (in seconds).
    
    Returns:
    None.
    """

    for phone_n in phone_nos:
        await send_what_msg(
            phone_n, message, **kwargs
        )


async def send_img_or_video_immediately(
        phone_no: str,
        path: str,
        message: str = None,
        **kwargs
) -> None:
    """Send an image or video file via WhatsApp instantly.
    This function opens a new tab in the default web browser, 
    navigates to the WhatsApp web page, and sends an image or
    video file to the specified phone number.
    Parameters:
    phone_no: The phone number to send the file to.
    path: The file path of the image or video file to be sent.
    wait_time: The time to wait before sending the file (in seconds).
    tab_close: A flag indicating whether to close the tab after sending the file.
    close_time: The time to wait before closing the tab (in seconds).
    
    Returns:
    None.
    """
    waiting_ = {
        'wait_time': kwargs.get('wait_time', 15),
        'tab_close': kwargs.get('tab_close', False),
        'close_time': kwargs.get('close_time', 3)
    }
    if not await core_.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}")
    time.sleep(waiting_['wait_time'])
    await core_.find_link()
    time.sleep(1)
    await core_.find_photo_or_video()
    if isinstance(path, str):
        path = pathlib.Path(path)
        pyperclip.copy(str(path.resolve()))
        print("Copied")
    else:
        str_n = " ".join(list(map(lambda x: str(pathlib.Path(x).resolve()), path)))
        print(str_n)
        pyperclip.copy(str_n)
    time.sleep(1)
    pg.hotkey('ctrl', 'v')
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    if message is not None:
        pyperclip.copy(message)
        time.sleep(1)
        pg.hotkey('ctrl', 'v')
    time.sleep(1)
    pg.press('enter')
    if waiting_['tab_close']:
        await core_.close_tab(wait_time=waiting_['close_time'])


async def send_whats_doc_immediately(
        phone_no: str,
        path: str,
        message: str = None,
        **kwargs
) -> None:
    """Send a WhatsApp document instantly.
This function opens a new tab in the default web browser, 
navigates to the WhatsApp web page, and sends a document to the specified phone number.
Parameters:
phone_no: The phone number to send the document to.
path: The file path of the document to be sent.
wait_time: The time to wait before sending the document (in seconds).
tab_close: A flag indicating whether to close the tab after sending the document.
close_time: The time to wait before closing the tab (in seconds).
Returns:
None.
"""
    waiting_ = {
        'wait_time': kwargs.get('wait_time', 15),
        'tab_close': kwargs.get('tab_close', False),
        'close_time': kwargs.get('close_time', 3)
    }

    if not await core_.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}")
    time.sleep(waiting_['wait_time'])
    await core_.find_link()
    time.sleep(1)
    await core_.find_document()
    if isinstance(path, str):
        path = pathlib.Path(path)
        pyperclip.copy(str(path.resolve()))
        print("Copied")
    else:
        str_n = " ".join(list(map(lambda x: str(pathlib.Path(x).resolve()), path)))
        print(str_n)

    time.sleep(1)
    pg.hotkey('ctrl', 'v')
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    if message is not None:
        pyperclip.copy(message)
        time.sleep(1)
        pg.hotkey('ctrl', 'v')
    pg.press('enter')
    if waiting_['tab_close']:
        await core_.close_tab(wait_time=waiting_['close_time'])


def open_web() -> bool:
    """Opens WhatsApp Web """

    try:
        web.open("https://web.whatsapp.com")
    except web.Error:
        return False
    return True
