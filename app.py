from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)
def compress_image_to_size(input_image_path, output_image_path, target_size_kb):
    target_size = target_size_kb * 1024  # Convert KB to bytes
    quality = 95  # Start with high quality
    step = 5  # Quality step to reduce
    max_iterations = 20  # Limit the number of iterations

    # Open the image
    img = Image.open(input_image_path)

    # Binary search for the best quality
    for _ in range(max_iterations):
        # Save the image with the current quality setting
        img.save(output_image_path, quality=quality)

        # Check the file size
        file_size = os.path.getsize(output_image_path)

        if file_size <= target_size:
            return True  # Success
        else:
            quality -= step  # Reduce the quality

        if quality <= 10:  # Ensure quality does not go below 10
            break

    # If quality steps are insufficient, resize the image
    width, height = img.size
    while file_size > target_size and width > 10 and height > 10:
        width = int(width * 0.9)
        height = int(height * 0.9)
        img = img.resize((width, height), Image.ANTIALIAS)
        img.save(output_image_path, quality=quality)
        file_size = os.path.getsize(output_image_path)

    return os.path.getsize(output_image_path) <= target_size

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    target_size_kb = int(request.form.get('target_size_kb', 100))  # Default to 100 KB if not provided

    input_image_path = os.path.join('uploads', image.filename)
    output_image_path = os.path.join('compressed', image.filename)

    os.makedirs('uploads', exist_ok=True)
    os.makedirs('compressed', exist_ok=True)

    image.save(input_image_path)

    success = compress_image_to_size(input_image_path, output_image_path, target_size_kb)

    if success:
        return jsonify({"message": "Image compressed successfully", "compressed_image_path": output_image_path}), 200
    else:
        return jsonify({"error": "Failed to compress image"}), 500

if __name__ == '__main__':
    app.run(debug=True)