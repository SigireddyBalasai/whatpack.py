import asyncio
import os
import collections
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from platform import system
from urllib.parse import quote
from webbrowser import open

import aiohttp
from pyautogui import click, hotkey, moveTo, press, size, typewrite
from pyscreeze import Box, screenshot
import cv2
import numpy as np

from .exceptions import InternetException, ImageNotFoundException

WIDTH, HEIGHT = size()

Box = collections.namedtuple('Box', 'left top width height score')


def check_number(number: str) -> bool:
    """Checks if the Number is Valid or not"""

    return ("+" in number) or ("_" in number)


def close_tab(wait_time: int = 2) -> None:
    """Closes the Currently Opened Browser Tab"""

    await asyncio.sleep(wait_time)
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
    location = locateOnScreen(f"{dir_path}\\data\\searchbar.png")
    try:
        moveTo(location[0] + location[2] / 2, location[1] + location[3])
        click()
    except:
        location = locateOnScreen(f"{dir_path}\\data\\searchbar2.png")
        moveTo(location[0] + location[2] / 2, location[1] + location[3])
        click()


def findtextbox() -> None:
    """click on text box"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locateOnScreen(f"{dir_path}\\data\\pywhatkit_smile1.png")
    try:
        moveTo(location[0] + 150, location[1] + 5)
        click()
    except:
        location = locateOnScreen(f"{dir_path}\\data\\pywhatkit_smile.png")
        moveTo(location[0] + 150, location[1] + 5)
        click()


def find_link():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"{dir_path}\\data\\link.png")
    linkpaths = ["link.png", "link2.png"]
    locations = [locateOnScreen(f"{dir_path}\\data\\{loc}", grayscale=True, confidence=0.9, multiscale=True) for loc in
                 linkpaths]
    location = None
    y = 0
    for poslink in locations:
        if poslink is not None and poslink[1] > y:
            y = poslink[1]
            location = poslink
    print(location)
    moveTo(location[0] + location[2] / 2, location[1] + location[3] / 2)
    click()


def find_document():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locateOnScreen(f"{dir_path}\\data\\document.png", confidence=0.8, multiscale=True, grayscale=True)
    print(location)

    moveTo(location[0] + location[2] / 2, location[1] + location[3] / 2)
    click()


def find_photo_or_video():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locateOnScreen(f"{dir_path}\\data\\photo_or_video.png",confidence=0.8, multiscale=True, grayscale=True)
    print(location)
    moveTo(location[0] + location[2] / 2, location[1] + location[3] / 2)
    click()


def check_connection() -> None:
    """Check the Internet connection of the Host Machine"""

    try:
        with aiohttp.ClientSession() as session:
            with session.get("https://google.com") as response:
                status = response.status
                if status < 400:
                    pass

    except:
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

    await _web(receiver=receiver, message=message)
    await asyncio.sleep(7)
    click(WIDTH / 2, HEIGHT / 2 + 15)
    await asyncio.sleep(wait_time - 7)
    await _web(receiver=receiver, message=message)
    await asyncio.sleep(7)
    click(WIDTH / 2, HEIGHT / 2)
    await asyncio.sleep(wait_time - 7)
    if not check_number(number=receiver):
        for char in message:
            if char == "\n":
                hotkey("shift", "enter")
            else:
                typewrite(char)
    await findtextbox()
    press("enter")


def locateOnScreen(image, **kwargs):
    """Locate button on screen using cv2.TemplateMatching algorithm

        Parameters
        ----------
        image : str
            The file location of the template image
        grayscale : bool
            Flag to run template matching using grayscale image
        confidence : float
            Confidence Threshold
        mulstiscale : bool
            Flag to run mulstiscale template matching from 1 to 0.8

        Returns
        -------
        Box
            a tuple of (x,y,w,h) of the best match
    """
    screenshotIm = screenshot(region=None)
    boxresult = locateMax_opencv(image, screenshotIm, **kwargs)
    try:
        screenshotIm.fp.close()
    except AttributeError:
        # FROM pyscreeze
        # Screenshots on Windows won't have an fp since they came from
        # ImageGrab, not a file. Screenshots on Linux will have fp set
        # to None since the file has been unlinked
        pass
    return boxresult


def locateMax_opencv(template: str,
                     screenImage: str,
                     grayscale: bool = False,
                     confidence=0.9,
                     multiscale=False) -> Box:
    """Locate button using cv2.TemplateMatching algorithm

        Parameters
        ----------
        template : str
            The file location of the template image
        screenImage : PIL.Image
            The screenshot done using pyscreeze
        grayscale : bool
            Flag to run template matching using grayscale image
        confidence : float
            Confidence Threshold
        mulstiscale : bool
            Flag to run mulstiscale template matching from 1 to 0.8

        Returns
        -------
        Box
            a tuple of (x,y,w,h) of the best match
    """
    confidence = float(confidence)

    template = loadImage(template, grayscale)
    templateH, templateW = template.shape[:2]
    screenImage = loadImage(screenImage, grayscale)

    if (screenImage.shape[0] < template.shape[0] or
            screenImage.shape[1] < template.shape[1]):
        # avoid semi-cryptic OpenCV error below if bad size
        raise ValueError('needle dimension(s) exceed the haystack image or region dimensions')

    if multiscale:
        sizes = [1, 0.9, 0.85, 0.8]
        matchx, matchy = None, None
        with ThreadPoolExecutor() as executor:
            future_to_contour = {executor.submit(cv2.matchTemplate,
                                                 screenImage.copy(),
                                                 cv2.resize(template.copy(), (0, 0), fx=size, fy=size),
                                                 cv2.TM_CCORR_NORMED): size for size in sizes}
            for future in as_completed(future_to_contour):
                _, maxVal, _, maxLoc = cv2.minMaxLoc(future.result())
                if maxVal >= confidence:
                    confidence = maxVal
                    matchx = maxLoc[0]
                    matchy = maxLoc[1]
        if matchx is not None:
            return Box(matchx, matchy, templateW, templateH, maxVal)
        else:
            raise ImageNotFoundException

    result = cv2.matchTemplate(screenImage, template, cv2.TM_CCORR_NORMED)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    if len(result) == 0:
        raise ImageNotFoundException
    if maxVal >= confidence:
        matchx = maxLoc[0]
        matchy = maxLoc[1]

        return Box(matchx, matchy, templateW, templateH, maxVal)
    return


def loadImage(img2load,
              gray: bool):
    if type(img2load) is str:
        assert os.path.exists(img2load)
        return cv2.imread(img2load) if not gray else cv2.cvtColor(cv2.imread(img2load), cv2.COLOR_BGR2GRAY)
    return np.array(img2load) if not gray else cv2.cvtColor(np.array(img2load), cv2.COLOR_BGR2GRAY)