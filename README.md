# Banggood Cash Collection bot :moneybag:
This simple python code utlizes Selenium to collect cash in Banggood's virtual cash game :money_mouth_face:.
please install the requirement packages using pip install before trying to run the script.

## How to use :green_book: :
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
<b>Note that the script is based on chrome web driver!</b>

## Update:
- The bot can now do the "15 seconds browsing" and "random product" dailies and will check after every deposit if dailies needs to be done/finished.
- Activting the script requires a "continue affirmation" after login, simply press `y` when requested (please ensure you are logged in), this was added due to Banggood's bot protection.

### Please consider staring the repository!
If you're using my project, please consider :star: the project