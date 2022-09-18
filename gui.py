import helper
import midi
import mido
from sys import platform
import tkinter as tk
from tkinter import messagebox
from translation_strings import translated_strings as ts

class gui:
    """When initialized, this class will create a window for the user to interact with.
    """
    def __init__(this):
        this.midi = midi.midi()
        this.root = tk.Tk()
        # Right click on control edit popup
        this.editPopup = tk.Toplevel(this.root)
        this.editPopup.protocol("WM_DELETE_WINDOW", this.editPopup.withdraw)
        this.editPopup.withdraw()
        this.editChannelLabel = tk.Entry(this.editPopup)
        this.editChannelLabel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        this.editChannelLabelLabel = tk.Label(this.editPopup)
        this.editChannelLabelLabel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        this.editDropdownVar = tk.StringVar(this.editPopup)
        this.editDropdown = tk.OptionMenu(this.editPopup, this.editDropdownVar, *[key.capitalize().replace("_", " ") for key in midi.TYPES.keys()], command=this.dropdownCallbackEdit)
        this.editDropdown.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        this.editDropdownLabel = tk.Label(this.editPopup)
        this.editDropdownLabel.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        this.editInputs = []
        this.editInputLabels = []

        # Preferences popup
        this.preferencesPopup = tk.Toplevel(this.root)
        this.preferencesPopup.protocol("WM_DELETE_WINDOW", this.preferencesPopup.withdraw)
        this.preferencesPopup.withdraw()
        this.languageDropdownVar = tk.StringVar(this.preferencesPopup)
        this.languageDropdownVar.set(helper.getSetting("language"))
        this.languages = ts["supported_languages"]
        this.preferencesLanguageDropdown = tk.OptionMenu(this.preferencesPopup, this.languageDropdownVar, *list(this.languages.keys()), command=this.dropdownCallbackSetting)
        this.preferencesLanguageDropdown.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        this.preferencesLanguageLabel = tk.Label(this.preferencesPopup)
        this.preferencesLanguageLabel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        this.preferencesRowCountStepper = tk.Spinbox(this.preferencesPopup, from_=1, to=10, command=this.rowSpinnerCallback)
        this.preferencesRowCountStepper.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        this.preferencesRowCountStepper.bind("<Key>", lambda e: "break")
        this.preferencesRowCountStepper.delete(0, tk.END)
        this.preferencesRowCountStepper.insert(0, helper.getSetting("rowCount"))
        this.preferencesRowCountLabel = tk.Label(this.preferencesPopup)
        this.preferencesRowCountLabel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        this.preferencesColumnCountStepper = tk.Spinbox(this.preferencesPopup, from_=1, to=10, command=this.columnSpinnerCallback)
        this.preferencesColumnCountStepper.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        this.preferencesColumnCountStepper.bind("<Key>", lambda e: "break")
        this.preferencesColumnCountStepper.delete(0, tk.END)
        this.preferencesColumnCountStepper.insert(0, helper.getSetting("columnCount"))
        this.preferencesColumnCountLabel = tk.Label(this.preferencesPopup)
        this.preferencesColumnCountLabel.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Create top menu bar
        this.optionBar = tk.Menu(this.root)
        this.editMenu = tk.Menu(this.optionBar, tearoff=0)
        this.editMenu.add_command(command=this.preferencesPopup.deiconify)
        this.editMenu.add_command(command=lambda :  messagebox.showinfo(title=helper.getString("About"), message=helper.getString("About Message")))
        this.editMenu.add_command(command=this.root.quit)
        # 
        this.optionBar.add_cascade(menu=this.editMenu)
        this.root.config(menu=this.optionBar)

        # Create main frame
        this.setGlobalStrings()
        this.mainFrame = tk.Frame(this.root)
        this.mainFrame.pack(fill=tk.BOTH, expand=True)
        this.buttons = []
        this.renderMainWindow()
        this.root.mainloop()
        
    def setGlobalStrings(this) -> None:
        """Sets all the strings in the gui to the current language
        """
        this.root.title(helper.getString("Virtual Midi Controller"))
        this.editPopup.title(helper.getString("Edit Midi Message"))
        this.preferencesPopup.title(helper.getString("Preferences"))
        this.editChannelLabelLabel.config(text=helper.getString("Channel Name"))
        this.editDropdownLabel.config(text=helper.getString("Type of Midi Message"))
        this.preferencesLanguageLabel.config(text=helper.getString("Prefered Language"))
        this.preferencesRowCountLabel.config(text=helper.getString("Row Count"))
        this.preferencesColumnCountLabel.config(text=helper.getString("Column Count"))
        this.editMenu.entryconfig(0, label = helper.getString("Preferences"))
        this.editMenu.entryconfig(1, label = helper.getString("About"))
        this.editMenu.entryconfig(2, label = helper.getString("Quit"))
        this.optionBar.entryconfig(1, label = helper.getString("Window"))

    def renderMainWindow(this) -> None:
        """Renders the main window.
        """
        # For each this.buttons, delete it
        for button in this.buttons:
            button.destroy()
        this.buttons = []
        row = helper.getSetting("rowCount")
        col = helper.getSetting("columnCount")
        for i in range(row):
            for j in range(col):
                buttonId = len(this.buttons)
                this.buttons.append(tk.Button(this.mainFrame, text=this.getButtonText(buttonId), height=5, width=10))
                this.buttons[-1].grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                this.buttons[-1].bind("<Button-1>", lambda e, button=buttonId: this.buttonPress(e, button))
                this.buttons[-1].bind("<ButtonRelease-1>", lambda e, id=buttonId: this.releaseButton(e, id))
                if (platform == "darwin"):
                    this.buttons[-1].bind("<Button-2>", lambda e, id=buttonId: this.eventRightClickMenu(e, id))
                else:
                    this.buttons[-1].bind("<Button-3>", lambda e, id=buttonId: this.eventRightClickMenu(e, id))

    def buttonPress(this, e, button: int):
        """Function called when a button is pressed.

        Args:
            e (tk.Event): Event
            button (int): Button ID
        """
        message = this.midi.getButtonMessage(button)
        if (message is None):
            return
        this.midi.send(message)
        
    def releaseButton(this, e, button: int):
        """Function called when a button is released.

        Args:
            e (tk.Event): Event
            button (int): Button ID
        """
        message = this.midi.getButtonMessage(button)
        if (message is None):
            return
        if (message.type == "note_on"):
            this.midi.send(this.midi.getNoteOffMessage(message))

    def getButtonText(this, button: int) -> str:
        """Gets the text for the button.

        Args:
            button (int): Button ID

        Returns:
            str: Text for the button
        """
        text = helper.getSetting("buttons")
        if ( text is None or len(text) <= button):
            text = str(button + 1)
            this.setButtonText(button, text)
            text = helper.getSetting("buttons")
        return text[button]["label"]

    def setButtonText(this, button: int, text: str) -> None:
        """Handles setting the text for a button.

        Args:
            button (int): Button ID
            text (str): Text for the button
        """
        buttonSettings = helper.getSetting("buttons")
        if (buttonSettings is None):
            buttonSettings = []
        while (len(buttonSettings) <= button):
            buttonSettings.append({"label": str(button + 1), "command": {"type": "control_change", "channel": 0, "control": 0, "value": 127}})
        buttonSettings[button]["label"] = text
        if (button < len(this.buttons)):
            btnToChange = this.buttons[button]
            btnToChange.config(text=text)
        helper.setSetting("buttons", buttonSettings)

    def eventRightClickMenu(this, e, button: int) -> None:
        """Handles right click menu.

        Args:
            button (int): Button ID
        """
        this.editingButton = button
        this.editChannelLabel.delete(0, tk.END)
        this.editChannelLabel.insert(0, this.getButtonText(button))
        currMidi = this.midi.getButtonMessage(button)
        if (currMidi is not None):
            currMidiType = currMidi.type
            if (currMidiType == "note_on"):
                this.editDropdownVar.set("Note")
            else:
                this.editDropdownVar.set(currMidiType.capitalize().replace("_", " "))
        this.dropdownCallbackEdit(this.editDropdownVar.get())
        this.editPopup.deiconify()

    def dropdownCallbackEdit(this, value:str) -> None:
        """Handles dropdown menu.
        
        Args:
            value (str): Value of the dropdown menu
        """
        for editInput in this.editInputs:
            editInput.destroy()
        for editInputLabel in this.editInputLabels:
            editInputLabel.destroy()
        this.editInputs = []
        this.editInputLabels = []
        currMidi = this.midi.getButtonMessage(this.editingButton)
        value = value.lower().replace(" ", "_")
        if (value == "Note"):
            value = "note_on"
        inputs = midi.TYPES.get(value, [])
        nextRow = 2 # Rows 0 and 1 are always used
        for input in inputs:
            if (input == "data"):
                # Input textbox
                this.editInputs.append(tk.Entry(this.editPopup))
                this.editInputs[-1].grid(row=nextRow, column=0, sticky="w")
                this.editInputLabels.append(tk.Label(this.editPopup, text=helper.getString("Data")))
                this.editInputLabels[-1].grid(row=nextRow, column=1, sticky="w")
            else:
                this.editInputs.append(tk.Spinbox(this.editPopup, from_=(1 if input == "channel" else 0), to=(16 if input == "channel" else 127)))
                this.editInputs[-1].grid(row=nextRow, column=0, sticky="nsew", padx=5, pady=5)
                if (currMidi is not None):
                    data = getattr(currMidi, input, 0)
                    if (input == "channel"):
                        data += 1
                    this.editInputs[-1].delete(0, tk.END)
                    this.editInputs[-1].insert(0, data)
            # this.editInputs[-1].bind("<Key>", lambda e: "break") # This disables keyboard input on the spinbox
            this.editInputLabels.append(tk.Label(this.editPopup, text=helper.getString(input.capitalize())))
            this.editInputLabels[-1].grid(row=nextRow, column=1, sticky="nsew", padx=5, pady=5)
            nextRow += 1
        # Add save and cancel buttons
        this.editInputs.append(tk.Button(this.editPopup, text=helper.getString("Save"), command=this.saveEdit))
        this.editInputs[-1].grid(row=nextRow, column=0, sticky="nsew", padx=5, pady=5)
        this.editInputs.append(tk.Button(this.editPopup, text=helper.getString("Cancel"), command=this.editPopup.withdraw))
        this.editInputs[-1].grid(row=nextRow, column=1, sticky="nsew", padx=5, pady=5)

    def dropdownCallbackSetting(this, value):
        """Handles dropdown menu.

        Args:
            value (str): Value of the dropdown menu
        """
        helper.setSetting("language", value)
        this.setGlobalStrings()
        
    def columnSpinnerCallback(this):
        """Handles column spinner.
        """
        helper.setSetting("columnCount", int(this.preferencesColumnCountStepper.get()))
        this.renderMainWindow()
    
    def rowSpinnerCallback(this):
        """Handles row spinner.
        """
        helper.setSetting("rowCount", int(this.preferencesRowCountStepper.get()))
        this.renderMainWindow()
        
    def saveEdit(this):
        """Saves the edit.
        """
        this.editPopup.withdraw()
        saveName = this.editChannelLabel.get()
        this.setButtonText(this.editingButton, saveName)
        midoType = this.editDropdownVar.get().lower().replace(" ", "_")
        if (midoType == "sysex"):
            data = {"type": midoType, "data": [int(x) for x in this.editInputs[0].get().split(" ")]}
        else:
            dataPointLabels = midi.TYPES.get(midoType)
            if (dataPointLabels is None):
                print(f"Invalid type: {midoType}")
                return
            dataPoints = [ int(this.editInputs[i].get()) for i in range(len(dataPointLabels)) ]
            data = dict(zip(dataPointLabels, dataPoints))
            data["type"] = midoType if (midoType != "note") else "note_on"
            if (data.get("channel") is not None):
                data["channel"] -= 1
        msg = mido.Message(**data)
        this.midi.setButtonMessage(this.editingButton, msg)

if __name__ == "__main__":
    gui = gui()
