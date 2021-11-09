import cv2
import greengrasssdk
import time
import logging
import json
    
client = greengrasssdk.client('iot-data')
    
OUTPUT_TOPIC = 'video/output'

def lambda_handler(event, context):
 video_fname = "/buffer/demo_1000.avi"
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
 cap2= cv2.VideoCapture('/buffer/demo_1000.avi')
 i=0
 while(cap2.isOpened()):
     ret, frame = cap2.read()
     if ret == False:
         break
     
     if i % 10 == 0:
     	cv2.imwrite('/buffer/frame'+str(i)+'.jpg',frame)
     	msg2 = json.dumps({'filepath':'/shared/greengrass/buffer/frame'+str(i)+'.jpg'})
     	client.publish(topic='blog/infer/input', payload=msg2)
     i+=1
 
 cap2.release()
 cv2.destroyAllWindows()
 msg = 'Funzione partita'
 logging.info(msg)
 client.publish(topic=OUTPUT_TOPIC, payload=msg)