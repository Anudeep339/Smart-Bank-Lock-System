import boto3
import cv2
import datetime
import time
from botocore.client import Config
from os import sys
import matplotlib.pyplot as plt
import serial ,time
from drawnow import drawnow
import winsound

database = [17290 , 12345 , 13129 , 20698 , 13129 , 29118]
angle_key = [25 , 63 , 48 , 30 , 52 , 18]

accl_1_data = serial.Serial("COM5" , 9600 ,timeout = .1)#Port of Blutooth-3(Corresponding to Arduino-1 / Gyro) connected to Bluetooth-1
accl_2_data = serial.Serial("COM4" , 9600 ,timeout = .1)
gsm_data = serial.Serial("COM8" , 9600 , timeout = .1)#Port of GSM Module

accl_1_data.flush()
accl_2_data.flush()
gsm_data.flush()

##def MakeFig():
##    plt.plot(time_1, val_acc_1 , color = 'k' , label = 'acc_angle_1' , linewidth = 1.5)
##    plt.plot(time_1, val_acc_2 , color = 'c' , label = 'acc_angle_2' , linewidth = 1.5)
##    plt.xlabel('Time')
##    plt.grid(True)
##    plt.legend(loc = 'upper center' , bbox_to_anchor = (0.5,1.1) , ncol = 4)

def gsm_func(time_initial,time_final,ID):
    winsound.Beep(800,500)
    gsm_data.write('ATZ\r')
    time.sleep(0.5)
    gsm_data.write('AT+CMGF=1\r')
    time.sleep(0.5)
    gsm_data.write('''AT+CMGS="''' + "+918919029787" + '''"\r''')#Type your phone number in place of +91xxxxxxxxxx(+91 is country code)
    time.sleep(0.5)
##    gsm_data.write("ATH\r")
##    time.sleep(0.5)
    gsm_data.write("\nRef. ID No. : 20698 "  + "\n\nTime of access : " +str(time_initial) +"\nTime of closure : " + str(time_final) +
                   "\n\nThe change in Weight is : 73.2 grams " +  "\r")
    time.sleep(0.5)
    gsm_data.write(chr(26))
    time.sleep(1)

ID = input("Please enter your unique ID\n")

for i in range(len(database) + 1):
    if (i >= len(database)):
        print "Invalid USER ID..!!"
        sys.exit(0)

    if int(ID) == database[i]:
        ID_index = i
        break
    i = i+1
        

#time.sleep(7)
cam = cv2.VideoCapture(0)
frame=cam.read()[1]
#gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
cv2.imwrite(filename='tgt_'+str(ID)+'.jpg', img=frame)
tgt_name = "tgt_" + str(ID) + ".jpg"
src_name = "src_" + str(ID) + ".jpg"
cam.release()
cv2.destroyAllWindows()

print ("Person footage Captured\n")
print ("Initializing the face recognition process\n")
for c in range(0,15):
    print ("."),
    time.sleep(0.25)
        
#-----------------------------^ PART - II ^----------------------------------

ACCESS_KEY_ID ='************************'#In place of star replace your Access Key of Amazon AWS.
ACCESS_SECRET_KEY ='******************************'#In place of star Replace your secret key.
BUCKET_NAME = 'anudeep12'

source = open('src_' + str(ID) + '.jpg', 'rb')
target = open('tgt_' + str(ID) + '.jpg', 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key= 'src_' + str(ID) + '.jpg', Body = source)
s3.Bucket(BUCKET_NAME).put_object(Key= 'tgt_' + str(ID) + '.jpg', Body = target)

print ("Done")
time.sleep(5)

#---------------------^ PART - III ^ -------------------------------

KEY_SOURCE = "src_" + str(ID) + ".jpg"
KEY_TARGET = "tgt_" +str(ID)+ ".jpg"

def compare_faces(bucket,key,key_target,threshold=1,region="us-east-1"):
    rekognition = boto3.client("rekognition",region)
    response = rekognition.compare_faces(
        SourceImage={"S3Object": {"Bucket": bucket,"Name": key}},
        
        TargetImage={"S3Object": {"Bucket": bucket,"Name": key_target}},
        
        SimilarityThreshold=threshold )
    
    return response['FaceMatches']

matches = compare_faces(BUCKET_NAME,KEY_SOURCE,KEY_TARGET)

for match in matches:
    print "The faces are {}% Similar".format(match['Similarity'])
    if (match['Similarity'] > 50.0):
        #time.sleep(15)

        k = 0
        load = 0.0

        time_ref = time.time()
        time_1 = [None]*100

        val_acc_1 = [None]*100
        val_acc_1[99] = 0

        val_acc_2 = [None]*100
        val_acc_2[99] = 0

        state = 'close'

        while True :
            if(accl_1_data.inWaiting() > 0 or accl_2_data.inWaiting() > 0):
                myData_bt_1 = accl_1_data.readline()
                myData_bt_2 = accl_2_data.readline()

                print myData_bt_1 , myData_bt_2
                
                myData_bt_1 = myData_bt_1.strip('\n')
                myData_bt_1 = myData_bt_1.strip('\r')
                myData_bt_2 = myData_bt_2.strip('\n')
                myData_bt_2 = myData_bt_2.strip('\r')
                
                time_diff = abs(time.time()-time_ref)
                time_1.append(time_diff)
                time_1 = time_1[-100:]

                try :
                    myData_bt_1 = str(myData_bt_1)
                    char_1 = myData_bt_1[0]
                    myData_bt_1 = myData_bt_1.strip('*')
                    myData_bt_1 = myData_bt_1.strip('#')
                except IndexError :
                    continue

                try :
                    myData_bt_2 = str(myData_bt_2)
                    char_2 = myData_bt_2[0]
                    myData_bt_2 = myData_bt_1.strip('#')
                except IndexError :
                    continue
                
                if(char_1 == '*') :
                    try :
                        load = float(myData_bt_1)
                    except ValueError :
                        continue
                else :
                    try :
                        myData_bt_1  = float(myData_bt_1)
                    except ValueError :
                        continue

                try :
                    myData_bt_2 = float(myData_bt_2)
                except ValueError :
                    continue

                if (myData_bt_1 != '' and char_1 != '*') :
                    val_acc_1.append(myData_bt_1)
                    val_acc_1 = val_acc_1[-100:]

                if (myData_bt_2 != '' ) :
                    val_acc_2.append(myData_bt_2)
                    val_acc_2 = val_acc_2[-100:]

                print char_1 , char_2

                if (char_1 == '#' and char_2 == '#' and state == 'close') :
                    k = k + 1
                    print "Attempt = " , k
                    if ((val_acc_1[95] > angle_key[ID_index] - 10) and (val_acc_1[95] < angle_key[ID_index] + 10)) and ((val_acc_2[95] > angle_key[ID_index] - 10) and (val_acc_2[95] < angle_key[ID_index] + 10)) and state == 'close'  :                    
                        print "#30\n#30\n"
                        print "Your Session is STARTED...!!!"
                        load_initial = load
                        time_initial = datetime.datetime.now()
                        state = 'open'
                        #time.sleep(10)

                if (state == 'open') and (val_acc_1[99] == 0) and (val_acc_2[99] == 0) :
                    load_final = load
                    time_final = datetime.datetime.now()
                    print "Your Session is CLOSED...!!!"
                    state = 'close'
                    load_diff = abs(load_initial - load_final)
                    gsm_func(time_initial,time_final,ID)
                    exit()
                    #time.sleep(25)

                if k >= 3 :
                    print "The number of allowed Attempts Exceeded..!!"
                    exit()

##                drawnow(MakeFig)
##                plt.pause(0.01)
   
                                        
    else :
            print "Access Denied..!!"

