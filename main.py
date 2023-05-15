import requests
import matplotlib.pyplot as plt
from datetime import datetime
import datetime


api_key = 'AIzaSyDRGeAIriYPPo9zJDh7P5IVjd2y0_b3xnI'

location = input("Enter city you want, to know situation about traffic) ")

url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}'


response = requests.get(url)
json_response = response.json()
location_data = json_response['results'][0]['geometry']['location']
lat = location_data['lat']
lng = location_data['lng']


current_time = datetime.datetime.now()
timestamp = int(current_time.timestamp())
date = datetime.datetime.fromtimestamp(timestamp)
categories=[]
values = []

for i in range(5):
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat},{lng}&destinations={lat},{lng}&departure_time={timestamp}&traffic_model=pessimistic&key={api_key}'
    date = date + datetime.timedelta(days=1)
    timestamp = int(date.timestamp())
    response = requests.get(url)
    json_response = response.json()
    traffic_data = json_response['rows'][0]['elements'][0]['duration_in_traffic']
    values.append(traffic_data['value'])
    categories.append(date.strftime('%Y-%m-%d'))


with plt.style.context('Solarize_Light2'):
    a = [categories[0], categories[1], categories[2], categories[3], categories[4]]
    b = [values[0], values[1], values[2], values[3], values[4]]
    fig, ax = plt.subplots()

    ax.bar(a, b, color='pink', edgecolor='black') 

    ax.set_xlabel('Data time', fontsize=12)
    ax.set_ylabel('Values', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.text(0.5, 1.1, f'Traffic in {location}', ha='center', va='center', transform=plt.gca().transAxes, color="black", fontsize=12, fontweight='bold')

    if sum(values) > 0:
        ax.text(0.5, 1.04, 'Traffic is in bad condition', ha='center', va='center', transform=plt.gca().transAxes, fontsize=9, color="black")
    else:
        ax.text(0.5, 1.04, 'Traffic is clear', ha='center', va='center', fontsize=9, color="black")

    ax.grid(axis='y', linestyle='--', alpha=0.7) 

    fig.tight_layout()

plt.show()
