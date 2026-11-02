# Weather Meteo

A lightweight Python 3 and Tkinter weather application.

**Developer:** Hamdy Abou El Anein
**Contact:** info@daylightlinux.ch
**License:** GNU GPL v3 (see LICENSE).

## Features

- Tkinter desktop interface replacing EasyGUI.
- HTTPS access to wttr.in using only the Python standard library.
- Temperature, apparent temperature, humidity and wind.
- Asynchronous refresh, input validation and network timeouts.
- Text-only CLI mode.

## Run

    python3 meteo.py
    python3 meteo.py --text --city Bern

## Tests

    python3 -m unittest discover -s tests -v

Forecast availability depends on the external wttr.in service.
The original code is preserved on the [old branch](https://github.com/hamdyaea/WeatherMeteo/tree/old).
