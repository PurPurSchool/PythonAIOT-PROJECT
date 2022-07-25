import pickle
import os
import base64
import googleapiclient.discovery
import time

from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer
from hal import hal_rfid_reader as rfid
from hal import hal_servo as servo

from picamera import PiCamera

from threading import Thread

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def opendoorifreplytrue(reply):
    if (reply == True):
        lcd = LCD.lcd()
        lcd.lcd_clear()

        lcd.lcd_display_string("The will now open...", 1)
        servo.set_servo_position(100)
        time.sleep(10)

        lcd.lcd_clear()
        lcd.lcd_display_string("The door is now closed.", 1)

        servo.set_servo_position(0)


def checkforreply(service, message):
    elapsed_time = 0
    test = 0

    while(test != 2 and elapsed_time < 20):
        threads = service.users().threads().get(userId='me', id=message['id']).execute()
        test = len(threads['messages'])
        time.sleep(1)
        elapsed_time = elapsed_time + 1
        print(elapsed_time)

    if(test == 2):
        print("TRUE")
        return True
    else:
        print("FALSE")
        return False


def sendPicture():
    # Get the path to the pickle file
    home_dir = os.path.expanduser('~')
    pickle_path = os.path.join(os.getcwd(), 'gmail.pickle')

    # Load our pickled credentials
    creds = pickle.load(open(pickle_path, 'rb'))

    # Build the service
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

    # replace with
    strFrom = 'aarontlm12345@gmail.com'
    strTo = 'aarontlm12345@gmail.com'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Picture from smart doorbell'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # Image goes into this snippet. Open the image you want to send.
    fp = open('image.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    raw = base64.urlsafe_b64encode(msgRoot.as_bytes())
    raw = raw.decode()

    body = {'raw': raw}

    message1 = body
    message = (
        service.users().messages().send(
            userId="me", body=message1).execute())
    print('Message Id: %s' % message['id'])

    reply = checkforreply(service, message)
    opendoorifreplytrue(reply)


def takeapicfunctioncamera():
    filedirectory = os.getcwd() + "/image.png"
    print(filedirectory)

    camera = PiCamera()
    time.sleep(1)
    camera.start_preview()
    time.sleep(3)
    camera.capture(filedirectory)
    camera.stop_preview()
    camera.close()
    time.sleep(2)
    sendPicture()
    lcd = LCD.lcd()
    lcd.lcd_display_string("Please ring", 1)
    lcd.lcd_display_string("the bell", 2)


def takeapicfunction():
    time.sleep(2)
    sendPicture()
    lcd = LCD.lcd()
    lcd.lcd_display_string("Please ring", 1)
    lcd.lcd_display_string("the bell", 2)


def whilefunction():
    while(True):
        time.sleep(0.2)
        keypress = keypad.get_key()
        if keypress:
            lcd = LCD.lcd()
            lcd.lcd_clear()
            lcd.lcd_display_string("Please wait...", 1)
            #buzzer.short_beep(2)
            takeapicfunction()
            time.sleep(5)

def checknfc():
    code = 246239183187
    while (True):
        id, text = rfid.SimpleMFRC522().read()
        print(id)
        print(text)
        time.sleep(1)
        if (id == code):
            opendoorifreplytrue(True)


def main():
    thread1 = Thread(target = whilefunction)
    thread2 = Thread(target = checknfc)

    keypad.init()
    buzzer.init()
    rfid.init()
    servo.init()

    lcd = LCD.lcd()
    lcd.lcd_clear()

    lcd.lcd_display_string("Please ring", 1)
    lcd.lcd_display_string("the bell", 2)

    thread1.start()
    thread2.start()

if __name__ == '__main__':
    main()