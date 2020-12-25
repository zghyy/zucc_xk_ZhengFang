import os
# 安装Pillow
from PIL import Image
# import matplotlib.pyplot as plt

#
# def show_code(image=None, path='.\\'):
#     if sys.platform== "linux":
#         path='./'
#     if image:
#         image = Image.open(path + "code.gif")
#     plt.figure("CODE")
#     plt.imshow(image)
#     plt.show()
#     return image


def stay_blue2gray(image):
    image = image.convert('RGB')
    height = image.size[0]
    width = image.size[1]
    for y in range(width):
        for x in range(height):
            pix_data = image.getpixel((x, y))
            if pix_data[0] <= 40 and pix_data[1] <= 40 and pix_data[2] >= 65:
                image.putpixel((x, y), (0, 0, 0))
                continue
            else:
                image.putpixel((x, y), (255, 255, 255))
    image = image.convert('L')
    return image


def split_image(image):
    images = []
    x = 5
    y = 0
    w = 12
    h = 23
    for i in range(4):
        images.append(image.crop((x, y, x + w, y + h)))
        x += w
        # images[i].save(str(i) + '.gif')
    return images


def ocr(images, dir_now):
    result = ""
    models = []
    file_names = []
    # 加载模型
    try:
        model_path = dir_now + r'zfgetcode\data\model'
        for filename in os.listdir(model_path):
            model = Image.open(model_path + "\\" + filename)
            file_names.append(filename[0:1])
            models.append(model.convert('L'))

    except BaseException:
        dir_now=dir_now[:-1]+"/"
        model_path = dir_now + r'zfgetcode/data/model'
        for filename in os.listdir(model_path):
            model = Image.open(model_path + "/" + filename)
            file_names.append(filename[0:1])
            models.append(model.convert('L'))

    # 分别识别切割的单子字符
    for image in images:
        result += (single_char_ocr(image, models, file_names))
    return result


def single_char_ocr(image, models, file_names):
    # 识别一个字符
    result = "#"
    height = image.size[0]
    width = image.size[1]
    min_count = width * height
    for i in range(len(models)):
        model = models[i]
        if model.size[1] - width > 2:
            print("OCR_CODE.py--71")
            continue
        count = 0
        width_min = width if width < model.size[1] else model.size[1]
        height_min = height if width < model.size[0] else model.size[0]
        for y in range(width_min):
            done = False
            for x in range(height_min):
                if model.getpixel((x, y)) != image.getpixel((x, y)):
                    count += 1
                    if count >= min_count:
                        done = True
                        break
            if done:
                break
        if count <= 3:
            result = file_names[i]
            print(result)
        elif count < min_count:
            min_count = count
            result = file_names[i]
    return result


def run(image_path, dir_now):
    image = Image.open(image_path + "code.gif")
    # show_code(image)
    image = stay_blue2gray(image)
    images = split_image(image)
    result = ocr(images, dir_now)
    # print(result)
    return result


if __name__ == "__main__":
    print(run(os.getcwd() + "/",os.getcwd() + "/"))
