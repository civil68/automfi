# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# -*- coding: utf-8 -*-
import cv2
from pyzbar import pyzbar
from pylibdmtx import pylibdmtx
# import winsound

found_QR = set()
found_DMX = set()


'''
def beep(frequency, amplitude, duration):
    sample = 8000
    half_period = int(sample/frequency/2)
    beep = chr(amplitude)*half_period+chr(0)*half_period
    beep *= int(duration*frequency)
    audio = open('/dev/snd/pcmC0DOp', 'wb')
    audio.write(beep)
    audio.close()
'''


def read_usb_capture(cam1, cam2):
    #cap = cv2.VideoCapture(camno, cv2.CAP_DSHOW)
    cap1 = cv2.VideoCapture(cam1, cv2.CAP_V4L2)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap1.set(cv2.CAP_PROP_EXPOSURE, 200)
    cap2 = cv2.VideoCapture(cam2, cv2.CAP_V4L2)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cv2.waitKey(100)
    cv2.namedWindow('QR-Code', cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
    #cv2.namedWindow('QR-Code')
    cv2.moveWindow('QR-Code',100,64)
    cv2.namedWindow('DataMetrix', cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
    cv2.moveWindow('DataMetrix',356,64)
    while cap1.isOpened() & cap2.isOpened():
        ret, frame1 = cap1.read()
        if ret:
            # img = cv2.cvtColor(frame[192:448, 112:368], cv2.COLOR_BGR2GRAY)
            img_QR = frame1[192:448, 112:368]
            #img_QR = frame1
            cv2.imshow('QR-Code', img_QR)

            #qrc = pyzbar.decode(img_QR, symbols=[pyzbar.ZBarSymbol.QRCODE])
            qrc = pyzbar.decode(img_QR)
            for tests in qrc:
                testdata = tests.data.decode('utf-8')
                testtype = tests.type
                (x,y,w,h) = tests.rect
                cv2.rectangle(img_QR,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.imshow('QR-Code', img_QR)
                # printout = "{} ({})".format(testdata, testtype)

                if testdata not in found_QR:
                    # winsound.Beep(3000, 100)
                    print("[INFO] 找到 {} 二維碼: {}".format(testtype, testdata))
                    # print(printout)
                    found_QR.clear()
                    found_QR.add(testdata)
                    # beep(3000, 5, 100)
                    print('\a')

        ret, frame2 = cap2.read()
        if ret:
            img_DMX = frame2[192:448, 112:368]
            cv2.imshow('DataMetrix', img_DMX)

            dmtx = pylibdmtx.decode(img_DMX, timeout=20, max_count=1)
            for tests in dmtx:
                testdata = tests.data.decode('utf-8')
                (x,y,w,h) = tests.rect
                cv2.rectangle(img_DMX,(x,256-y),(x+w,256-y-h),(0,0,255),2)
                cv2.imshow('DataMetrix', img_DMX)
                if testdata not in found_DMX:
                    # winsound.Beep(4000, 100)
                    # print("[INFO] 找到 DataMatrix 二維碼: {}".format(testdata))
                    print("[INFO] 找到 DataMatrix 二維碼: {}".format(testdata))
                    found_DMX.clear()
                    found_DMX.add(testdata)
                    # beep(4000, 5, 100)
                    print('\a')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放畫面
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_usb_capture(0, 2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/