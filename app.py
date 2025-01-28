from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    artwork = request.files['artwork']
    img = Image.open(artwork).convert("RGBA")
    urls = [request.form[f'url{i+1}'] for i in range(4) if request.form[f'url{i+1}']]
    positions = [(int(request.form[f'x{i+1}']), int(request.form[f'y{i+1}'])) for i in range(len(urls))]

    for url, (x, y) in zip(urls, positions):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white').convert("RGBA")
        qr_img = qr_img.resize((100, 100))
        img.paste(qr_img, (x, y), qr_img)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)