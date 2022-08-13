import pickle
import os
from hal import hal_rfid_reader as rfid

pickle_path = os.path.join(os.getcwd(), 'RFID_ID.pickle')


def write_Emptylist():
    empty_list = []

    with open(pickle_path, 'wb') as write_ids:
        pickle.dump(empty_list, write_ids)

    print("Pickle file successfully created. Please re-run the program.")


def readRFID_sendtoPICKLE():
    with open(pickle_path, 'rb') as read_ids:
         current_ids = pickle.load(read_ids)

    print("Please place the RFID tag on the RFID reader")
    id, text = rfid.SimpleMFRC522().read()

    current_ids.append(id)

    with open(pickle_path, 'wb') as write_ids:
        pickle.dump(current_ids, write_ids)

    with open(pickle_path, 'rb') as read_ids:
        current_ids = pickle.load(read_ids)

    print("CURRENT IDS ARE: ")
    print(current_ids)


def main():
    rfid.init()

    isFile = os.path.isfile(pickle_path)

    if isFile == True:
        readRFID_sendtoPICKLE()
    else:
        write_Emptylist()


if __name__ == '__main__':
    main()
