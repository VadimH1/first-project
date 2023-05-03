import os
import json 
import jwt
from flask import Flask, Blueprint, request, render_template, session, jsonify, g
from flask import send_from_directory
from models import Upload
from schemas import UploadSchema
from db import db
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, BLOG_IMAGE_FOLDER, MEDIA_FOLDER, UPLOAD_EXTENSIONS
from uuid import uuid4
from .user_api import login_required
import datetime

upload_urls = Blueprint("upload", __name__)

@upload_urls.route('/api/v1/upload-files', methods=['POST'])
@login_required
def upload_file():
    uploaded_file = request.files['file']

    if not uploaded_file:
        return {"error_file_upload": "Not file"}, 400
    filename = secure_filename(f"{uploaded_file.filename}-{uuid4()}")

    file_ext = os.path.splitext(filename)[1]
    if file_ext not in UPLOAD_EXTENSIONS:
        return {"Error File_Extention": "Invalid file extension"}

    uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))

    url = f"{BLOG_IMAGE_FOLDER}/{filename}"
    author_id = g.user_id

    file = Upload(
        url=url,
        author_id=author_id
    )

    db.session.add(file)
    db.session.commit()
    return {
        "status":"Uploaded",
        "id": file.id
    }, 200



@upload_urls.route('/api/v1/delete-file/<int:image_id>', methods=['DELETE'])
@login_required
def delete_file(image_id):

    image = Upload.query.filter(Upload.id==image_id).one_or_none()

    if not image:
        return {"Error": "File not found"}, 400
    
    db.session.delete(image)
    db.session.commit()

    return {"Status": "File deleted"}, 200


@upload_urls.route('/media/<path:path>')
def download_image(path):
    return send_from_directory(MEDIA_FOLDER, path)