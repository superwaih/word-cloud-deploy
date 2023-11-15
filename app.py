from flask import Flask, render_template, request, send_file
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

stopwords = set(STOPWORDS)
stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

@cache.memoize(timeout=3600)  # Cache timeout in seconds (1 hour in this example)
def generate_wordcloud(wine_mask_np, text_input):
    # Your existing word cloud generation code here
    # ...

    wc.generate(text_input.upper())

    img_buffer = BytesIO()
    wc.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud_route():
    if 'wine_mask' not in request.files:
        return "No wine mask provided."

    wine_mask = request.files['wine_mask']
    wine_mask_np = np.array(Image.open(wine_mask))

    text_input = request.form.get('text_input', '')

    img_buffer = generate_wordcloud(wine_mask_np, text_input)

    return send_file(img_buffer, mimetype='image/png', as_attachment=True, download_name='wordcloud.png')

if __name__ == '__main__':
    app.run(debug=True)
