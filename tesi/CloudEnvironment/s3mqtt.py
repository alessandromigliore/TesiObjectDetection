import cv2
import time
import logging
import json
import os
import time
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import numpy as np
import urllib


def main():
 video_fname = '#PATH FOLDER/VIDEO NAME'
 camera_id = 0
 
 cap = cv2.VideoCapture(camera_id)

 # Define the codec and create VideoWriter object. For mac mp4v or avi1 is the best option.
 # You can also use: 0x00000021 if this codec doesn't work for you
 fourcc = cv2.VideoWriter_fourcc(*'MJPG')

 # Create a video writer, specify the codec as well as the image widge and height.
 # cap.get(3) is the width, and cap.get(4) is the height of the camera in cap.
 out = cv2.VideoWriter(video_fname, fourcc, 5.0, (int(cap.get(3)), int(cap.get(4))))
 
 start_time = time.time()
 
 while( int(time.time() - start_time) < 10 ):
  ret, frame = cap.read()
  
  if ret==True:
   out.write(frame)

   #if cv2.waitKey(1) & 0xFF == ord('q'):
   # print("\nstop signal received.")
   # break
   
  else:
      break
      
      
 # When everything done, release the capture
 cap.release()
 out.release()
 cv2.destroyAllWindows()


 # Opens the Video file
 cap2= cv2.VideoCapture('#PATH FOLDER /VIDEO NAME')
 i=0
 while(cap2.isOpened()):
     ret, frame = cap2.read()
     if ret == False:
         break
     
     if i % 10 == 0:
     	cv2.imwrite('/home/alessandro/Scrivania/buffers3/frame'+str(i)+'.jpg',frame)
     	client = boto3.client('s3', region_name='eu-west-1')
     	client.upload_file('#PATH FOLDER/frame'+str(i)+'.jpg', '#BUCKET' ,'images/frame'+str(i)+'.jpg')
     i+=1
 
 cap2.release()
 cv2.destroyAllWindows()
 
main()

