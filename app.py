from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from rembg import remove 
from PIL import Image 
import io

app = Flask(__name__)
 
upload_folder = os.path.join('static', 'uploads')
 
app.config['UPLOAD'] = upload_folder
 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD'], filename)
        file.save(file_path)
        
        with open(file_path, 'rb') as f:
            img_data = f.read()
        
        processed_img_data = remove(img_data)
        processed_img = Image.open(io.BytesIO(processed_img_data)).convert('RGB')  # Convert to RGB mode
        processed_img.save(file_path, 'JPEG')  # Save as JPEG
        
        return render_template('image_render.html', img=file_path)
    
    return render_template('image_render.html')
 
if __name__ == '__main__':
    app.run(debug=True, port=8001)
