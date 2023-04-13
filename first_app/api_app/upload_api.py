import os
import json 
import jwt
from flask import Flask, Blueprint, request, render_template, session, jsonify, g
from models import Upload
from schemas import UploadSchema
from db import db
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
import datetime

upload_urls = Blueprint("upload", __name__)


@upload_urls.route('/api/v1/upload-files', methods=['POST'])
def upload_files():
    uploaded_files = request.files['file']

    if uploaded_files.filename != '':
        uploaded_files.save(secure_filename(uploaded_files.filename))

    path_to_file = uploaded_files.save(os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_files.filename)))    
    upload = Upload(url = uploaded_files.filename)
    db.session.add(upload)
    db.session.commit()

    upload_schema = UploadSchema()
    return jsonify(upload_schema.dump(upload))