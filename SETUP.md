# Coin Watch

## Setup

### Requirements

- Raspberry Pi 4 (Recommended) with SD Card
- Breadboard
- LED(s) and required resistors
- Pushdown Button
- Jumper Wires
- Alexa Developer Console Account
- Twilio Developer Console Account

### Softwares I Used

1. Balena Etcher
2. Visual Studio Code
3. PuTTy
4. Notepad++

### Raspberry Pi

1. Download Raspberry Pi OS from this [link](https://www.raspberrypi.com/software/operating-systems/).
2. Flash the image to the SD Card you plan on using with the Pi. Recommended too is Balena Etcher.
3. Connect the SD Card to your computer again and follow these steps to connect the Pi to your WiFi. Use Notepad++ to protect the filetype.
  - In the root folder of the SD Card, create a file named `wpa_supplicant.conf` and add the following lines of code to it:
    ``` bash
    country=us
    update_config=1
    ctrl_interface=/var/run/wpa_supplicant

    network={
    scan_ssid=1
    ssid="SSID"
    psk="Password"
    }
  - Create another file named `ssh` without any extensions. These will help us connect with the Raspberry Pi using PuTTY and an Ethernet Cable. Again, use Notepad++ for this.
4. Take the SD Card and insert it in the slot given in Raspberry Pi. Connect the Ethernet Cable to both the Pi and the Computer and then connect the Pi to power supply.
5. Open PuTTY and connect using `raspberrypi.local` or the IP Address of the Pi if you're able to fetch it from your router and add it in the "Host Name" field.
6. Login using `pi` as the username and `raspberry` as the password. You can change these later.
7. Run the following set of commands to install and upgrade the libraries required for this project:
  ``` bash
  sudo apt-get upgrade
  python3 -m pip install Flask-Ask
  pip3 install --upgrade setuptools
  pip3 install 'cryptography<2.2'
  pip install twilio
  pip install pyserial
  pip install RPi.GPIO
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
  unzip ngrok-stable-linux-arm.zip
  ```
8. Create a file `rpi-alexa.py` and copy the code from the repository. [Raspberry Pi Code](rpi-alexa.py)
9. Please change the Twilio Credentials in the file. You can get yours from the Twilio Console.
10. Execute the script by using `python3 rpi-alexa.pi` and you should be able to run the script in Debugging Mode.
11. Open another terminal and execute `./ngrok http 5000` to open your local server port to the internet.
12. Copy the second URL from the console (HTTPS) to use it as an endpoint for our Alexa Skill.

### Alexa Skill

1. Head over to https://developer.amazon.com/alexa/console/ask and login if you haven't done so already.
2. Click on Create Skill.
3. Enter the skill name of your liking and choose a locale that suits you best.
4. For the prompt "Choose a model to add to your skill", select `Custom`.
5. For "Choose a method to host your skill's backend resources", select `Provision your own`. Again click on Create Skill.
6. For "Choose a template to add to your skill", click on `Start from Scratch` and then click on Choose.
7. In the window that now opens, select `Interaction model` and then click on `JSON Editor`.
8. Past the content from [alexa-skill.json](alexa-skill.json) in the Editor and the Intents with their Utterances will be populated automatically. Click on `Save Model`.
9. Now scroll down and find `Endpoint`. Select `HTTPS` instead of AWS Lambda ARN here.
10. Enter the URI we copied from the Ngrok Console in the input box and then select "My development endpoint is a sub-domain of a domain that has a wild card certificate..." and then click on Save Endpoints.
11. Now you can build the model and test the whole thing by clicking on `Test` in the Navigation Bar.
12. Enter the utterances to call specific Intents and you're all set.