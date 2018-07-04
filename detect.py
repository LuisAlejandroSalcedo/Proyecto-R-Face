import math
import cv2
import numpy as np
import config

def levelFace(image, face):
    ((x, y, w, h), eyedim) = face
    if len(eyedim) != 2:
        return image[y:y+h, x:x+w]

    leftx = eyedim[0][0]
    lefty = eyedim[0][1]
    rightx = eyedim[1][0]
    righty = eyedim[1][1]
    if leftx > rightx:
        leftx, rightx = rightx, leftx
        lefty, righty = righty, lefty
    if lefty == righty or leftx == rightx:
        return image[y:y+h, x:x+w]

    rotDeg = math.degrees(math.atan((righty - lefty) / float(rightx - leftx)))
    if abs(rotDeg) < 20:
        rotMat = cv2.getRotationMatrix2D((leftx, lefty), rotDeg, 1)
        rotImg = cv2.warpAffine(image, rotMat, (image.shape[1], image.shape[0]))
        return rotImg[y:y+h, x:x+w]

    return image[y:y+h, x:x+w]

def detectFaces(image, faceCascade, eyeCascade=None, returnGray=True):
    cas_rejectLevel = 1.3
    cas_levelWeight = 5

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, cas_rejectLevel, cas_levelWeight)
    result = []
    for (x, y, w, h) in faces:
        eyes = []
        if eyeCascade != None:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eyeCascade.detectMultiScale(roi_gray)

        result.append(((x, y, w, h), eyes))

    if returnGray:
        return gray, result
    else:
        return image, result

if __name__ == '__main__':

    cv2.namedWindow("camera", 1)
    width = None
    height = None

    faceCascade = cv2.CascadeClassifier('cascades/face.xml')
    eyeCascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')


    while True:
        img = cv2.imread('test/barack.jpg')
        image, face_dim = detectFaces(img, faceCascade, eyeCascade, False)
        for ((x, y, w, h), eye_dim) in face_dim:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            for (ex, ey, ew, eh) in eye_dim:
                cv2.rectangle(image, (ex+x, ey+y), (ex+x+ew, ey+y+eh), (0, 255, 0), 2)

        cv2.imshow("camera", image)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()
