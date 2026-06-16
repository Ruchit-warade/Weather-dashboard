import requests,json,sys
#This weather dashboard gives the current weather report using openweatherapp api key integration

#Funtion mon created for changing data format form yyyy-mm-dd hh:mm:ss to dd month
try:
    def mon(x):
        text = x
        month = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr","05":"May","06":"Jun","07":"Jul", "08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
        mon = text[5:7]
        day = text[8:10]
        for i in month:
            if(i==mon):
                mon=month[i]
        return f"  {day} {mon}"        

    #Open json file containing country and their country codes
    with open("countrycodes.json","r") as f:
        country = json.load(f)

    print("======================================")
    print("||        WEATHER DASHBOARD         ||")
    print("======================================")
    
    while True:
        name = input("🌏 Enter the country of which you want to check weather(First Letter Uppercase) :-")
        try:
            cou=""
            for i in country:
                if(name == country[i]):
                    cou = i
            if(cou==""):
                print("Country not found.Please check for spelling mistakes.") 
            else:
                break                  
        except Exception as err:
            print(f"An Error Ocurred as {err}.")

    #Pincode/Postal code API to give latitude and longitude of Pincode/Postal Code        
    try:
        zip = input("📮 Enter your PIN Code/Postal Code:- ")

        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},{cou}&appid=<your_api_key>"
        api_key = "<your_api_key>"

        # Define your authorization headers
        headers = {
            "Accept": "application/json",
            "X-API-Key": api_key
        }

        response = requests.get(url, headers=headers)
        area = response.json()
    except Exception as err:
        print(f"An error Occured as {err}.Please Try Again")


    lat = area["lat"]
    lon = area["lon"]

    #Weather API gives json file containing multiple day forcast
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=<your_api_key>"
    api_key = "<your_api_key>"

    # Define your authorization headers
    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }

    response = requests.get(url, headers=headers)
    weather = response.json()

    #Variables
    feels = weather["list"][0]["main"]["feels_like"]
    tempmax = weather["list"][0]["main"]["temp_max"]
    tempmin = weather["list"][0]["main"]["temp_min"]
    date = weather["list"][0]["dt_txt"]
    temp = weather["list"][0]["main"]["temp"]
    condition = weather["list"][0]["weather"][0]["description"]

    #Design and Code to display weather according to pincode 
    print("======================================")
    print("||          WEATHER REPORT          ||")
    print("======================================\n")

    print(f" 📍 Location :- {area["name"]}\n 🕒 Date & Time :-{mon(weather["list"][0]["dt_txt"])} "+date[11:16])
    print("\n------------CURRENT WEATHER-----------\n")
    print(f" ☀️  Condition :- {condition.title()}\n 🌡️  Temperature :- {f"{round(temp-273.0,1)}"+"°C"}\n 🤔 Feels Like :- {f"{round(feels-273.0,1)}"+"°C"}\n")
    print(f" 🌡️  MAX Temperature :- {f"{round(tempmax-273.0,1)}"+"°C"}\n 🌡️  MIN Temperature :- {f"{round(tempmin-273.0,1)}"+"°C"}\n")
    print(f" 💧 Humidity :- {f"{weather["list"][0]["main"]["humidity"]}"+" %"}\n 📊 Pressure :- {f"{weather["list"][0]["main"]["pressure"]}"+" hPa"}\n")
    print(f" ☁️  Cloud Cover :- {f"{weather["list"][0]["clouds"]["all"]}"+" %"}\n 👁 Visibility :- {f"{weather["list"][0]["visibility"]}"+" m"}\n")
    print(f" 🌬  Wind Speed :- {f"{weather["list"][0]["wind"]["speed"]}"+" m/s"}\n 🧭 Wind Direction :- {f"{weather["list"][0]["wind"]["deg"]}"+" °"}\n 💨 Wind Gust :- {f"{weather["list"][0]["wind"]["gust"]}"+" m/s"}\n")
    print("-----------5 DAY FORECAST-------------\n")
    print("______________________________________")
    print("    Date    |   Temp   |  Condition   ")
    print("--------------------------------------")
    for item in weather["list"]:
            if "12:00:00" in item["dt_txt"]:
                print(f"  {mon(item["dt_txt"])}      {round(int(item["main"]["temp"])-273.15,1)}         {item["weather"][0]["main"]}")    

        
    print("======================================\n   Data provided by OpenWeatherMap    \n======================================")
except Exception as error:
    print("If the error occured says \"lat\" or \"lon\", then the Pincode/Postal Code you entered was incorrect. Please check and try again.")
    print(f"An error occured as {error}. Please try again.")    