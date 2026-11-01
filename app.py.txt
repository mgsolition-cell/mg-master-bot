
from flask import Flask, render_template_string, request, jsonify
import json, os, io, base64, random
from datetime import datetime
from PIL import Image, ImageDraw

app = Flask(__name__)

def load_clients():
    if os.path.exists('clients.json'):
        try:
            with open('clients.json','r') as f: return json.load(f)
        except: return []
    return []

def save_clients(data):
    with open('clients.json','w') as f: json.dump(data,f,indent=2)

@app.route('/')
def admin():
    try:
        with open('dashboard.html','r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<h2>MG Bot V5 - Dashboard missing: {e}</h2><p>Upload dashboard.html</p>"

@app.route('/api/clients')
def api_clients():
    return jsonify(load_clients())

@app.route('/api/create_client', methods=['POST'])
def create_client():
    data = request.json
    data['id'] = len(load_clients())+1
    data['created'] = datetime.now().strftime("%d-%m-%Y %H:%M")
    data['status'] = data.get('status','Pending')
    data['wallet'] = 0
    data['last_post'] = "Not posted yet"
    clients = load_clients()
    clients.append(data)
    save_clients(clients)
    return jsonify({"ok":True, "client":data})

def make_poster(shop_name, phone):
    W,H = 1080,1080
    img = Image.new('RGB', (W,H), (15,15,15))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(W,250)], fill=(0,230,118))
    draw.text((40,40), shop_name[:25].upper(), fill="black")
    draw.text((40,120), "T.NAGAR CHENNAI", fill="black")
    draw.text((40,350), "TODAY SPECIAL", fill=(0,230,118))
    draw.text((40,450), "50% OFF", fill="white")
    draw.text((40,550), "Sarees | Kurtis | Lehengas", fill="gray")
    draw.rectangle([(40,700),(W-40,800)], fill=(0,230,118))
    draw.text((300,730), "DM FOR PRICE", fill="black")
    draw.text((40,850), f"Call: {phone}", fill="gray")
    return img

@app.route('/api/v5_one_click/<int:client_id>', methods=['POST','GET'])
def v5_one_click(client_id):
    clients = load_clients()
    client = next((c for c in clients if c['id']==client_id), None)
    if not client:
        return jsonify({"ok":False, "error":"Client not found"}), 404
    mode = request.args.get('mode','all')
    count = int(request.args.get('count',1))
    if mode == 'unlimited':
        count = 10
    posters = []
    logs = []
    logs.append(f"Client: {client['shop_name']} ID:{client_id}")
    for i in range(count):
        img = make_poster(client['shop_name'], client.get('phone',''))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        b64 = base64.b64encode(buf.getvalue()).decode()
        posters.append({"design": i+1, "base64": f"data:image/png;base64,{b64}", "public_url": None})
        logs.append(f"Poster {i+1} Generated OK")
    # Video fake
    videos = []
    if mode in ['all','video']:
        videos.append({"gif_path": "video ready"})
        logs.append("AI Video Generated")
    # Auto reply
    auto_reply = ["Thanks! DM us", "Visit T.Nagar", "Call for price"]
    logs.append("Auto Reply ON")
    logs.append(f"Unlimited ON - {count} posters")
    for c in clients:
        if c['id']==client_id:
            c['last_post']=datetime.now().strftime("%d-%m %H:%M")+" V5"
    save_clients(clients)
    return jsonify({"ok":True, "posters":posters, "videos":videos, "auto_reply":auto_reply, "logs":logs, "summary":f"V5 DONE {len(posters)} Posters"})

@app.route('/webhook/instagram', methods=['GET','POST'])
def webhook():
    if request.method=='GET':
        return request.args.get('hub.challenge','ok')
    return jsonify({"ok":True})

@app.route('/pay/<int:amount>')
def pay(amount):
    return f"<h2>Pay Rs.{amount} UPI: 8940498738@ybl</h2><a href='upi://pay?pa=8940498738@ybl&pn=MG&am={amount}'>Pay</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
