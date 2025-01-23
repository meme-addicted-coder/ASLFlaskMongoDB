from flask import Flask, request, jsonify
from pymongo import MongoClient
import base64
import io
from PIL import Image

app = Flask(__name__)

# Initialize MongoDB Client
client = MongoClient(mongodb+srv://Bhabnashre:mongodb@asl.148wj.mongodb.net/?retryWrites=true&w=majority&appName=asl) 
db = client[ASL]             
collection = db[Data]       

# Route for the home page
@app.route('/')
def home():
    return 'Home - Flask App for Saving Data'

# Route to handle uploads and save to MongoDB
@app.route('/upload', methods=['POST'])
def upload():
    # Check if files are provided
    if 'image' not in request.files or 'video' not in request.files or 'text' byst not in request.form:
        return jsonify({'error': 'Image, video, and text are required'}), 400
    
    # Get the files and text from the request
    image_file = request.files['image']
    video_file = request.files['video']
    text = request.form['text']
    
    # Encode image to base64
    image = Image.open(io.BytesIO(image_file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Encode video to base64
    video_str = base64.b64encode(video_file.read()).decode()
    
    # Store the data in MongoDB as JSON
    data = {
        'image': img_str,
        'video': video_str,
        'text': text
    }
    collection.insert_one(data)
    
    return jsonify({'message': 'Data uploaded successfully'})

# Route to retrieve data from MongoDB
@app.route('/retrieve/<data_id>', methods=['GET'])
def retrieve(data_id):
    from bson.objectid import ObjectId
    data = collection.find_one({'_id': ObjectId(data_id)})
    
    if not data:
        return jsonify({'error': 'Data not found'}), 404
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
