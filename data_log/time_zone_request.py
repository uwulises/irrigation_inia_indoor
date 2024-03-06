from datetime import datetime
# Funcion para obtener fecha y hora segun ubicacion geografica


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
