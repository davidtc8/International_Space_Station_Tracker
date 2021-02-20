import requests
from datetime import datetime
import random
import smtplib

# TODO: Remember that only you can see your password
###### Constants ########
my_email = "" # here you have to write the email
# Don't let anyone see your password!
password = "" # here you have to write the password of the email that is going to send the mssg
recipient = "" # here you have to write the email recipient

# TODO: Change your latitude and longitude to your current place
MY_LAT = 52.681872 # Your latitude
MY_LONG = -85.268882 # Your longitude

###### API INFORMATION ########
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

###### TESTING API RESULTS ########
print(f"the latitude is {iss_latitude}")
iss_almost_latitude = random.uniform(iss_latitude -5, iss_latitude + 5)
print(iss_almost_latitude)
print(f"the longitude is {iss_longitude}")
iss_almost_longitude = random.uniform(iss_longitude -5, iss_longitude + 5)
print(iss_almost_longitude)

###### FUNCTIONS TO DETECT IF IT'S NIGHTTIME AND THE ISS IS NEAR ME ########
def iss_is_close_to_me():
    """
    This function will let me know if the ISS is close to where I live
    """
    iss_is_close = None
    # Latitude +-5
    iss_latitude_plus_five = iss_latitude + 5
    iss_latitude_minus_five = iss_latitude - 5

    # Longitude +- 5
    iss_longitude_plus_five = iss_longitude + 5
    iss_longitude_minus_five = iss_longitude - 5

    # If the ISS is close to my current position
    if iss_latitude_minus_five <= MY_LAT <= iss_latitude_plus_five and iss_longitude_minus_five <= MY_LONG <= iss_longitude_plus_five:
        iss_is_close = True
    else:
        iss_is_close = False
    return iss_is_close

def is_night_time():
    """
    This function will let me know if the ISS is near me during night time
    """
    if time_now >= sunset or time_now <= sunrise:
        return True

# sunset
print(sunset)

###### Calling the functions ########
iss_close = iss_is_close_to_me()
is_night = is_night_time()

###### Sending me an email if the previous functions are True ########
#If the ISS is close to my current position
if iss_close is True and is_night is True:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # tls stands for transport layer security and is a way of securing our connection to our email server
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs= recipient,
                            msg="Subject: The International Space Station is near you!\n\nTake a look at the sky, you will have the chance to take a look at the space station\n\n Keep dreaming (:")
    #confirmation email
    print(f"I have sent you an email to {recipient}, go and take a look at it!")
else:
    print("The space station is nowhere near you")
