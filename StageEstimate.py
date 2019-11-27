import cv2
import time
import numpy as np
import json
import tensorflow as tf
import os

from model_params.neural_net import TwoLayerNet

class StageEstimate():
    #	判断图像是抓拿、麻醉、固定、手术的哪一个阶段

    def __init__(self, configFile):

        with open(configFile, "r", encoding="utf-8") as fp:  # 载入参数
            config = json.load(fp)
            self.W1 = np.loadtxt(config['W1'], dtype=np.float32)
            self.W2 = np.loadtxt(config['W2'], dtype=np.float32)
            self.b1 = np.loadtxt(config['b1'], dtype=np.float32)
            self.b2 = np.loadtxt(config['b2'], dtype=np.float32)
            self.X_mean = np.loadtxt(config['X_mean'], dtype=np.float32)
            self.U = np.loadtxt(config['U'], dtype=np.float32)

            self.model_dir = config['model_dir']
            self.net = TwoLayerNet(1000, 100, 4)
            self.net.params['W1'] = self.W1
            self.net.params['b1'] = self.b1
            self.net.params['W2'] = self.W2
            self.net.params['b2'] = self.b2


    def create_graph(self):
        with tf.gfile.GFile(os.path.join(
                self.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')



    def estimate(self, img):
        with tf.Session() as sess:
            image_data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pool_3_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')
            feature = sess.run(pool_3_tensor, {'DecodeJpeg:0': image_data}) 
            feature = feature - self.X_mean
            feature = np.dot(feature, self.U[:,:1000])
            result = self.net.predict(feature)
            return result
#	测试
if __name__ == '__main__':
    se= StageEstimate("ScoresLine.json")
    se.create_graph()

    import glob
    imgStram = glob.glob("img/*.jpg")  # 获取img路径下的所有 jpg 图片
    for im in imgStram:
        im = cv2.imread(im)
        result = se.estimate(im)
        print(result[0])
        cv2.imshow("img", im)
        k = cv2.waitKey(10)
        if (k == ord('q')):
            break

