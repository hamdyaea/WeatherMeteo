# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-or-later
import importlib.util
from pathlib import Path
from unittest import TestCase

spec = importlib.util.spec_from_file_location("app", Path(__file__).resolve().parents[1] / "meteo.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class Tests(TestCase):
    def test_url(self):
        self.assertIn("Saint%20Sylvester", app.weather_url("Saint Sylvester"))
        with self.assertRaises(ValueError):
            app.weather_url("")
    def test_parse(self):
        data = {"current_condition": [{"temp_C": "20", "FeelsLikeC": "21",
                "humidity": "40", "windspeedKmph": "5",
                "weatherDesc": [{"value": "Sunny"}]}]}
        self.assertEqual(app.parse_weather(data)["temperature"], "20")
        with self.assertRaises(ValueError):
            app.parse_weather({})
    def test_window(self):
        window = app.WeatherApp()
        try:
            self.assertEqual(window.city.get(), "Bern")
        finally:
            window.destroy()
