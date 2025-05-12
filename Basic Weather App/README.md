Weather App
A simple command-line Python application that fetches and displays current weather data for a user-specified city using the OpenWeatherMap API. The app shows temperature (in Celsius), humidity, and weather conditions.

Features
Fetches real-time weather data for any city.
Displays temperature, humidity, and weather description.
Handles errors for invalid city names or network issues.
Easy-to-use command-line interface.

Prerequisites
Python 3.6 or higher installed
Visual Studio Code (VS Code) with the Python extension installed
An active internet connection
OpenWeatherMap API key (already embedded in the code)

Setup

1.Download the Project:
Save the project files (weather_app.py, README.md, requirements.txt) to a folder on your computer.

2.Open in VS Code:
Launch VS Code.
Go to File > Open Folder and select the project folder containing the files.

3.Install Dependencies:
Ensure the Python extension is installed in VS Code (available in the Extensions view: Ctrl+Shift+X).
Open requirements.txt in VS Code.
If prompted by VS Code, click "Install" to add the requests library, or use the Python extension's dependency installation feature.
Alternatively, ensure the requests library is available in your Python environment.

4.Verify API Key:
The weather_app.py file includes an OpenWeatherMap API key. If you need to use a different key, sign up at OpenWeatherMap, obtain a free API key, and replace the api_key value in weather_app.py.

Running the App

Open weather_app.py in VS Code.
Click the "Run Python File" button (a play icon) in the top-right corner of the editor.
A terminal window will appear in VS Code with the app running.
Follow the prompts:
Enter a city name (e.g., "London") to see the weather.
Type "quit" to exit the app.