from flask import Flask, request, render_template
import easyocr, cv2, numpy as np
import base64, re
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/upload_webcam', methods=['POST'])
def upload_webcam():
    data_url = request.form['image_data']
    header, encoded = data_url.split(",", 1)
    binary_data = base64.b64decode(encoded)
 
    # Convert to image using numpy
    img_array = np.frombuffer(binary_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
 
    # OCR with easyocr
    reader = easyocr.Reader(['en'])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = reader.readtext(gray, detail=0)
 
    result_string = " ".join(result)
 
    total_match = re.search(r'Total\s+(\d+\.\d+)', result_string)
    cash_match = re.search(r'Cash\s+(\d+\.\d+)', result_string)
 
    total_amount = total_match.group(1) if total_match else "Not Found"
    cash_paid = cash_match.group(1) if cash_match else "Not Found"
 
    return render_template('index.html', result=result_string, total=total_amount, cash=cash_paid)
 
if __name__ == '__main__':
    app.run(debug=True)
 