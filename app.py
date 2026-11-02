from flask import Flask, request, render_template, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry', methods=['POST'])
def capture_telemetry():
    # 1. Grab the real visitor IP from Cloudflare's header, fallback to standard proxy/remote IP
    client_ip = request.headers.get('CF-Connecting-IP') or request.headers.get('X-Forwarded-For') or request.remote_addr
    
    # 2. Grab browser/device user agent
    user_agent = request.headers.get('User-Agent')
    
    # 3. Grab extra data sent by frontend JavaScript
    payload = request.get_json() or {}
    
    visitor_log = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "ip_address": client_ip,
        "user_agent": user_agent,
        "screen_resolution": payload.get("screen"),
        "timezone": payload.get("timezone"),
        "language": payload.get("language")
    }
    
    # This prints live to your server logs whenever someone opens your site
    print("\n[NEW VISITOR CAPTURED]:", visitor_log)
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
