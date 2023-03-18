from django.shortcuts import render
import requests, json
from bs4 import BeautifulSoup as bs

def get_weather_data(city):
    city = city.replace('  '," ").replace(' ','+').replace('++','+').strip()
    url = f'https://www.google.com/search?q=weather+of+{city}'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    LANGUAGE = 'en-US,en;q=0.9'

    session = requests.Session()
    session.headers['user-agent'] = USER_AGENT
    session.headers['accept-language'] = LANGUAGE
    response = session.get(url)
    soup = bs(response.text, 'html.parser')

    #Extract data
    result = {}
    result['region'] = soup.find('span', attrs={'class':'BBwThe'}).text
    result['daytime'] = soup.find('div', attrs={'id':'wob_dts'}).text
    result['weather'] = soup.find('span', attrs={'id':'wob_dc'}).text
    result['temp'] = soup.find('span', attrs={'id':'wob_tm'}).text
    return result


get_weather_data("dhaka")

# Create your views here.
def home_view(request):
    if request.method == "GET" and 'city' in request.GET:
        city = request.GET.get('city')
        results = get_weather_data(city)

        context = {'results':results}
    else:
        context = {}
    return render(request, 'weather/home.html',context)

#function for api weather
def weather_api(city):
    api_key = 'c837f131c7a003f52f364aa42d40560d'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)
    results = {}
    results['weather'] = data['weather'][0]['main']
    results['description'] = data['weather'][0]['description']
    results['temp'] = data['main']['temp']
    results['temp_min'] = data['main']['temp_min']
    results['temp_max'] = data['main']['temp_max']
    return results

#weather_api view
def api_view(request):
    if request.method == "POST" and 'city' in request.POST:
        city = request.POST.get('city')
        results = weather_api(city)
        context = {'results':results}
        return render(request, 'weather/api.html', context)