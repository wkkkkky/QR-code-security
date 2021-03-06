from yolo import YOLO
from PIL import Image


# 用于调用YOLO的detect_img函数来识别输入的图片
# 输入参数：本地图片的路径
# 传入yolo参数是为了不用每次都载入模型，好节约时间
def detect_img(yolo, path):
    # yolo = YOLO()
    try:
        image = Image.open(path)
        r_image, temp, classID = yolo.detect_image(image)
        # print(classID)
        return classID
    except Exception as e:
        print(e)

# if __name__ == "__main__":
#     detect_img('./templates/images/baidu.jpg')
