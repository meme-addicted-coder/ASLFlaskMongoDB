from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import base64
import io
from PIL import Image
from bson.objectid import ObjectId

app = Flask(__name__)

# Initialize MongoDB Client with your URI
client = MongoClient("mongodb+srv://Bhabnashre:mongodb@asl.148wj.mongodb.net/?retryWrites=true&w=majority&appName=asl")
db = client['ASL']
collection = db['Data']

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle uploads and save to MongoDB
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files
    text = request.form.get('text')
    
    # Get image file and encode to base64
    image_file = files.get('image')
    image = Image.open(io.BytesIO(image_file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode() if image_file else None
    
    # Get video file and encode to base64
    video_file = files.get('video')
    video_str = base64.b64encode(video_file.read()).decode() if video_file else None
    
    # Store the data in MongoDB as JSON
    data = {
        'image': img_str,
        'video': video_str,
        'text': text
    }
    collection.insert_one(data)
    
    return jsonify({'message': 'Data uploaded successfully'})

@app.route('/retrieve', methods=['GET'])
def retrieve():
    data_list = list(collection.find())
    
    for data in data_list:
        data['_id'] = str(data['_id'])  # Convert ObjectId to string

    return render_template('retrieve.html', data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True , port =5002)

