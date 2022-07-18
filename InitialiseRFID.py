from hal import hal_rfid_reader as rfid

def main():
    rfid.init()
    text = input('New data:')
    print("Now place your tag to write")
    rfid.SimpleMFRC522().write(text)
    print("Written")

if __name__ == '__main__':
    main()