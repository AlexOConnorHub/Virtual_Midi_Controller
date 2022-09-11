import tkinter as tk
import midi
import mido
import helper

# Create gui clas
class gui():
    # constructor
    def __init__(this):
        this.root = tk.Tk()
        this.root.title(helper.getString("Virtual Midi Controller"))
        
        # Create top menu bar
        this.optionBar = tk.Menu(this.root)
        this.editMenu = tk.Menu(this.optionBar, tearoff=0)
        this.editMenu.add_command(label="Undo")
        this.editMenu.add_command(label="Redo")
        this.optionBar.add_cascade(label="Edit", menu=this.editMenu)
        this.root.config(menu=this.optionBar)

        # Create main frame
        this.mainFrame = tk.Frame(this.root)
        this.mainFrame.pack(fill=tk.BOTH, expand=True)
        
        # Add 3 x 4 button grid
        for i in range(3):
            for j in range(4):
                this.button = tk.Button(this.mainFrame, text=f"Key {this.convertButtonNumberToKey(i*4+j)}", command=lambda i=i, j=j: this.buttonPress(i*4+j))
                this.button.grid(row=i, column=j, sticky="nsew")

        this.midi = midi.midi()

        this.root.mainloop()

    def buttonPress(this, button: int):
        message = mido.Message("control_change", control=7, value=this.convertButtonNumberToMidiValue(button))
        this.midi.send(message)
        print(f"Sending message: {message} from button {this.convertButtonNumberToKey(button)}")
        
    def convertButtonNumberToKey(this, button: int) -> int:
        if (button == 0):
            return "C"
        elif (button == 1):
            return "C#"
        elif (button == 2):
            return "D"
        elif (button == 3):
            return "D#"
        elif (button == 4):
            return "E"
        elif (button == 5):
            return "F"
        elif (button == 6):
            return "F#"
        elif (button == 7):
            return "G"
        elif (button == 8):
            return "G#"
        elif (button == 9):
            return "A"
        elif (button == 10):
            return "A#"
        elif (button == 11):
            return "B"
        
    def convertButtonNumberToMidiValue(this, button: int) -> int:
        if (button == 0):
            return 0
        elif (button == 1):
            return 10
        elif (button == 2):
            return 20
        elif (button == 3):
            return 30
        elif (button == 4):
            return 40
        elif (button == 5):
            return 50
        elif (button == 6):
            return 60
        elif (button == 7):
            return 70
        elif (button == 8):
            return 80
        elif (button == 9):
            return 90
        elif (button == 10):
            return 100
        elif (button == 11):
            return 110
        

if __name__ == "__main__":
    gui()