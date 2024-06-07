from flask import Flask, render_template, request
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

app = Flask(__name__)

def generate_aamva_data(data):
    aamva_data = (
        "@\n"
        "ANSI 6360010101DL00410282ZV03190015DLDAAD\r"
        f"DCSS{data['last_name']}\r"
        f"DAC{data['first_name']}\r"
        f"DAD{data['middle_name']}\r"
        f"DBB{data['date_of_birth']}\r"
        f"DAY{data['eye_color']}\r"
        f"DBC{data['sex']}\r"
        f"DBD{data['issue_date']}\r"
        f"DBA{data['expiration_date']}\r"
        f"DAG{data['street_address']}\r"
        f"DAI{data['city']}\r"
        f"DAJ{data['state']}\r"
        f"DAK{data['zip_code']}\r"
        f"DAQ{data['license_number']}\r"
        f"DAU{data['height']}\r"
        f"DAW{data['weight']}\r"
    )
    return aamva_data

def generate_pdf417_barcode(aamva_data):
    # Generate PDF417 barcode
    pdf417 = barcode.get_barcode_class('pdf417')
    pdf417_barcode = pdf417(aamva_data, writer=ImageWriter())
    
    # Save barcode to BytesIO object
    buffer = BytesIO()
    pdf417_barcode.write(buffer)
    buffer.seek(0)
    
    return buffer

@app.route('/', methods=['GET', 'POST'])
def index():
    barcode_image = None
    if request.method == 'POST':
        # Collect form data
        form_data = {
            "last_name": request.form['last_name'],
            "first_name": request.form['first_name'],
            "middle_name": request.form['middle_name'],
            "date_of_birth": request.form['date_of_birth'],
            "eye_color": request.form['eye_color'],
            "sex": request.form['sex'],
            "issue_date": request.form['issue_date'],
            "expiration_date": request.form['expiration_date'],
            "street_address": request.form['street_address'],
            "city": request.form['city'],
            "state": request.form['state'],
            "zip_code": request.form['zip_code'],
            "license_number": request.form['license_number'],
            "height": request.form['height'],
            "weight": request.form['weight']
        }

        # Generate AAMVA formatted data
        aamva_data = generate_aamva_data(form_data)
        
        # Generate PDF417 barcode
        barcode_buffer = generate_pdf417_barcode(aamva_data)
        
        # Encode barcode image to base64
        barcode_image = base64.b64encode(barcode_buffer.read()).decode('utf-8')
    
    return render_template('index.html', barcode_image=barcode_image)

if __name__ == '__main__':
    app.run(debug=True)

