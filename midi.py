import doctest
import helper
import mido

class midi:
    def __init__(this) -> None:
        this.input = mido.open_input("Virtual_Midi_Keyboard", virtual=True)
        this.output = mido.open_output("Virtual_Midi_Controller", virtual=True)

    def __del__(this) -> None:
        this.input.close()
        this.output.close()

    def send(this, message: mido.Message) -> None:
        this.output.send(message)

if __name__ == "__main__":
    doctest.testmod()