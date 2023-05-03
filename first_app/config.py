import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'dev'
MEDIA_FOLDER = "media"
BLOG_IMAGE_FOLDER = 'media/blog_images'
UPLOAD_FOLDER = os.path.join(basedir, BLOG_IMAGE_FOLDER)
UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
