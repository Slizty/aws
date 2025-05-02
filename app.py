from flask import Flask, request, jsonify
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = "s3-upload-22025"
S3_REGION = "us-east-1"  # Change to your region

# Initialize S3 client
s3 = boto3.client(
    's3',
    region_name=S3_REGION
)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Secure the filename and upload to S3
    filename = secure_filename(file.filename)
    s3.upload_fileobj(file, S3_BUCKET, filename)

    # Generate a public download link (expires in 1 hour)
    download_link = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': filename},
        ExpiresIn=3600
    )

    return jsonify({"downloadLink": download_link})
#dd