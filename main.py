import time
import mss
import numpy as np
import cv2
from pykeyboard import PyKeyboard
import threading
import sys
import os


def edge_trace(orig):
    normalized=np.zeros((600,800))
    gray=np.zeros((600,800))
    normalized=cv2.normalize(orig,normalized,1,255,cv2.NORM_MINMAX)
    gray=cv2.cvtColor(normalized,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('norm',cv2.Canny(normalized, threshold1=300, threshold2=50))
    cv2.imshow('gray',cv2.Canny(gray, threshold1=300, threshold2=50))
    return cv2.Canny(gray, threshold1=300, threshold2=50)


holding = {}


def release_key(keyboard, key):
    holding[key] = False
    keyboard.release_key(key)


def hold_key(keyboard, key, hold_secs, release_secs=0, regulating=False):
    if key in holding.keys() and holding[key] is True:
        return
    holding[key] = True
    print("HOLD KEY!")
    if not regulating:
        keyboard.press_key(key)
        time.sleep(hold_secs)
        release_key(keyboard, key)
    else:
        while key in holding.keys() and holding[key]:
            keyboard.press_key(key)
            time.sleep(hold_secs)
            keyboard.release_key(key)
            time.sleep(release_secs)


def release_all_keys(keyboard):
    for key in holding.keys():
        release_key(keyboard, key)
    holding.clear()


def show_fb():
    sct = mss.mss()
    pyk = PyKeyboard()
    while 1:
        monitor = {'top': 100, 'left': 100, 'width': 800, 'height': 600}
        img = sct.grab(monitor)
        img_np = np.array(img)
        frame = cv2.resize(
            img_np,
            (int(img_np.shape[1]), int(img_np.shape[0])),
        )
        cv2.imshow("FrameBuffer", edge_trace(frame))
        ip_key = cv2.waitKey(1)
        if ip_key == 27 or ip_key == 113:
            break
        if ip_key == 97:
            thread = threading.Thread(target=hold_key, args=(pyk, 'a', 0.5, 1.5, True))
            thread.start()
        if ip_key == 114:
            release_all_keys(pyk)

    cv2.destroyAllWindows()

def test_fb(argv):
    # sct = mss.mss()
    pyk = PyKeyboard()
    for image in argv:
        # monitor = {'top': 100, 'left': 100, 'width': 800, 'height': 600}
        img = cv2.imread(image)
        img_np = np.array(img)
        frame = cv2.resize(
            img_np,
            (int(img_np.shape[1]), int(img_np.shape[0])),
        )
        final=edge_trace(frame)
        # cv2.imshow("FrameBuffer", final)
        ip_key = cv2.waitKey(1)
        if ip_key == 27 or ip_key == 113:
            break
        if ip_key == 97:
            thread = threading.Thread(target=hold_key, args=(pyk, 'a', 0.5, 1.5, True))
            thread.start()
        if ip_key == 114:
            release_all_keys(pyk)
        image=image.replace("./img/","")
        # print(os.path.join("./edge/edge_",image))
        cv2.imwrite("./edge/"+image,final)

    cv2.destroyAllWindows()
    print("done")


def main():
    # print(sys.argv)
    print(len(sys.argv))
    # list=[]
    if(len(sys.argv)==1):
        show_fb()
    else:
        test_fb(sys.argv[1:])


if __name__ == '__main__':
    main()

#sudo systemctl disable gdm