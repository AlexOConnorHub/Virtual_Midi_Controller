import helper
import mido
import mido.backends.rtmidi

TYPES = {
    "note": ["channel", "note", "velocity"],
    # "note_on": ["channel", "note", "velocity"],
    # "note_off": ["channel", "note", "velocity"],
    "polytouch": ["channel", "note", "value"],
    "control_change": ["channel", "control", "value"],
    "program_change": ["channel", "program"],
    "aftertouch": ["channel", "value"],
    "pitchwheel": ["channel", "pitch"],
    "sysex": ["data"],
    "quarter_frame": ["frame_type", "frame_value"],
    "songpos": ["pos"],
    "song_select": ["song"],
    "tune_request": [],
    "clock": [],
    "start": [],
    "continue": [],
    "stop": [],
    "active_sensing": [],
    "reset": [],
}
class midi:
    """Provides a simpe interface for sending and receiving MIDI messages.
    """
    def __init__(this) -> None:
        this.input = mido.open_input("Virtual_Midi_Keyboard", virtual=True)
        this.output = mido.open_output("Virtual_Midi_Controller", virtual=True)

    def __del__(this) -> None:
        this.input.close()
        this.output.close()

    def send(this, message: mido.Message) -> None:
        """Sends the message to the output.

        Args:
            message (mido.Message): Message being sent
        """
        print("Sending message: " + str(message.dict()))
        this.output.send(message)
        
    def getButtonMessage(this, button: int) -> mido.Message:
        """Returns the message to be sent when a button is pressed.

        Args:
            button (int): Button ID

        Returns:
            mido.Message: Message configured for the button
        """
        contents = helper.getSetting("buttons")[button].get("command")
        if (contents is None):
            return None
        return mido.Message.from_dict(contents)
    
    def setButtonMessage(this, button: int, contents: mido.Message) -> None:
        """Sets the message to be sent when a button is pressed.

        Args:
            button (int): Button ID
            contents (mido.Message): The message to send
        """
        buttonSettings = helper.getSetting("buttons")
        buttonSettings[button]["command"] = contents.dict()
        helper.setSetting("buttons", buttonSettings)
        
    def getNoteOffMessage(this, message: mido.Message) -> mido.Message:
        return mido.Message("note_off", note=message.note, velocity=message.velocity, channel=message.channel)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
