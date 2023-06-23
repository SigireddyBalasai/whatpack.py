import asyncio
import os
import collections
from concurrent.futures import ThreadPoolExecutor, as_completed
from platform import system
from typing import NamedTuple, Union
from urllib.parse import quote
from webbrowser import open
import requests
from requests import ConnectionError
from pyautogui import click, hotkey, moveTo, press, size, typewrite, ImageNotFoundException
from pyscreeze import Box, screenshot
import cv2
import numpy as np

from .exceptions import InternetException

WIDTH, HEIGHT = size()

Box = collections.namedtuple('Box', 'left top width height score')


def check_number(number: str) -> bool:
    """Checks if the Number is Valid or not"""

    return ("+" in number) or ("_" in number)


def close_tab(wait_time: int = 2) -> None:
    """Closes the Currently Opened Browser Tab"""

    asyncio.sleep(wait_time)
    _system = system().lower()
    if _system in ("windows", "linux"):
        hotkey("ctrl", "w")
    elif _system == "darwin":
        hotkey("command", "w")
    else:
        raise Warning(f"{_system} not supported!")
    press("enter")


def find_recent_chat():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locate_on_screen(f"{dir_path}\\data\\searchbar.png")
    try:
        moveTo(location[0] + location[2] / 2, location[1] + location[3])
        click()
    except ImageNotFoundException:
        location = locate_on_screen(f"{dir_path}\\data\\searchbar2.png")
        moveTo(location[0] + location[2] / 2, location[1] + location[3])
        click()


def find_textbox() -> None:
    """click on text box"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locate_on_screen(f"{dir_path}\\data\\pywhatkit_smile1.png")
    try:
        moveTo(location[0] + 150, location[1] + 5)
        click()
    except ImageNotFoundException:
        location = locate_on_screen(f"{dir_path}\\data\\pywhatkit_smile.png")
        moveTo(location[0] + 150, location[1] + 5)
        click()


def find_link():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"{dir_path}\\data\\link.png")
    link_paths = ["link.png", "link2.png"]
    locations = [locate_on_screen(f"{dir_path}\\data\\{loc}", grayscale=True, confidence=0.9, multiscale=True)
                 for loc in link_paths]
    location = None
    y = 0
    for position_link in locations:
        if position_link is not None and position_link[1] > y:
            y = position_link[1]
            location = position_link
    print(location)
    moveTo(location[0] + location[2] / 2, location[1] + location[3] / 2)
    click()


def find_document():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locate_on_screen(f"{dir_path}\\data\\document.png", confidence=0.8, multiscale=True, grayscale=True)
    print(location)

    moveTo(location[0] + location[2] / 2, location[1] + location[3] / 2)
    click()


def find_photo_or_video():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locate_on_screen(f"{dir_path}\\data\\photo_or_video.png", confidence=0.8,
                                multiscale=True,
                                grayscale=True)
    print(location)
    moveTo(location[0] + location[2] / 2, location[1] + location[3] / 2)
    click()


def check_connection() -> None:
    """Check the Internet connection of the Host Machine"""

    try:
        requests.get("www.google.com")
    except ConnectionError:
        raise InternetException(
            "Error while connecting to the Internet. Make sure you are connected to the Internet!"
        )


def _web(receiver: str, message: str) -> None:
    """Opens WhatsApp Web based on the Receiver"""
    if check_number(number=receiver):
        open(
            "https://web.whatsapp.com/send?phone="
            + receiver
            + "&text="
            + quote(message)
        )
    else:
        open("https://web.whatsapp.com/accept?code=" + receiver)


def send_message(message: str, receiver: str, wait_time: int) -> None:
    """Parses and Sends the Message"""

    _web(receiver=receiver, message=message)
    asyncio.sleep(7)
    click(WIDTH / 2, HEIGHT / 2 + 15)
    asyncio.sleep(wait_time - 7)
    _web(receiver=receiver, message=message)
    asyncio.sleep(7)
    click(WIDTH / 2, HEIGHT / 2)
    asyncio.sleep(wait_time - 7)
    if not check_number(number=receiver):
        for char in message:
            if char == "\n":
                hotkey("shift", "enter")
            else:
                typewrite(char)
    find_textbox()
    press("enter")


def locate_on_screen(image, **kwargs):
    """Locate button on screen using cv2.TemplateMatching algorithm

        Parameters
        ----------
        image : str
            The file location of the template image
        grayscale : bool
            Flag to run template matching using grayscale image
        confidence : float
            Confidence Threshold
        multi_scale : bool
            Flag to run multi_scale template matching from 1 to 0.8

        Returns
        -------
        Box
            a tuple of (x,y,w,h) of the best match
    """
    screenshot_im = screenshot(region=None)
    box_result = locate_max_opencv(image, screenshot_im, **kwargs)
    try:
        screenshot_im.fp.close()
    except AttributeError:
        # FROM pyscreeze
        # Screenshots on Windows won't have an fp since they came from
        # ImageGrab, not a file. Screenshots on Linux will have fp set
        # to None since the file has been unlinked
        pass
    return box_result


def locate_max_opencv(template: str,
                      screen_image: str,
                      grayscale: bool = False,
                      confidence=0.9,
                      multiscale=False) -> Union[Box, Box, None]:
    """Locate button using cv2.TemplateMatching algorithm

        Parameters
        ----------
        template : str
            The file location of the template image
        screen_image : PIL.Image
            The screenshot done using pyscreeze
        grayscale : bool
            Flag to run template matching using grayscale image
        confidence : float
            Confidence Threshold
        multiscale : bool
            Flag to run multiscale template matching from 1 to 0.8

        Returns
        -------
        Box
            a tuple of (x,y,w,h) of the best match
    """
    confidence = float(confidence)

    template = load_image(template, grayscale)
    template_h, template_w = template.shape[:2]
    screen_image = load_image(screen_image, grayscale)

    if (screen_image.shape[0] < template.shape[0] or
            screen_image.shape[1] < template.shape[1]):
        # avoid semi-cryptic OpenCV error below if bad size
        raise ValueError('needle dimension(s) exceed the haystack image or region dimensions')

    if multiscale:
        sizes = [1, 0.9, 0.85, 0.8]
        match_x, match_y = None, None
        with ThreadPoolExecutor() as executor:
            future_to_contour = {executor.submit(cv2.matchTemplate,
                                                 screen_image.copy(),
                                                 cv2.resize(template.copy(), (0, 0), fx=size, fy=size),
                                                 cv2.TM_CCORR_NORMED): size_ for size_ in sizes}
            for future in as_completed(future_to_contour):
                _, max_val, _, max_loc = cv2.minMaxLoc(future.result())
                if max_val >= confidence:
                    confidence = max_val
                    match_x = max_loc[0]
                    match_y = max_loc[1]
        if match_x is not None:
            return Box(match_x, match_y, template_w, template_h, max_val)
        else:
            raise ImageNotFoundException

    result = cv2.matchTemplate(screen_image, template, cv2.TM_CCORR_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(result)

    if len(result) == 0:
        raise ImageNotFoundException
    if max_val >= confidence:
        match_x = max_loc[0]
        match_y = max_loc[1]

        return Box(match_x, match_y, template_w, template_h, max_val)
    return


def load_image(img2load,
               gray: bool):
    if type(img2load) is str:
        assert os.path.exists(img2load)
        return cv2.imread(img2load) if not gray else cv2.cvtColor(cv2.imread(img2load), cv2.COLOR_BGR2GRAY)
    return np.array(img2load) if not gray else cv2.cvtColor(np.array(img2load), cv2.COLOR_BGR2GRAY)
