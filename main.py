import time
import mss
import numpy as np
import cv2
from pykeyboard import PyKeyboard
import threading


def edge_trace(orig):
    return cv2.Canny(cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY), threshold1=400, threshold2=300)


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
        monitor = {'top': 20, 'left': 0, 'width': 800, 'height': 600}
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


def main():
    show_fb()


if __name__ == '__main__':
    main()
