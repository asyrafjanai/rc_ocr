import copy
import os
import time
import logging
import json
from pathlib import Path
from datetime import timedelta

import numpy as np
import cv2
import tensorflow as tf  
from flask import request, Blueprint
from flask.json import jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.python.keras.backend import set_session

from app.craft.network import create_craft
from app.craft.filter import get_reg_info, remove_noise, sort_prediction, get_rc_info_textbox

logging.info('Initializing OCR model...')
craft_start = time.time()
craft = create_craft()
pipeline = craft.pipeline

#kickstart, dummy prediction
logging.info('Kickstarting...')
dummy_img = np.random.randint(100, size=(500,500,3)).astype(dtype='uint8')
_ = pipeline.recognize([dummy_img])

logging.info(f'OCR model loaded, time taken {time.time() - craft_start} seconds')
from app import root_dir
from app.config import Config

# initializing blueprint
rc_ocr = Blueprint('rc_ocr', __name__)

data_dir = Path(root_dir)
print(f'data_dir: {data_dir}')

# Logging config
logging.basicConfig(level=logging.DEBUG, filename="flask.log", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

# helper function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in Config.ALLOWED_EXTENSIONS


@rc_ocr.route('/')
def hello():
    return jsonify(
        is_success=True,
        message='Welcome to MyTukar data science API!'
    )

@rc_ocr.route('/ocr', methods=['POST'])
def upload_file():
    logging.info(f'Endpoint hit {request.method}')
    start = time.time()
    if request.method == 'POST':

        # read image from request
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(root_dir, 'flaskapp', 'app', 'uploads', filename)
            file.save(path)

            # file.stream.seek(0) # seek to the beginning of file
            image = cv2.imread(path)
            print(f'image size: {image.shape}')

        try:
            pipeline_start = time.time()
            predictions = pipeline.recognize([image])
            prediction = predictions[0]
            pred_text = ' '.join([character for character,_ in sort_prediction(prediction, image)])
            reg_info = get_reg_info(pred_text)
            rc_info = {'filename': filename, **reg_info}
            result = json.dumps(reg_info, indent=2)

            pred_info = {'filename': filename,
                        'text':copy.deepcopy(reg_info),
                        'boxes':get_rc_info_textbox(prediction,image)}
            
            return jsonify(
                is_success=True,
                message="Ocr success",
                exec_time='{:.2f} s'.format(time.time() - pipeline_start),
                data=result
            )

        except Exception as e:
            return jsonify(
                is_success=False,
                error='ocr error! cannot extract words',
                message=str(e),
                exec_time=f'{time.time() - start:.2f} s'
            )


        else:
            logging.info('Invalid image type!')
            return jsonify(
                is_success=False,
                error='Invalid image type!',
                message='(Allowed image type: JPEG, PNG, GIF, BMP)',
                exec_time='{:.2f} s'.format(time.time() - start)
            )


    else:
        logging.info('Something wrong with the file!')
        return jsonify(
            is_success=False,
            error='Something wrong with the file!',
            message='Use POST method!',
            exec_time='{:.2f} s'.format(time.time() - start)
        )

# error handler
@rc_ocr.errorhandler(500)
def internal_error(error):
    print(str(error)) 

@rc_ocr.errorhandler(404)
def not_found_error(error):
    print(str(error))

@rc_ocr.errorhandler(405)
def not_allowed_error(error):
    print(str(error))
