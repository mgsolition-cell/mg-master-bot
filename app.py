
from flask import Flask, render_template_string, request, jsonify, redirect
import json, os, qrcode, io, base64
from datetime import datetime

app = Flask(__name__)

# CONFIG - CHANGE HERE ONLY
UPI_ID = "8940498738@ybl"
BUSINESS_NAME = "MG Bot"
MONTHLY_AMOUNT = 1000

# Load clients
def load_clients():
    if os.path.exists('clients.json'):
        try:
            with open('clients.json','r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_clients(data):
    with open('clients.json','w') as f:
        json.dump(data,f,indent=2)

@app.route('/')
def admin():
    # Dashboard HTML
    with open('dashboard.html','r', encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html)

@app.route('/api/clients')
def api_clients():
    return jsonify(load_clients())

@app.route('/api/create_client', methods=['POST'])
def create_client():
    data = request.json
    data['id'] = len(load_clients())+1
    data['created'] = datetime.now().strftime("%d-%m-%Y")
    data['status'] = data.get('status','Pending')
    data['wallet'] = int(data.get('wallet',0))
    clients = load_clients()
    clients.append(data)
    save_clients(clients)
    return jsonify({"ok":True, "client":data})

@app.route('/api/update_status', methods=['POST'])
def update_status():
    req = request.json
    clients = load_clients()
    for c in clients:
        if c['id'] == req['id']:
            c['status'] = req['status']
            if 'wallet' in req:
                c['wallet'] = req['wallet']
    save_clients(clients)
    return jsonify({"ok":True})

@app.route('/pay/<int:amount>')
def pay_page(amount):
    upi_link = f"upi://pay?pa={UPI_ID}&pn={BUSINESS_NAME}&am={amount}&cu=INR&tn=Monthly {amount}"
    html = f"""
    <html><body style='font-family:sans-serif;text-align:center;padding:30px'>
    <h2>Pay Rs.{amount} to {BUSINESS_NAME}</h2>
    <p>UPI: {UPI_ID}</p>
    <a href="{upi_link}" style='display:inline-block;padding:15px 30px;background:#00c853;color:white;text-decoration:none;border-radius:10px;font-size:20px'>Pay Rs.{amount} via GPay/PhonePe</a>
    <br><br><p>Or Scan QR in Admin Panel</p>
    <p>After payment send screenshot to admin</p>
    </body></html>
    """
    return html

@app.route('/api/upi_qr/<int:amount>')
def upi_qr(amount):
    upi_link = f"upi://pay?pa={UPI_ID}&pn={BUSINESS_NAME}&am={amount}&cu=INR"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return jsonify({"qr": f"data:image/png;base64,{b64}", "link": upi_link})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
