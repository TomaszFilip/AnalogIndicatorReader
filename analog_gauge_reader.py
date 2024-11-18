import cv2
import numpy as np

PI=3.14
WHITE,GREEN=(255,255,255), (0,255,0)

def avg_circles(circles, b):
    avg_x=0
    avg_y=0
    avg_r=0
    for i in range(b):
        #optional - average for multiple circles (can happen when a gauge is at a slight angle)
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x/(b))
    avg_y = int(avg_y/(b))
    avg_r = int(avg_r/(b))
    return avg_x, avg_y, avg_r

def calibrate_circle(gauge_number, file_type):
    img = cv2.imread('./analog_scale_img/%s.%s' %(gauge_number, file_type))
    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #save gray image
    cv2.imwrite('gauge-%s-bw.%s' %(gauge_number, file_type),gray)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(height*0.30), int(height*0.45))
    a, num_of_circles, c = circles.shape
    x,y,r = avg_circles(circles, num_of_circles)
    cv2.circle(img, (x, y), r, GREEN, 3, cv2.LINE_AA)  # draw circle
    cv2.circle(img, (x, y), 2, GREEN, 3, cv2.LINE_AA)  # draw center of circle
    #save gray image with average circle and circle center
    cv2.imwrite('gauge-%s-circles.%s' % (gauge_number, file_type), img)

    separation = 10.0 #in degrees
    interval = int(360 / separation)
    p1 = np.zeros((interval,2))  #set empty arrays
    p2 = np.zeros((interval,2))
    p_text = np.zeros((interval,2))
    
    
    for i in range(0,interval):
        for j in [0,1]:
            if (j%2==0):
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * PI / 180) 
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * PI / 180)
                
    text_offset_x = 10
    text_offset_y = 5
    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p2[i][j] = x + r * np.cos(separation * i * PI / 180)
                p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos((separation) * (i-9) * PI / 180)
            else:
                p2[i][j] = y + r * np.sin(separation * i * PI / 180)
                p_text[i][j] = y + text_offset_y + 1.2* r * np.sin((separation) * (i-9) * PI / 180)

    for i in range(0,interval):
        cv2.line(img, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),WHITE, 2)
        cv2.putText(img, '%s' %(int((i*separation)*160/360)), (int(p_text[i][0]), int(p_text[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3,WHITE,1,cv2.LINE_AA)
        
    #save image with circle,lines
    cv2.imwrite('gauge-%s-calibration.%s' % (gauge_number, file_type), img) 

def read_needle(gauge_number, file_type):
    img = cv2.imread('./analog_scale_img/%s.%s' %(gauge_number, file_type))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #TODO

def main():
    numbers=[1,2,3,4]
    for n in numbers:
        gauge_number = n
        file_type='jpeg'
        print('./analog_scale_img/%s.%s' % (gauge_number, file_type))
        calibrate_circle(gauge_number, file_type)
        read_needle(gauge_number, file_type)
        
if __name__=='__main__':
    main()
   	
