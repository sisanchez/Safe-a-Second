# -*- coding: utf-8 -*-

from RPi import GPIO
import time

# �nimport�e�n�N�㦳SDK��TencentYoutuyun��Ƨ��[�J�M�פ�
import TencentYoutuyun
import cv2

GPIO.setmode(GPIO.BCM)

# ��J�U�����_
appid = 'XXXXXXXXXX'
secret_id = 'XXXXXXXXXXXXXXXXXXXXXXX'
secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
userid = 'test'  # ���N�r���

face_cascade = cv2.CascadeClassifier('xml_file/haarcascade_frontalface_default2.xml')
cap = cv2.VideoCapture(0)
i = 0
count_face = 0

# GPIO ports for the 7seg pins
segments = (11, 4, 23, 8, 7, 10, 18, 25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
GPIO.setup(segments, GPIO.OUT, initial=0)

# GPIO ports for the digit 0-3 pins 
digits = (22, 27, 17, 24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
GPIO.setup(digits, GPIO.OUT, initial=1)

# green
GPIO.setup(19, GPIO.OUT)
# red
GPIO.setup(26, GPIO.OUT)

#          (a,b,c,d,e,f,g,dp)
num = {' ': (0, 0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0, 0),
       '1': (0, 1, 1, 0, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1, 0),
       '3': (1, 1, 1, 1, 0, 0, 1, 0),
       '4': (0, 1, 1, 0, 0, 1, 1, 0),
       '5': (1, 0, 1, 1, 0, 1, 1, 0),
       '6': (1, 0, 1, 1, 1, 1, 1, 0),
       '7': (1, 1, 1, 0, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1, 0),
       '9': (1, 1, 1, 1, 0, 1, 1, 0),
       'b': (0, 0, 1, 1, 1, 1, 1, 0),
       'y': (0, 1, 1, 1, 0, 1, 1, 0),
       'E': (1, 0, 0, 1, 1, 1, 1, 0),
       'A': (1, 1, 1, 0, 1, 1, 1, 0),
       'L': (0, 0, 0, 1, 1, 1, 0, 0),
       'X': (0, 1, 1, 0, 1, 1, 1, 0)}

GPIO.output(19, False)
GPIO.output(26, True)


def seg():
    for digit in range(2):
        GPIO.output(segments, (num[display_string[digit]]))
        GPIO.output(digits[digit], 0)
        time.sleep(0.01)
        GPIO.output(digits[digit], 1)


try:
    n = 2100

    while n >= -2:
        display_string = str(n).rjust(4)
        if n == 0:
            display_string = '00  '
        seg()
        n -= 1
        if 1098 < n < 1100:
            print("--------------take photo---------------")
            # �}�l�i�氻��(�Ĥ@��)

            # �j��]10�� = 2����(�g�L�ڱM�~�����q + = = )
            while 1:

                ret, img = cap.read()
                ret, takeimg = cap.read()
                ret, takeimg_2 = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                i = i + 1

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    oi_gray = gray[y:y + h, x:x + w]
                    roi_color = img[y:y + h, x:x + w]

                    # show image
                cv2.imshow('Take_Photo', img)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

                    # take photo
                if i == 3:
                    takephoto_filename = time.strftime('take_pic/%Y%m%d-%H%M%S') + "_01.jpg"
                    cv2.imwrite(takephoto_filename, takeimg)
                    takephoto = "detaction_Pic/face_image.jpg"
                    cv2.imwrite(takephoto, takeimg_2)

                    # �j��while loop interrupt
                if i == 4:
                    break

            cap.release()
            cv2.destroyAllWindows()

            # �H�y�Ϥ���m
            image_pathstr_1 = "detaction_Pic/face_image.jpg"
            end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT  # �˰T�u�϶}�񥭥x
            youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)
            ret = youtu.DetectFace(image_path=image_pathstr_1, mode=0, data_type=0)

            for j in ret["face"]:
                count_face = count_face + 1
            print("�H�y�� = " + count_face.__str__())
            print("--------------over---------------")

        if count_face >= 1:
            n = 2600
            while n >= -2:
             display_string = str(n).rjust(4)
             if n == 0:
              display_string = '00  '
            seg()
            n -= 1

        if display_string == '00  ':
          GPIO.output(19, True)
          GPIO.output(26, False)

    n = 1000
    while n >= 0:
      if n <= 50000:
        display_string = '00  '
    seg()
    n -= 1

finally:
 GPIO.cleanup()


