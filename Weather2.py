def weather_func(city):
    import requests
    from googletrans import Translator
    translator = Translator()
    apiKey = "51903e101ea0a726d4cc028d31a348e5"
    s_city = city
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': apiKey})
        data = res.json()
        if data['list'] != []:
            #cities = ["{} ({})".format(d['name'], d['sys']['country'])
                        #for d in data['list']]
            #print("city:", cities)
            city_id = data['list'][0]['id']
            #print('city_id=', city_id)
        else:
            s_city = translator.translate(text=s_city, dest='en', src='ru')
            s_city = s_city.text
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': apiKey})
            data = res.json()
            #cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      #for d in data['list']]
            # print("city:", cities)
            city_id = data['list'][0]['id']
            # print('city_id=', city_id)

    except Exception as e:
        pass
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': apiKey})
        data = res.json()

        description = data['weather'][0]['description']

        pic_url = 'http://openweathermap.org/img/w/' + data['weather'][0]['icon']+ '.png'

        description = description.capitalize()

        temp = data["main"]["temp"]

        humidity = data["main"]["humidity"]

        wind = data["wind"]
        wind_speed = wind["speed"]
        wind_deg = wind["deg"]

        if wind_deg < 23:
            side = "Северное"
        elif wind_deg < 68:
            side = "Северо-восточное"
        elif wind_deg < 113:
            side = "Восточное"
        elif wind_deg < 158:
            side = "Юго-восточное"
        elif wind_deg < 203:
            side = "Южное"
        elif wind_deg < 248:
            side = "Юго-восточное"
        elif wind_deg < 293:
            side = "Западное"
        elif wind_deg < 338:
            side = "Северо-западное"
        else:
            side = "Северное"

        answer = description + '\n' + str(temp) + "°C " + '\n' + "Влажность воздуха" + " " + str(humidity) + "%" + '\n' + side + " направление ветра" + ", " + str(wind_speed) + " м\с"
        return answer, pic_url

    except Exception as e:
        return ["Указанный город не найден!", "Указанный город не найден!"]
        pass
