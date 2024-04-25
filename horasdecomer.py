from datetime import datetime, timedelta
import ephem, pgeocode, pytz, timezonefinder



def find3rdAnd9thDaylightHours(sunrise, sunset):
    dt_rise = datetime.strptime(sunrise, "%H:%M")
    dt_set = datetime.strptime(sunset, "%H:%M")

    true_hour = (dt_set - dt_rise) / 12

    hour3 = (dt_rise + 2 * true_hour).strftime("%H:%M")
    hour9 = (dt_rise + 8 * true_hour).strftime("%H:%M")

    return [hour3, hour9]

#return a the sunrise and sunset times for a given location in its respective timezone
def get_sunrise_sunset(lat, lon, date):
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = date

    sunrise = observer.next_rising(ephem.Sun())
    sunset = observer.next_setting(ephem.Sun())

    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    timezone = pytz.timezone(timezone_str)
    dt = datetime.now()

    return sunrise.datetime() + timezone.utcoffset(dt), sunset.datetime() + timezone.utcoffset(dt)

response1 = input("Are you in the united states? (y/n): ").lower()

if response1[0] == "y":
    zip_code = input("Enter your zip code: ")
    nomi = pgeocode.Nominatim("us")
    location = nomi.query_postal_code(zip_code)

    lat = location["latitude"]
    lon = location["longitude"]
else:
    lat = float(input("Please enter your latitude: "))
    lon = float(input("Please enter your longitude: "))

qty = input("Would you like to calculate for a single date or a range of dates? (s/r): ")
if qty[0] == "r":
    start_date = input("Enter start date (YYYY/MM/DD): ")
    end_date = input("Enter end date (YYYY/MM/DD): ")

    startd = datetime.strptime(start_date, "%Y/%m/%d")
    endd = datetime.strptime(end_date, "%Y/%m/%d")

    for i in range((endd-startd).days + 1):
        day = startd + timedelta(days = i)
        sunrise_dt, sunset_dt = get_sunrise_sunset(lat, lon, day)

        sunrise_time = sunrise_dt.strftime("%H:%M")
        sunset_time = sunset_dt.strftime("%H:%M")

        hour3, hour9 = find3rdAnd9thDaylightHours(sunrise_time, sunset_time)

        print("date = %s sunrise = %s sunset = %s" % (day, sunrise_time, sunset_time))
        print("3rd daylight hour = %s 9th daylight hour = %s" % (hour3, hour9))
    print("peace be upon you")

else:
    date = input("Enter a single date (YYYY/MM/DD): ")
    sunrise_dt, sunset_dt = get_sunrise_sunset(lat, lon, date)

    sunrise_time = sunrise_dt.strftime("%H:%M")
    sunset_time = sunset_dt.strftime("%H:%M")

    hour3, hour9 = find3rdAnd9thDaylightHours(sunrise_time, sunset_time)

    print("date = %s sunrise = %s sunset = %s" % (date, sunrise_time, sunset_time))
    print("3rd daylight hour = %s 9th daylight hour = %s" % (hour3, hour9))
    print("peace be upon you")


