# Banggood Cash Collection bot
This simple python code utlizes Selenium to collect cash in Banggood's virtual cash game.
please install the requirement packages using pip install.

## How to use:
First clone the repository, and then install the required dependencies using:
```
pip install -r requirements.txt
```

Create a `.env` file inside your folder and insert the following variables (update them with the relevant info):

```
API_USERNAME=your_username
API_PASSWORD=your_password
CHROME_PATH=path-to-your-chrome-web-driver
```

## Update:
- The bot can now do the dailies and will check after every deposit if dailies need to be done/finished.
- Activting the script requires a "continue affirmation" after login, simply press y when requested (please ensure you are logged in).

