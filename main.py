import requests
import datetime as dt
import smtplib
import time

# USER DATA
MY_LAT = 
MY_lNG = 


def location_compare():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_lat = float(iss_data['iss_position']['latitude'])
    iss_lng = float(iss_data['iss_position']['longitude'])
    if (MY_LAT + 5 >= iss_lat >= MY_LAT - 5) and (MY_lNG + 5 >= iss_lng >= MY_lNG - 5):
        return True


def email_sender():
    USER = ''
    PASSWORD = ''

    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=USER,
                         password=PASSWORD
                         )
        connection.sendmail(
            from_addr=USER,
            to_addrs=USER,
            msg='subject:ISS IS OVERHEAD\n\nISS is your overhead go '
                'out and see!'
        )


def is_night_time():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_lNG,
        'formatted': 0
    }
    sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    sun_data = sun_response.json()
    sun_rise_time = int(sun_data['results']['sunrise'].split('T')[1].split(':')[0])
    sun_set_time = int(sun_data['results']['sunset'].split('T')[1].split(':')[0])

    time_now = dt.datetime.now()
    hour_now = time_now.hour
    if sun_set_time <= hour_now <= (sun_rise_time - 1):
        return True


while True:
    time.sleep(60)
    if is_night_time() and location_compare():
        email_sender()
