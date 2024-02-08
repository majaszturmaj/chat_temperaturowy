import threading
import queue
from flask import Flask, request
import time
import copy
import random
from pathlib import Path
from tkinter import Tk
from tkinter import Canvas
from tkinter import Entry
from tkinter import Text
from tkinter import Button
from tkinter import PhotoImage
import subprocess

app = Flask(__name__)
app.debug = False
app.use_reloader = False

# Create a queue to hold the new temperatures
new_temperatures = queue.Queue()

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.form.to_dict()
    crc_id = data['crc_id']
    temp = data['temperature']
    temperatures[crc_id] = temp
    update_canvas()
    return 'Data received successfully', 200

def run_server():
    app.run(host='0.0.0.0', port=5000, threaded=True)  # Ensure threaded mode

# Run the server in a separate thread
print("Running the server in a separate thread")
server_thread = threading.Thread(target=run_server)
server_thread.start()

temperatures = {"b7": 0.00,
                "56": 0.00,
                "a5": 0.00,
                "1d": 0.00,
                "d5": 0.00,
                "fd": 0.00}
print(temperatures)

def update_canvas():
    for measurement in temperatures:
        update_temperature(measurement, temperatures[measurement])
    calc_average_temperature()


# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/maja/Tools/Tkinter-Designer/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_color(temperature):
    # Convert temperature to a float
    temperature = float(temperature)

    # Clamp temperature between 0 and 40
    clamped_temp = max(0, min(40, temperature))

    # Convert temperature to a value between 0 and 1
    temp_ratio = clamped_temp / 40.0

    # Calculate red and blue components
    red = int(255 * temp_ratio)
    blue = int(255 * (1 - temp_ratio))

    # Convert to hexadecimal and return
    return f"#{red:02x}{blue:02x}80"

def update_temperature(measurement, new_temperature):
    color = get_color(new_temperature)
    # Update the text object associated with the measurement
    canvas.itemconfig(text_objects[measurement], text=f"{new_temperature} °C")
    # Update the rectangle object associated with the measurement
    canvas.itemconfig(rect_objects[measurement], fill=color)

def calc_average_temperature():
    mean = sum(float(value) for value in temperatures.values()) / len(temperatures)
    canvas.itemconfig(average_temperature, text=f"Average temperature: {mean:.2f} °C")


window = Tk()

window.geometry("1920x1080")
window.configure(bg = "#29252C")



canvas = Canvas(
    window,
    bg = "#29252C",
    height = 1080,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

canvas.create_rectangle(
    1008.0,
    153.0,
    1754.0,
    694.0,
    fill="#1A171C",
    outline="")

# temperature fields ############################################################################################################

rect_objects = {}

# first row ##################

rect_objects['d5'] = canvas.create_rectangle(
    992.0,
    134.0,
    1231.0,
    401.0,
    fill="#D9D9D9",
    outline="")

rect_objects['fd'] = canvas.create_rectangle(
    1231.0,
    134.0,
    1471.0,
    401.0,
    fill="#D9D9D9",
    outline="")

rect_objects['1d'] = canvas.create_rectangle(
    1470.0,
    134.0,
    1710.0,
    401.0,
    fill="#D9D9D9",
    outline="")

# second row ##################

rect_objects['56'] = canvas.create_rectangle(
    992.0,
    401.0,
    1231.0,
    668.0,
    fill="#D9D9D9",
    outline="")

rect_objects['b7'] = canvas.create_rectangle(
    1231.0,
    401.0,
    1471.0,
    668.0,
    fill="#D9D9D9",
    outline="")

rect_objects['a5'] = canvas.create_rectangle(
    1471.0,
    401.0,
    1711.0,
    668.0,
    fill="#D9D9D9",
    outline="")

# temperatures ############################################################################################################

# Create a dictionary to store the text objects
text_objects = {}

# first row ##################

text_objects['d5'] = canvas.create_text(
    1065.0,
    249.0,
    anchor="nw",
    text="0.00 °C",
    fill="#36485E",
    font=("Inter", 20 * -1)
)

text_objects['fd'] = canvas.create_text(
    1304.0,
    249.0,
    anchor="nw",
    text="0.00 °C",
    fill="#36485E",
    font=("Inter", 20 * -1)
)

text_objects['1d'] = canvas.create_text(
    1543.0,
    249.0,
    anchor="nw",
    text="0.00 °C",
    fill="#36485E",
    font=("Inter", 20 * -1)
)

# second row ##################

text_objects['56'] = canvas.create_text(
    1065.0,
    521.0,
    anchor="nw",
    text="0.00 °C",
    fill="#36485E",
    font=("Inter", 20 * -1)
)

text_objects['b7'] = canvas.create_text(
    1304.0,
    521.0,
    anchor="nw",
    text="0.00 °C",
    fill="#36485E",
    font=("Inter", 20 * -1)
)

text_objects['a5'] = canvas.create_text(
    1543.0,
    521.0,
    anchor="nw",
    text="0.00 °C",
    fill="#36485E",
    font=("Inter", 20 * -1)
)






average_temperature = canvas.create_text(
    1069.0,
    785.0,
    anchor="nw",
    text="Average temperature: 0.00 °C",
    fill="#9EFFA9",
    font=("Inter", 40 * -1)
)

# Load the image
robot_image = PhotoImage(file="assets/robotassistantsleeping.png")

image_id = canvas.create_image(530, 505, image=robot_image)

# canvas.create_rectangle(
#     260.0,
#     255.0,
#     800.0,
#     755.0,
#     fill="#FFFFFF",
#     outline="")


window.resizable(False, False)
window.title("Chat temperaturowy")


outlier_group = {}
def check_temperatures():
    time.sleep(10) # Wait for admin to start sending data
    print("Checking temperatures - THREAD STARTED")
    while True:
        prev_temperatures = copy.deepcopy(temperatures)
        outlier_group = {}
        time.sleep(5)
        print("Checking temperatures................................................................")
        print()
        print(prev_temperatures)
        print(temperatures)
        print()
        for key, temp in temperatures.items():
            # Convert temp to float
            temp = float(temp)

            # Use dict.get() to provide a default value if the key does not exist
            # Convert prev_temp to float
            prev_temp = float(prev_temperatures[key])

            print(temp, "                            ", prev_temp)

            if temp > prev_temp + 0.5: # check if the temperature is an outlier
                temp_rise = temp - prev_temp
                outlier_group[key] = temp_rise
                print("OUTLIERS:", outlier_group)
                
        if len(outlier_group) != 0:
            max_temp_key = max(outlier_group, key=outlier_group.get)
            print("MAX TEMP KEY:", max_temp_key)
            outlier_group = {}
            chat(max_temp_key)
    
start_commands = {"1d": "test psychologiczny",
                  "b7": "quiz o informatyce",
                  "d5": "quiz o robotach",
                  "fd": "quiz o programowaniu",
                  "a5": "quiz o sztucznej inteligencji",
                  "56": "test psychologiczny w języku angielskim"}

test_commands_pl = {"1d": "Tak",
                    "b7": "Nie",
                    "d5": "Nie wiem",
                    "56": "Wyjście"}

test_commands_eng = {"1d": "Yes",
                     "b7": "No",
                     "d5": "I don't know",
                     "56": "Exit"}

quiz_commands = {"1d": "A",
                 "d5": "B",
                 "a5": "C",
                 "56": "Wyjście",}

game_mode = False

def chat(choosen_key):
    global game_mode
    print("Start update_image function in a thread")
    stop_update_image_flag.clear()

    if game_mode == False:
        stop_update_image_flag.clear()
        print("Open ChatGPT application")
        send_shell_command("adb shell am start -n com.openai.chatgpt/.MainActivity")

        print("Start choosen game mode")

        print("Out of Start mode")
        game_mode = start_commands[choosen_key]

        text = start_commands[choosen_key]
        print("Writing start command:", text)

        # Split the text into words
        words = text.split()
        time.sleep(1)
        for word in words:
            input = f"adb shell input text {word}"
            print(input)
            send_shell_command(input)
            send_shell_command("adb shell input keyevent 62")  # 62 is the key code for the space key

        print("Sending start command")
        send_shell_command("adb shell input tap 1000 1400")  # tap the send button

        time.sleep(2)

        print("Reading the response")
        send_shell_command("adb shell input touchscreen swipe 500 650 500 650 1000")
        send_shell_command("adb shell input tap 700 1400")

    elif game_mode == True:
        send_shell_command("adb shell input tap 500 2200") # tap the text field
        if choosen_key == "56":
            game_mode = False
            stop_update_image_flag.set()
            send_shell_command("adb shell am force-stop com.openai.chatgpt")

    elif game_mode == "test psychologiczny":

        print("Sending Tak/Nie/Nie wiem/Wyjście")
        try:
            # Attempt to get the command
            text = test_commands_pl[choosen_key]
        except KeyError:
            # Handle the exception if the key is not in the dictionary
            print("Invalid option. Please choose a valid key.")
        else:
            words = text.split()
            send_shell_command("adb shell input tap 500 2200") # tap the text field
            time.sleep(1)
            for word in words:
                input = f"adb shell input text {word}"
                print(input)
                send_shell_command(input)
                send_shell_command("adb shell input keyevent 62")  # 62 is the key code for the space key

            send_shell_command("adb shell input tap 1000 1400")  # tap the send button
            time.sleep(2)
        

        print("Reading the response")
        send_shell_command("adb shell input touchscreen swipe 500 650 500 650 1000")
        send_shell_command("adb shell input tap 700 1400")
    
        if choosen_key == "56":
            game_mode = False
            stop_update_image_flag.set()
            send_shell_command("adb shell am force-stop com.openai.chatgpt")

    elif game_mode == "test psychologiczny w języku angielskim":

        
        print("Sending Yes/No/I don't know/Exit")
        try:
            # Attempt to get the command
            text = test_commands_eng[choosen_key]
        except KeyError:
            # Handle the exception if the key is not in the dictionary
            print("Invalid option. Please choose a valid key.")
        else:
            words = text.split()
            time.sleep(1)
            send_shell_command("adb shell input tap 500 2200") # tap the text field
            for word in words:
                input = f"adb shell input text {word}"
                print(input)
                send_shell_command(input)
                send_shell_command("adb shell input keyevent 62")  # 62 is the key code for the space key

            send_shell_command("adb shell input tap 1000 1400")
            time.sleep(2)

        print("Reading the response")
        send_shell_command("adb shell input touchscreen swipe 500 650 500 650 1000")
        send_shell_command("adb shell input tap 700 1400")

        if choosen_key == "56":
            game_mode = False
            stop_update_image_flag.set()
            send_shell_command("adb shell am force-stop com.openai.chatgpt")
    
    elif game_mode == "quiz o informatyce" or game_mode == "quiz o robotach" or game_mode == "quiz o programowaniu" or game_mode == "quiz o sztucznej inteligencji":

        print("Sending A/B/C/Wyjście")
        try:
            # Attempt to get the command
            text = quiz_commands[choosen_key]
        except KeyError:
            # Handle the exception if the key is not in the dictionary
            print("Invalid option. Please choose a valid key.")
        else:
            words = text.split()
            time.sleep(1)
            send_shell_command("adb shell input tap 500 2200") # tap the text field
            for word in words:
                input = f"adb shell input text {word}"
                print(input)
                send_shell_command(input)
                send_shell_command("adb shell input keyevent 62")  # 62 is the key code for the space key

            send_shell_command("adb shell input tap 1000 1400")
            time.sleep(2)

        print("Reading the response")
        send_shell_command("adb shell input touchscreen swipe 500 650 500 650 1000")
        send_shell_command("adb shell input tap 700 1400")

        if choosen_key == "56":
            game_mode = False
            stop_update_image_flag.set()
            send_shell_command("adb shell am force-stop com.openai.chatgpt")

    text = None
    print("End of chat function")

def send_shell_command(command):
    print("Executing command:", command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Print the output
    print("Output:", result.stdout.strip())

    # Print any errors
    if result.stderr:
        print("Errors:", result.stderr.strip())
    

active_robot_images = {1: "assets/friendlyrobotassistantwaving.png",
                       2: "assets/happyrobotassistantwavinghello.png",
                       3: "assets/robotassistanterror.png",
                       4: "assets/robotassistantsad.png",
                       5: "assets/robotassistantstandingandlooking.png"}


def update_image():
    while not stop_update_image_flag.is_set():
        # Choose a random image
        new_image_path = random.choice(list(active_robot_images.values()))
        new_image = PhotoImage(file=new_image_path)
        print("Random image chosen")

        # Update the image on the canvas using after() to schedule the update on the main thread
        canvas.after(0, lambda: canvas.itemconfig(image_id, image=new_image))
        print("Image updated")

        # Wait for a random interval between 3 and 6 seconds
        time.sleep(random.uniform(3, 6))



# Start the background thread
print("Here the background thread starts")
check_temp_thread = threading.Thread(target=check_temperatures, daemon=True)
check_temp_thread.start()

# the image update thread
# Define a flag to control the thread
stop_update_image_flag = threading.Event()
stop_update_image_flag.set()
update_image_thread = threading.Thread(target=update_image, daemon=True)

window.mainloop()