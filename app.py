# from flask import Flask, request, jsonify, send_file
# from PIL import Image
# import os
# from flask_cors import CORS
# import io

# app = Flask(__name__)
# CORS(app)

# def compress_image_to_size(image, target_size_kb):
#     target_size = target_size_kb * 1024  # Convert KB to bytes
#     quality = 95
#     step = 5
#     max_iterations = 20

#     # Convert to RGB mode if the image is in RGBA
#     if image.mode == 'RGBA':
#         image = image.convert('RGB')

#     # Create a BytesIO object to hold the image data
#     img_byte_arr = io.BytesIO()

#     for _ in range(max_iterations):
#         # Save the image with the current quality setting
#         image.save(img_byte_arr, format='JPEG', optimize=True, quality=quality)
        
#         # Get the current file size
#         file_size = img_byte_arr.tell()
        
#         if file_size <= target_size:
#             return img_byte_arr.getvalue()
#         else:
#             quality -= step
#             img_byte_arr.seek(0)
#             img_byte_arr.truncate()

#         if quality <= 10:
#             break

#     # If quality reduction is not enough, resize the image
#     while file_size > target_size and image.width > 10 and image.height > 10:
#         image = image.resize((int(image.width * 0.9), int(image.height * 0.9)), Image.LANCZOS)
#         img_byte_arr.seek(0)
#         img_byte_arr.truncate()
#         image.save(img_byte_arr, format='JPEG', optimize=True, quality=quality)
#         file_size = img_byte_arr.tell()

#     return img_byte_arr.getvalue()

# @app.route('/compress', methods=['POST'])
# def compress_image():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400

#     image = request.files['image']
#     target_size_kb = int(request.form.get('target_size_kb', 100))  # Default to 100 KB if not provided

#     try:
#         # Open the image using Pillow
#         img = Image.open(image.stream)
        
#         # Compress the image
#         compressed_image_data = compress_image_to_size(img, target_size_kb)
        
#         # Create a BytesIO object from the compressed image data
#         img_io = io.BytesIO(compressed_image_data)
#         img_io.seek(0)
        
#         # Return the compressed image as a file response
#         return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='compressed_image.jpg')
    
#     except Exception as e:
#         return jsonify({"error": f"There was an error compressing the image: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/compress": {"origins": "http://localhost:3000"}})  # Allow requests from Next.js dev server

def compress_image_to_size(image, target_size_kb):
    target_size = target_size_kb * 1024  # Convert KB to bytes
    quality = 95
    step = 5
    max_iterations = 20

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    img_byte_arr = io.BytesIO()

    for _ in range(max_iterations):
        image.save(img_byte_arr, format='JPEG', optimize=True, quality=quality)
        file_size = img_byte_arr.tell()
        
        if file_size <= target_size:
            return img_byte_arr.getvalue()
        else:
            quality -= step
            img_byte_arr.seek(0)
            img_byte_arr.truncate()

        if quality <= 10:
            break

    while file_size > target_size and image.width > 10 and image.height > 10:
        image = image.resize((int(image.width * 0.9), int(image.height * 0.9)), Image.LANCZOS)
        img_byte_arr.seek(0)
        img_byte_arr.truncate()
        image.save(img_byte_arr, format='JPEG', optimize=True, quality=quality)
        file_size = img_byte_arr.tell()

    return img_byte_arr.getvalue()

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return {"error": "No image file provided"}, 400

    image = request.files['image']
    target_size_kb = int(request.form.get('target_size_kb', 100))

    try:
        img = Image.open(image.stream)
        compressed_image_data = compress_image_to_size(img, target_size_kb)
        
        img_io = io.BytesIO(compressed_image_data)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='compressed_image.jpg')
    
    except Exception as e:
        return {"error": f"There was an error compressing the image: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)