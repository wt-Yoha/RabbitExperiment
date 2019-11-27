import json


# 评分系统 维护一个实现了 GiveMark 接口的函数队列 用于给当前的 checkedObjects 评分
class GradeSYS:
    def __init__(self, configFile):
        self.pakage = __import__("GiveMark")  # 获取当前包的引用
        self.transcript = {}  # 维护一个成绩单字典 用于保存评分结果
        self.commandLine = []  # 维护一个评分操作的列表

        with open(configFile, "r", encoding="utf-8") as fp:  # 由 config 确定哪些评分项需要被载入
            config = json.load(fp)
            self.classList = config['scoresLine']

        for className in self.classList:
            cl = getattr(self.pakage, className)  # 获取目标类的引用
            markObject = cl(self.transcript)  # 给入成绩单，创建一个评分对象
            self.commandLine.append(markObject)  # 将评分对象加入执行链

    def beginMarkLine(self, checkedObjects):
        # 给入当前的目标检测情况 开始一个轮次的评分
        for markObj in self.commandLine:
            if markObj.giveMark(checkedObjects):
                # 如果返回值为 True 则表示该项测试已结束 将其移出评分序列
                self.commandLine.remove(markObj)

    def printTranscript(self):
        print(self.transcript)


# 所有评分函数的接口
class GiveMark:
    def __init__(self, transcript):
        # 目前已经检测到的目标  checkedObjects 为一个列表，下标即为对应的 Object
        # 1：兔子  2：剪刀  3：伤口  4：手  5：耳朵  6：针头
        # 列表的值 第一项为 Object 到目前为止出现的次数(为了减小错误识别造成的影响，暂定出现40次时确定该物品已被检测到) , 第二项为一个标识 Object 当前位置的元组
        self.transcript = transcript
        self.minTimes = 40

    def giveMark(self, transcript):
        print("You got 99 points!")


# =====================所有的评分方法在此添加============================================
class checkCatching(GiveMark):
    def giveMark(self, checkedObjects):
        stage = checkedObjects[6][0]
        rabbitPos = checkedObjects[0][2]
        rabbitCenterX = (rabbitPos[0]+rabbitPos[2])/2
        rabbitCenterY = (rabbitPos[1]+rabbitPos[3])/2
        if (stage == 0 and rabbitCenterX>640 and rabbitCenterX<1280 and rabbitCenterY>360 and rabbitCenterY<720):
            print('有效的抓拿判断帧...')
            if (checkedObjects[3][0] == 1 and checkedObjects[4][0] == 1):
                handPos = checkedObjects[3][2]
                earPos = checkedObjects[4][2]
                j = self.judgeCatching(handPos, earPos)
                if j:
                	self.transcript['抓拿判定'] = 10
                else:
                	self.transcript['抓拿判定'] = 0
                print('抓拿判定结束')
	
    def judgeCatching(self, handPos, earPos):
        if earPos[2]<handPos[0]:
           print('错误！抓屁股')
           return False
        elif (earPos[0]>handPos[0]-30 and earPos[2]<handPos[2]+30):
           print('错误！抓耳朵')
           return False
        else:
           return True
            
            
    

class checkWound(GiveMark):
    # 检查伤口是否存在
    def giveMark(self, checkedObjects):
        print("伤口检测开始...")
        if checkedObjects[2][0] > self.minTimes:
            self.transcript['伤口检测'] = 10
            return True
        print("伤口检测结束")
        return False


class checkNeedle(GiveMark):
    def giveMark(self, checkedObjects):
        print("针头检测开始...")
        print("针头检测结束")
        return False


class checkNerve(GiveMark):
    def giveMark(self, checkedObjects):
        print("神经检测开始...")
        print("神经检测结束")
        return False
# ======================================================================================


# 测试
if __name__ == '__main__':
    gs = GradeSYS("ScoresLine.json")

    checkedObjects = [[] for i in range(6)]
    checkedObjects[2].append(43)
    checkedObjects[2].append((1, 1, 1, 1))

    gs.beginMarkLine(checkedObjects)

    gs.printTranscript()
