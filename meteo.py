#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-or-later
"""Weather forecasts in a lightweight Tkinter application."""
import argparse
import json
import threading
import tkinter as tk
from tkinter import ttk
from urllib.parse import quote
from urllib.request import Request, urlopen

LANGUAGES = {"English": "en", "French": "fr", "German": "de", "Italian": "it"}


def weather_url(city, language="en"):
    if not city.strip() or len(city) > 100 or any(ord(c) < 32 for c in city):
        raise ValueError("Enter a valid location")
    if language not in LANGUAGES.values():
        raise ValueError("Unsupported language")
    return "https://wttr.in/" + quote(city.strip(), safe="") + "?format=j1&lang=" + language


def parse_weather(data):
    try:
        current = data["current_condition"][0]
        return {
            "temperature": str(current["temp_C"]),
            "description": str(current["weatherDesc"][0]["value"]),
            "feels": str(current["FeelsLikeC"]),
            "humidity": str(current["humidity"]),
            "wind": str(current["windspeedKmph"]),
        }
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Unexpected weather response") from exc


def fetch_weather(city, language="en"):
    request = Request(weather_url(city, language), headers={"User-Agent": "WeatherMeteo/2.0"})
    with urlopen(request, timeout=18) as response:
        data = response.read(300000)
    return parse_weather(json.loads(data.decode("utf-8")))


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Meteo — Hamdy Abou El Anein")
        self.geometry("530x420")
        self.minsize(410, 330)
        self.configure(bg="#101827")
        self.city = tk.StringVar(value="Bern")
        self.language = tk.StringVar(value="English")
        self.status = tk.StringVar(value="Enter a location and refresh.")
        self.forecast = tk.StringVar(value="—")
        box = tk.Frame(self, bg="#101827", padx=24, pady=22)
        box.pack(fill="both", expand=True)
        tk.Label(box, text="WEATHER METEO", font=("DejaVu Sans", 16, "bold"),
                 bg="#101827", fg="#8bd6c1").pack(anchor="w")
        tk.Label(box, text="Location", bg="#101827", fg="white").pack(anchor="w", pady=(14, 3))
        tk.Entry(box, textvariable=self.city).pack(fill="x")
        ttk.Combobox(box, textvariable=self.language, state="readonly",
                     values=list(LANGUAGES)).pack(fill="x", pady=14)
        tk.Label(box, textvariable=self.forecast, bg="#101827", fg="#f2c879",
                 font=("DejaVu Sans", 15, "bold"), justify="left",
                 wraplength=470).pack(anchor="w", pady=22)
        self.button = tk.Button(box, text="Refresh", command=self.refresh,
                                bg="#7ddcc0", fg="#10211c", relief="flat", padx=20, pady=9)
        self.button.pack(anchor="w")
        tk.Label(box, textvariable=self.status, bg="#101827",
                 fg="#c5d5e5", wraplength=470).pack(anchor="w", pady=12)

    def refresh(self):
        city, language = self.city.get(), LANGUAGES[self.language.get()]
        try:
            weather_url(city, language)
        except ValueError as exc:
            self.status.set(str(exc))
            return
        self.button.config(state="disabled")
        self.status.set("Loading weather…")

        def worker():
            try:
                report, error = fetch_weather(city, language), None
            except (OSError, ValueError) as exc:
                report, error = None, str(exc)

            def display():
                self.button.config(state="normal")
                if error:
                    self.status.set("Weather unavailable: " + error)
                else:
                    self.forecast.set(
                        report["temperature"] + " °C · " + report["description"] + "\n"
                        + "Feels like " + report["feels"] + " °C · Humidity "
                        + report["humidity"] + "%\nWind " + report["wind"] + " km/h"
                    )
                    self.status.set("Data: wttr.in")
            try:
                self.after(0, display)
            except RuntimeError:
                pass
        threading.Thread(target=worker, daemon=True).start()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", default="Bern")
    parser.add_argument("--language", default="en", choices=LANGUAGES.values())
    parser.add_argument("--text", action="store_true")
    args = parser.parse_args()
    if args.text:
        try:
            report = fetch_weather(args.city, args.language)
        except (OSError, ValueError) as exc:
            parser.exit(1, "Weather unavailable: " + str(exc) + "\n")
        print(args.city + ": " + report["temperature"] + " °C, " + report["description"])
    else:
        WeatherApp().mainloop()


if __name__ == "__main__":
    main()
