from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

# Create the uploads folder if it doesn't exist
os.makedirs('uploads', exist_ok=True)

def calculate_darkness(image_path):
    # Open the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    # Get the pixel values
    pixels = list(image.getdata())
    # Calculate the average brightness
    avg_brightness = sum(pixels) / len(pixels)
    # Darker images will have a lower average brightness value
    darkness_level = 255 - avg_brightness  # Invert to get darkness
    return darkness_level

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    feedback = ""
    
    if request.method == 'POST':
        file = request.files['image']
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)  # Save the uploaded image
            darkness_level = calculate_darkness(file_path)
            result = f"The measured darkness intensity is {darkness_level:.2f}."
            
            if darkness_level < 50:
                feedback = "It's quite bright."
            elif darkness_level < 150:
                feedback = "It's somewhat dark."
            else:
                feedback = "It's very dark!"

    return render_template('index.html', result=result, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
