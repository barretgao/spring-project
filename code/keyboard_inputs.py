#credit to python tutorial 
#https://pythonprogramming.net/next-steps-python-plays-gta-v/

import numpy as np
from screenReading import grab_screen
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
import pyautogui


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(image, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(image, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass

def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1 = 100, threshold2=300)
    #blur the line with gaussianBlur
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    # find the region of interests
    vertices = np.array([[0,750],[0,500], [400,400], [700,400], [1024,500], [1024,750]], np.int32)
    processed_img = roi(processed_img, [vertices])

    #get the edges. 
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 100, 15)
    draw_lines(processed_img, lines)
    return processed_img

def main():
    
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    while True:
        screen = grab_screen(region=(0,40,1024,768))
        new_screen = process_img(screen)
        cv2.imshow('window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
if __name__ == '__main__':
    main()