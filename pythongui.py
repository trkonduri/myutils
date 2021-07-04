import tkinter as tk
from PIL import Image, ImageTk
import requests
import os
import urllib.request

WIDTH=500
HEIGHT=600

API_KEY = "22fae907b089b8f1732197bb568310d0"
url = "https://api.openweathermap.org/data/2.5/weather"

def test_function(x):
    print(f'Weather at {x} is : api.openweathermap.org/data/2.5/forecast?q={x}&appid={API_KEY}')



day = ['01d.png', '02d.png', '03d.png', '04d.png', '09d.png', '10d.png', '11d.png', '13n.png', '50d.png']
night = ['01n.png', '02n.png', '03n.png', '04n.png', '09n.png', '10n.png', '11n.png', '13n.png', '50n.png']

base_url = 'https://openweathermap.org/img/w/'
img_dir = './img/'
if not os.path.exists(img_dir):
	os.makedirs(img_dir)

# Get the day weather icons
for name in day:
	file_name = img_dir+name
	if not os.path.exists(file_name):
		urllib.request.urlretrieve(base_url+name, file_name)

# Repeat the same thing for night weather icons
for name in night:
	file_name = img_dir+name
	if not os.path.exists(file_name):
		urllib.request.urlretrieve(base_url+name, file_name)


def format_response(weather_json):
    try:
        name = weather_json["name"]
        description = weather_json["weather"][0]["description"]


        temp = weather_json["main"]["temp"]
        final_str = f'City: {name} \n Conditions: {description} \n Temparature: {temp}\u00b0F'
    except:
        final_str = "Error: There is a problem retreiving the data"

    return final_str

def get_weather(city):
    params = {'appid' : API_KEY, 'q' : city, 'units' : 'imperial' }
    response = requests.get(url,params)
    weather_json = response.json()
    print(weather_json)
    label["text"] = format_response(weather_json)
    icon = weather_json["weather"][0]["icon"]
    img_path = os.path.join(img_dir, icon + ".png")
    if  os.path.exists(img_path):
        size = int(lower_frame.winfo_height() * 0.25)
        img = ImageTk.PhotoImage(Image.open(img_path).resize((size, size)))
        weather_icon.delete("all")
        weather_icon.create_image(0, 0, anchor='nw', image=img)
        weather_icon.image = img
    else:
        weather_icon.delete("all")


#get_weather("san diego")



root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH,height=HEIGHT)
canvas.pack()
bg_image = ImageTk.PhotoImage(Image.open("./landscape.jpeg"))
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1,relheight=1)

#Image.open("./landscape.jpeg")
frame = tk.Frame(root, bg="#03ecfc",bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor="n")

entry = tk.Entry(frame, bg="gray", font=40)
entry.place(relwidth=0.65,relheight=1)

#button = tk.Button(frame, text="Get weather", command= lambda : test_function(entry.get()))
button = tk.Button(frame, text="Get weather", command= lambda : get_weather(entry.get()))

button.place(relx=0.7,rely=0,relwidth=0.3,relheight=1)

lower_frame = tk.Frame(root, bg="#03ecfc",bd=5)
lower_frame.place(relx=0.5,rely=0.25,relwidth=0.75,relheight=0.5,anchor="n")
label = tk.Label(lower_frame,font={'Modern``(',40})
label.place(relx=0,rely=0,relwidth=1,relheight=1)
weather_icon = tk.Canvas(label, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

root.mainloop()