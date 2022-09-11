import datetime
from json import loads, dumps
import doctest
import os

def log(str: str) -> None:
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S - ")
    open("log.txt", "a").write(f"{timestamp} {str}\n")

def getString(str: str, returnNoneOnError: bool = False) -> str:
    strings = loads(open("translation.json", "r").read())
    localLanguage = getSetting("language")
    if localLanguage is None:
        initSettings()
    if (str in strings and localLanguage in strings[str]):
        return strings[str][localLanguage]
    log(f"String '{str}' not found in translation.json")
    if (returnNoneOnError): 
        return None
    else:
        return str
    
def addString(str: str) -> None:
    strings = loads(open("translation.json", "r").read())
    if (str not in strings):
        strings[str] = { "en": str }
        open("translation.json", "w").write(dumps(strings, indent=4))

def getSetting(str: str) -> str:
    if (not os.path.exists("settings.json")):
        open("settings.json", "w").write("{}")
    settings = loads(open("settings.json", "r").read())
    if (str in settings):
        return settings[str]
    else:
        return None
    
def setSetting(str: str, value: str) -> None:
    settings = loads(open("settings.json", "r").read())
    settings[str] = value
    open("settings.json", "w").write(dumps(settings, indent=4))
    
def initSettings() -> None:
    if (getSetting("language") is None):
        setSetting("language", "en")

if __name__ == "__main__":
    doctest.testmod()