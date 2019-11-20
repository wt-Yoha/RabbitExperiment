import cv2
import sys
import time
from glob import glob


deploy_path = 'no_bn.prototxt'
model_path = 'no_bn.caffemodel'
SIZE = 300


def run(img):
    net = cv2.dnn.readNetFromCaffe(deploy_path, model_path)

    rows = img.shape[0]
    cols = img.shape[1]
    net.setInput(cv2.dnn.blobFromImage(img, 1.0 / 127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=False, crop=False))

    start_time = time.time()
    cvOut = net.forward()
    print('time cost: ', time.time() - start_time)

    for detection in cvOut[0, 0, :, :]:
        score = float(detection[2])
        if score > 0.3:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows

            cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
            text = str(detection[1])
            cv2.putText(img, text, (int(left), int(top)), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)

    ratiao = rows / cols
    img = cv2.resize(img, (int(cols / 2), int(cols / 2 * ratiao)))
    return img


if __name__ == "__main__":
    # image = cv2.imread("./000323.jpg")
    # image = run(image)
    # cv2.imwrite("result.jpg", image)
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)

    imgs = glob("./img/*.jpg")

    command = -1
    for i in range(len(imgs)):
        im = cv2.imread(imgs[i])
        result = run(im)
        cv2.imshow("image", result)
        cv2.waitKey(0)
