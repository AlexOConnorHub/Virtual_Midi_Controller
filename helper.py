from json import loads, dumps
from os import path, makedirs
from translation_strings import translated_strings as ts
from platformdirs import user_data_dir

def getString(str: str, returnNoneOnError: bool = False) -> str:
    """Gets a string from the translation file.

    Args:
        str (str): English string
        returnNoneOnError (bool, optional): Return `None` on error. Defaults to False.

    Returns:
        str: String to use
    """
    localLanguage = getSetting("language")
    if localLanguage is None:
        initSettings()
    if (localLanguage in ts.get("supported_languages")):
        localLanguage = ts.get("supported_languages")[localLanguage]
    else:
        localLanguage = "en"
    if ((str in ts)):
        if (localLanguage in ts[str]):
            return ts[str][localLanguage]
        elif ("en" in ts[str]):
            print(f"String '{str}' not translated to {localLanguage} in translation_strings.py")
            return ts[str]["en"]
    print(f"String '{str}' not found in translation_strings.py")
    if (returnNoneOnError): 
        return None
    else:
        return str

def getSetting(str: str) -> str:
    """Gets a setting from settings.json

    Args:
        str (str): Setting name

    Returns:
        str: Setting value
    """
    if (not path.exists(getSettingLocation())):
        makedirs(path.dirname(getSettingLocation()), exist_ok=True)
        open(getSettingLocation(), "w").write("{}")
        initSettings()
    settings = loads(open(getSettingLocation(), "r").read())
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
    settings = loads(open(getSettingLocation(), "r").read())
    settings[str] = value
    open(getSettingLocation(), "w").write(dumps(settings, indent=4))
    
def getSettingLocation() -> str:
    """_summary_

    Returns:
        str: path to settings.json
    """
    return path.join(user_data_dir("Virtual Midi Controller"), "settings.json")
    
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
