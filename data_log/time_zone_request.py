import requests
from datetime import datetime

# Fetch the current time from an internet time API
response = requests.get('http://worldtimeapi.org/api/ip')
data = response.json()

# Extract the current time from the API response
current_time = data['datetime']

# Convert the time string to a datetime object
time_object = datetime.fromisoformat(current_time)

# Extract specific components from the time object
hour = time_object.hour
minute = time_object.minute
second = time_object.second

# Print the current time
print(f"Current time is: {hour}:{minute}:{second}")