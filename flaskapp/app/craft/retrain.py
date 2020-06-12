import keras_ocr
import imgaug
import cv2

import json
import csv
import os

import tensorflow as tf

from network import create_craft
from filter import filter_corrections
from sklearn.model_selection import train_test_split

from config import Config
data_dir = '../'

from app.rc_ocr.rc_stream import get_corrections, history_to_s3

with open(os.path.join(data_dir,Config.CRAFT_DECODER)) as file:
    decoder = json.load(file)

def generate_labels():
    corrections = get_corrections()
    labels = filter_corrections(corrections)
    
    print(f"Correction data size - {len(labels)}")
    ratios = 0.9
    train_labels = labels[:int(ratios*len(labels))]
    test_labels = labels[int(ratios*len(labels)):]

    return train_labels, test_labels

#Initialize OCR Model
def train():
    craft = create_craft()
    recognizer = craft.recognizer

    batch_size = 32

    augmenter = imgaug.augmenters.Sequential([
        imgaug.augmenters.GammaContrast(gamma=(0.25, 3.0)),
    ])

    train_labels, validation_labels = generate_labels()
    train_labels, validation_labels = train_test_split(train_labels, test_size=0.2, random_state=42)
    (training_image_gen, training_steps), (validation_image_gen, validation_steps) = [
        (
            keras_ocr.datasets.get_recognizer_image_generator(
                labels=labels,
                height=recognizer.model.input_shape[1],
                width=recognizer.model.input_shape[2],
                alphabet=recognizer.alphabet,
                augmenter=augmenter
            ),
            len(labels) // batch_size
        ) for labels, augmenter in [(train_labels, augmenter), (validation_labels, None)]
    ]

    #set a fix validation gen
    training_gen, validation_gen = [
        recognizer.get_batch_generator(
            image_generator=image_generator,
            batch_size=batch_size
        )
        for image_generator in [training_image_gen, validation_image_gen]
    ]

    #Training
    train_folder = '../../data/craft/train/craft/'
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(f"{train_folder}checkpoints", exist_ok=True)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=10, restore_best_weights=False),
        tf.keras.callbacks.CSVLogger(f'{train_folder}recognizer_registrationtext.csv')
    ]

    history = recognizer.training_model.fit_generator(
        generator=training_gen,
        steps_per_epoch=training_steps,
        validation_steps=validation_steps,
        validation_data=validation_gen,
        callbacks=callbacks,
        epochs=1,
    )
    #store history to S3
    history_to_s3(history.history)

    lowest_loss = min(history.history['val_loss'])
    #set validation loss threshold to save model
    loss_thresh = 0.6
    if lowest_loss < loss_thresh:    
        #savemodel
        model_path = os.path.join(data_dir,Config.CRAFT_MODEL)
        recognizer.training_model.save()
        print(f"New model saved, current loss - {lowest_loss}")
if __name__ == '__main__':
    train()