import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time


stream = cv2.VideoCapture(0)
flag = True

# Function to play the camera feed and control the speed
def play(Speed):
    global flag
    grabbed, frame = stream.read()
    if not grabbed:
        print("Failed to grab frame")
        return

  
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    # Update the canvas with the new frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)
    canvas.image = frame  

   
    if flag:
        canvas.create_text(130, 40, fill="yellow", font="Times 20 bold", text="Decision Pending")
    
    flag = not flag

def pending(decision):
   
    frame = cv2.cvtColor(cv2.imread("decision pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)
    canvas.image = frame

    time.sleep(2)


    if decision == "Out":
        decisionImg = "out.png"
        decision_label.config(text="Player is OUT!", fg="red")
    else:
        decisionImg = "not.png"
        decision_label.config(text="Player is NOT OUT!", fg="green")

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)
    canvas.image = frame


def Out():
    thread = threading.Thread(target=pending, args=("Out",))
    thread.daemon = True
    thread.start()

def Not_Out():
    thread = threading.Thread(target=pending, args=("Not Out",))
    thread.daemon = True
    thread.start()


SET_WIDTH = 800
SET_HEIGHT = 500

# Create the main application window
Window = tk.Tk()
Window.title("Decision Review System")
Window.geometry(f"{SET_WIDTH}x{SET_HEIGHT+100}")


canvas = tk.Canvas(Window, width=SET_WIDTH, height=SET_HEIGHT)
canvas.pack()


decision_label = tk.Label(Window, text="Waiting for decision...", font="Arial 16", fg="black")
decision_label.pack()

btn_frame = tk.Frame(Window)
btn_frame.pack(side=tk.BOTTOM, pady=20)


btn_prev_fast = tk.Button(btn_frame, text="<< Previous (Fast)", width=20, command=partial(play, -25))
btn_prev_fast.grid(row=0, column=0, padx=5)

btn_prev_slow = tk.Button(btn_frame, text="<< Previous (Slow)", width=20, command=partial(play, -2))
btn_prev_slow.grid(row=0, column=1, padx=5)

btn_next_slow = tk.Button(btn_frame, text="Next (Slow) >>", width=20, command=partial(play, 2))
btn_next_slow.grid(row=0, column=2, padx=5)

btn_next_fast = tk.Button(btn_frame, text="Next (Fast) >>", width=20, command=partial(play, 25))
btn_next_fast.grid(row=0, column=3, padx=5)


btn_out = tk.Button(btn_frame, text="Give Out", width=20, command=Out)
btn_out.grid(row=1, column=1, pady=10)

btn_not_out = tk.Button(btn_frame, text="Give Not Out", width=20, command=Not_Out)
btn_not_out.grid(row=1, column=2, pady=10)

Window.mainloop()
