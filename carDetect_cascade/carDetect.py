import cv2
import imutils
import datetime
import statistics


car_cascade = cv2.CascadeClassifier("data/cars.xml")
gun_cascade = cv2.CascadeClassifier("data/gun.xml")


def main():
    
    '''
    img_car_src = "data/traffic.jpg"
    img_car_src = "data/test.jpg"
    '''
    
    #video_car_src = 'data/video1.avi'
    '''
    video_car_src = "data/jonVidTrim.mp4"
    cap = cv2.VideoCapture(video_car_src)
    vid_car_detect(cap)
    '''
    
    
    img_mesaW_src = "data/traffic10.jfif"
    carCount = img_count_cars(img_mesaW_src) 
    file = "carCount.txt"
    writeToFile(file, str(carCount))
    
    
    
    
    #video_gun_src = 'data/gun.mp4'
    #img_gun_src = "data/cop2.jpg"
    #cap = cv2.VideoCapture(video_gun_src)
    #vid_gun_detect(cap)
    #img_gun_detect(img_gun_src)

    


def writeToFile(file, write):
    
    print("Writing to File:", write)
    file = open("carCount.txt", "w")
    file.write(str(write))
    file.close()
    
    
def vid_gun_detect(cap):
    
    # initialize the first frame in the video stream
    firstFrame = None
    
    # loop over the frames of the video
    
    gun_exist = False
    
    while True:
        (grabbed, frame) = cap.read()
    
        # if the frame could not be grabbed, then we have reached the end of the video
        if not grabbed:
            break
    
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
        
        if len(gun) > 0:
            gun_exist = True
            
        for (x,y,w,h) in gun:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]    
    
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue
    
        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
    
    if gun_exist:
        print("guns detected")
    else:
        print("guns NOT detected")
    
    # cleanup the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()
    

def img_gun_detect(img_path):
    
    firstFrame = None
    
    # loop over the frames of the video
    
    gun_exist = False
    
    frame = cv2.imread(img_path)
    
        # if the frame could not be grabbed, then we have reached the end of the vid
    
        # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
        
    if len(gun) > 0:
        gun_exist = True
            
    for (x,y,w,h) in gun:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]    
    
        # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
    
        # draw the text and timestamp on the frame
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
        # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if gun_exist:
        print("guns detected")
    else:
        print("guns NOT detected")
    
    # cleanup the camera and close any open windows
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    
    
def vid_car_detect(cap):
    
    
    frameCarCount = 0
    every30Frames = []
    
    while True:
        ret, img = cap.read()
        
        if img is None:
            break
        
        
        img = imutils.resize(img, width=500)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)
        
        for (x,y,w,h) in cars:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            frameCarCount+=1
            
            
        if len(every30Frames) == 30:
            mostfrequent = statistics.mode(every30Frames)
            every30Frames = []
            print(mostfrequent)
            
        else:
            every30Frames.append(frameCarCount)
        
            
        cv2.imshow('video', img)
        #print(frameCarCount)
        frameCarCount=0

        if cv2.waitKey(27) == 30:
            break
        
    cv2.destroyAllWindows()




def img_count_cars(img_path):
    
    img = cv2.imread(img_path)
    carCount=0
    
    img = imutils.resize(img, width=490)
    gray = cv2.cvtColor(img//2, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    
    for (x, y, w, h) in cars:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        carCount+=1

    print(carCount)
    
    cv2.imshow("img", img)
    
    cv2.waitKey()
    
    return carCount

    
main()


