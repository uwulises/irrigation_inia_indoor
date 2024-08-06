from datetime import datetime
# Funcion para obtener fecha y hora segun ubicacion geografica
import json

def call_datetime():

    #get the local time from raspberry pi
    data = {'datetime': datetime.now().isoformat()}
    
    # Extract the current time from the API response
    current_time = data['datetime']
    AAAA_MM_DD = data['datetime'][:10]
    
    # Convert the time string to a datetime object
    time_object = datetime.fromisoformat(current_time)

    # Extract specific components from the time object
    hour = time_object.hour
    minute = time_object.minute
    second = time_object.second
    print("Fecha: ", AAAA_MM_DD, "Hora: ", hour, ":", minute)

    return current_time, AAAA_MM_DD,"T{}:{}:{}".format(hour, minute, second), hour, minute, second


def check_log_time_variable(previous_datetime):
    current_datetime = call_datetime()[0]
    # Convert the time string to a datetime object
    current_datetime = datetime.fromisoformat(current_datetime)
    previous_datetime = datetime.fromisoformat(previous_datetime)
    # Calculate the time difference in minutes
    time_diff = (current_datetime - previous_datetime).total_seconds() / 60

    if time_diff >= 10:
        # Toggle the boolean variable
        print("Han pasado 10min desde el ultimo registro de datos")
        return True
    
    return False

def check_irrigation_time():
    current_datetime = call_datetime()[0]
    current_datetime = datetime.fromisoformat(current_datetime)

    with open('data_log/irrigation_time.json', 'r') as file:
        data = json.load(file)
    
    # Extract the day and time from the data
    irrigation_days = data["dias_riego"]
    irrigation_times = data["hora_riego"]
    
    # Check if the current day is in the irrigation days
    current_day = current_datetime.strftime('%A')
    if current_day in irrigation_days:
        # Iterate over the irrigation times to check if any match within 10 minutes
        for irrigation_time in irrigation_times:
            irrigation_datetime = datetime.strptime(irrigation_time, '%H:%M').replace(
                year=current_datetime.year, 
                month=current_datetime.month, 
                day=current_datetime.day
            )
            
            # Check if the current time is within 10 minutes of the irrigation time
            time_difference = abs((current_datetime - irrigation_datetime).total_seconds())
            if time_difference <= 600:  # 600 seconds = 10 minutes
                return True
    
    return False