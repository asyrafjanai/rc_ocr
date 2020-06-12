import cv2
import os
import time
import json
import random

from network import create_craft
from filter import get_reg_info, remove_noise

def test():
    IMAGE_NUM = 5

    img_path = '../../data/registrationregion/img/'
    image_filenames = os.listdir(img_path)

    start = IMAGE_NUM
    end = len(image_filenames)

    end_idx = random.randint(start,end)
    start_idx= end_idx-IMAGE_NUM

    images = [ cv2.imread(f"{img_path}{image_name}") for image_name in image_filenames[start_idx:end_idx] ]
    craft = create_craft()
    model = craft.pipeline
    start_time = time.time()
    predictions = model.recognize(images)
    # print(predictions)
    pred_texts = [' '.join([character for character,_ in prediction]) for prediction in predictions ]
    reg_info = [{'text':remove_noise(pred_text.upper()) , **get_reg_info(pred_text)} for pred_text in pred_texts]
    print(json.dumps(reg_info, indent=2))
    print("--- %s images execution : %s seconds  ---" % (IMAGE_NUM, (time.time() - start_time)) )

if __name__ == '__main__':
    test()