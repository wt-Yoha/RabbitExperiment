import cv2
import time
import numpy
import GiveMark


class Detector:
    # 运行的检测类，用于检测当前图片上的物品，并维护一个 List checkedObject

    def __init__(self):
        self.deploy_path = 'no_bn.prototxt'
        self.model_path = 'no_bn.caffemodel'
        self.SIZE = 300
        self.classNum = 6  # 目前能够识别的物品数量
        # 列表的值 第一项为 Object 到目前为止出现的次数(为了减小错误识别造成的影响，暂定出现40次时确定该物品已被检测到) , 第二项为一个标识 Object 当前位置的元组
        self.checkedObjects = [[0, []] for i in range(self.classNum)]
        self.net = cv2.dnn.readNetFromCaffe(self.deploy_path, self.model_path)

    def getCheckedObjects(self):
        return self.checkedObjects

    def printCheckedObjects(self):
        objName = ['兔子', '剪刀', '伤口', '手', '耳朵', '针头']
        for oName, obj in zip(objName, self.checkedObjects):
            if obj[0] > 0:
                print("【", oName, "】", ": ", obj[0],obj[1], end=" ")
        print()

    def checkImg(self, img):
        assert isinstance(img, numpy.ndarray), "输入对象不是图片!"

        rows = img.shape[0]
        cols = img.shape[1]
        self.net.setInput(
            cv2.dnn.blobFromImage(img, 1.0 / 127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=False, crop=False))

        start_time = time.time()
        cvOut = self.net.forward()
        print('time cost: ', time.time() - start_time)

        for detection in cvOut[0, 0, :, :]:
            score = float(detection[2])
            if score > 0.3:
                left = detection[3] * cols
                top = detection[4] * rows
                right = detection[5] * cols
                bottom = detection[6] * rows
                self.checkedObjects[int(detection[1] - 1)][0] += 1
                self.checkedObjects[int(detection[1] - 1)][1] = (int(left), int(top), int(right), int(bottom))

                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
                text = str(detection[1])
                cv2.putText(img, text, (int(left), int(top)), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)

        ratiao = rows / cols
        img = cv2.resize(img, (int(cols / 2), int(cols / 2 * ratiao)))
        return img


# 测试
if __name__ == '__main__':
    detector = Detector()
    gradSys = GiveMark.GradeSYS("ScoresLine.json")

    import glob
    imgStram = glob.glob("img/*.jpg")  # 获取img路径下的所有 jpg 图片
    for im in imgStram:
        im = cv2.imread(im)
        im = detector.checkImg(im)
        detector.printCheckedObjects()
        gradSys.beginMarkLine(detector.getCheckedObjects())
        gradSys.printTranscript()
        cv2.imshow("img", im)
        cv2.waitKey(0)
