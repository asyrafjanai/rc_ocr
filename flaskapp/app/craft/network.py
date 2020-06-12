import json
import keras_ocr
import os
import pickle

from app import root_dir
from app.config import Config
from pathlib import Path

import tensorflow as tf
# from app.rc_ocr.rc_stream import weights_from_s3, coder_from_s3

data_dir = Path(root_dir)

class CRAFT():
    def __init__(self):
        self.decoder_path = os.path.join(
                root_dir, 'data', 'craft','character_label_decoder.json')
        with open(self.decoder_path) as f:
            self.decoder = json.load(f)
        recognizer_alphabet = ''.join(self.decoder.values())
        try:
            #initialize recognizer
            self.recognizer = keras_ocr.recognition.Recognizer(
                alphabet=recognizer_alphabet,
                weights='kurapan'
            )
            self.recognizer.include_top = True
            self.recognizer.compile()
            for layer in self.recognizer.backbone.layers:
                layer.trainable = False
        except Exception as e:
            print(e)
            # Default model
            self.recognizer = keras_ocr.recognition.Recognizer()
            self.recognizer.compile()

        #initialize detector
        self.detector = keras_ocr.detection.Detector()
        #load weights
        # recognizer_weights = weights_from_s3('recognizer-weights')
        # use  local weight
        recognizer_weights = self.recognizer.model.load_weights(
            os.path.join(
                root_dir, 'data', 'craft', 'recognizer_registrationtext.h5')
            )
        # self.recognizer.model.set_weights(recognizer_weights)
        self.pipeline = keras_ocr.pipeline.Pipeline(recognizer=self.recognizer)

    #compete pipeline predictions
    def __call__(self, img):
        prediction_groups = self.pipeline.recognize(img)

    def get_recognizer(self):
        return self.recognizer
        
    def get_pipeline(self):
        return self.pipeline

    def recognize(self, img):
        recognitions = self.recognizer.recognize([img])
        return recognitions

    def detect(self, img):
        detections = self.detector.detect([img])
        return detections

    def predict(self, img):
        prediction_groups = self.pipeline.recognize([img])
        return prediction_groups

def create_craft():
    return CRAFT()

    
