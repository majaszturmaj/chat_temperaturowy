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
    print("Checking temperatures - THREAD STARTED")
    while True:
        prev_temperatures = copy.deepcopy(temperatures)
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

            if temp > prev_temp + 0.5:
            # if temp > prev_temperatures[i] + 0.5:  # check if the temperature is an outlier
                temp_rise = temp - prev_temp
                outlier_group[key] = temp_rise
                print("OUTLIERS:", outlier_group)
                
        if len(outlier_group) != 0:
            max_temp_key = max(outlier_group, key=outlier_group.get)
            chat()
            outlier_group = {}

        # # When a new temperature is available, put it in the queue
        # new_temperature = get_new_temperature()
        # new_temperatures.put(new_temperature)
    

active_robot_images = {1: "assets/friendlyrobotassistantwaving.png",
                       2: "assets/happyrobotassistantwavinghello.png",
                       3: "assets/robotassistanterror.png",
                       4: "assets/robotassistantsad.png",
                       5: "assets/robotassistantstandingandlooking.png"}


def chat():
    # Start the update_image function in a new thread
    print("Start update_image function in a new thread")
    update_image_thread.start()
    # threading.Thread(target=update_image, daemon=True).start()
    pass

def update_image():
    while True:
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

# Start the image update thread
update_image_thread = threading.Thread(target=update_image, daemon=True)



# window_thread = threading.Thread(target=window.mainloop, daemon=True)
# window_thread.start()
window.mainloop()