import json
from urllib.parse import quote_plus

import kivy
from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

kivy.require("1.11.1")


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    id_rv = ObjectProperty()

    def search_location(self):
        """
        Search for the given location through all available locations in OpenWeather.
        """
        # The URL's base.
        base_url = "http://api.openweathermap.org/data/2.5/find?q="
        # The place to search.
        place_to_search = f"{self.search_input.text}"
        # My API key.
        api_key = "&type=like&APPID=7b6e61038914b2c13915adcb9087ce7d"
        # The above variables together to make the complete search request.
        search_url = base_url + quote_plus(place_to_search) + api_key
        print(search_url)
        # Make the request to OpenWeatherMap
        self.request = UrlRequest(search_url, self.found_location)
        print(
            f"## search_location (type: {type(self.request)}\t data: {self.request.result}"
        )

    def found_location(self, request, data, *args):
        """
        Add the given location by the user to list view.


        Args:
            request (UrlRequest): Object request.
            data (list): List with requested data.
        """
        # If the data is type dict there's no to do decode, else will decode
        # the data.
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        # Save each matched option.
        cities = [f"{i['name']} ({i['sys']['country']})" for i in data["list"]]
        # Show the saved options.
        self.id_rv.data = [{"text": item} for item in cities]


class WeatherApp(App):
    def build(self):
        return AddLocationForm()


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
