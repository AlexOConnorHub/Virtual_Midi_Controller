import datetime
from json import loads, dumps
import os

def log(str: str) -> None:
    """Logs a message to log.txt

    Args:
        str (str): Message
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S - ")
    open("log.txt", "a").write(f"{timestamp} {str}\n")

def getString(str: str, returnNoneOnError: bool = False) -> str:
    """Gets a string from the translation file.

    Args:
        str (str): English string
        returnNoneOnError (bool, optional): Return `None` on error. Defaults to False.

    Returns:
        str: String to use
    """
    strings = loads(open("translation.json", "r").read())
    localLanguage = getSetting("language")
    if localLanguage is None:
        initSettings()
    if (localLanguage in strings.get("supported_languages")):
        localLanguage = strings.get("supported_languages")[localLanguage]
    else:
        localLanguage = "en"
    if ((str in strings) and (localLanguage in strings[str])):
        return strings[str][localLanguage]
    log(f"String '{str}' not found in translation.json")
    if (returnNoneOnError): 
        return None
    else:
        return str
    
def addString(str: str) -> None:
    """Adds string to translation file. This is only useful for developers.

    Args:
        str (str): English string
    """
    strings = loads(open("translation.json", "r").read())
    if (str not in strings):
        strings[str] = { "en": str }
        open("translation.json", "w").write(dumps(strings, indent=4))

def getSetting(str: str) -> str:
    """Gets a setting from settings.json

    Args:
        str (str): Setting name

    Returns:
        str: Setting value
    """
    if (not os.path.exists("settings.json")):
        open("settings.json", "w").write("{}")
        initSettings()
    settings = loads(open("settings.json", "r").read())
    if (str in settings):
        return settings[str]
    else:
        return None
    
def setSetting(str: str, value: str) -> None:
    """Sets a setting in settings.json

    Args:
        str (str): Setting name
        value (str): Setting value
    """
    settings = loads(open("settings.json", "r").read())
    settings[str] = value
    open("settings.json", "w").write(dumps(settings, indent=4))
    
def initSettings() -> None:
    """Initializes settings.json with default values.
    """
    if (getSetting("language") is None):
        setSetting("language", "English")
    if (getSetting("rowCount") is None):
        setSetting("rowCount", 3)
    if (getSetting("columnCount") is None):
        setSetting("columnCount", 4)
        
def validateNumber(str: str, min: int, max: int) -> bool:
    """Checks if a string is a number, and if it is within a range. Also returns True if empty

    Args:
        str (str): String to check
        min (int): Minimum value
        max (int): Maximum value

    Returns:
        bool: True if number, False if not
    """
    try:
        if (str == ""):
            return True
        inputVal = int(str)
        return (inputVal >= int(min) and inputVal <= int(max))
    except ValueError:
        return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
