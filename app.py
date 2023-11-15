from flask import Flask, render_template, request, send_file
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
import concurrent.futures

app = Flask(__name__)

stopwords = set(STOPWORDS)
stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

def transform_format(val):
    return 255 if val != 0 else val

def one_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h, s, l = 0, 0, 0
    return "hsl({}, {}%, {}%)".format(h, s, l)

def generate_wordcloud_async(text_input, wine_mask):
    wine_mask_np = np.array(Image.open(wine_mask))
    vectorized_transform_format = np.vectorize(transform_format)
    transformed_wine_mask = vectorized_transform_format(wine_mask_np)

    wc = WordCloud(
        background_color="white",
        mask=transformed_wine_mask,
        stopwords=stopwords,
        max_words=200,
        repeat=True,
        color_func=one_color_func
    )

    wc.generate(text_input.upper())

    # Save the word cloud image to a BytesIO object
    img_buffer = BytesIO()
    wc.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    if 'wine_mask' not in request.files:
        return "No wine mask provided."

    wine_mask = request.files['wine_mask']
    text_input = request.form.get('text_input', '')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run the image generation task asynchronously
        img_future = executor.submit(generate_wordcloud_async, text_input, wine_mask)
        img_buffer = img_future.result()

    return send_file(img_buffer, mimetype='image/png', as_attachment=True, download_name='wordcloud.png')

if __name__ == '__main__':
    app.run(debug=True)
