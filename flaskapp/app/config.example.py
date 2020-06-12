import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    UPLOAD_FOLDER = os.path.join('uploads', 'rc_ocr')
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    # plate detection
    RETINA_MODEL = os.path.join('data', 'plate_detection',
                                'retinanet_latest.h5')
    PLATE_UPLOAD = os.path.join('flaskapp', 'app', 'uploads', 'plate_blur')


    # keras ocr
    CLS_MODEL = os.path.join( 'data',
                             'rc_classifier', 'classifier_model.h5')
    MASK_MODEL = os.path.join( 'data','mrcnn','mask_rcnn_latest.h5')
    MRCNN_DIR = os.path.join( 'data','mrcnn')
    CRAFT_MODEL = os.path.join('data','craft','recognizer_registrationtext.h5')
    CRAFT_ENCODER = os.path.join('data','craft','character_label_encoder.json')
    CRAFT_DECODER = os.path.join('data','craft','character_label_decoder.json')
