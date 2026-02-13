#!/usr/bin/env python3
# HTTPS Flask App for IP Address Camera Access
# Save this as: app_https.py

from app import app
import ssl
import os

def create_self_signed_cert():
    """Create a self-signed certificate for HTTPS"""
    try:
        from OpenSSL import crypto
        import socket
        
        # Create certificate and key
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)
        
        cert = crypto.X509()
        cert.get_subject().C = "LK"
        cert.get_subject().ST = "Western"
        cert.get_subject().L = "Negombo"
        cert.get_subject().O = "Robot Dashboard"
        cert.get_subject().OU = "AI Research"
        cert.get_subject().CN = "172.20.10.2"
        
        # Add Subject Alternative Names for different access methods
        cert.add_extensions([
            crypto.X509Extension(b"subjectAltName", False, 
                                b"IP:172.20.10.2,DNS:localhost,IP:127.0.0.1")
        ])
        
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)  # Valid for 1 year
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, 'sha256')
        
        # Save certificate and key
        with open('dashboard.crt', 'wb') as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            
        with open('dashboard.key', 'wb') as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
            
        print("✅ Self-signed certificate created: dashboard.crt, dashboard.key")
        return True
        
    except ImportError:
        print("❌ PyOpenSSL not available for certificate generation")
        return False
    except Exception as e:
        print(f"❌ Certificate creation failed: {e}")
        return False

def run_https_server():
    """Run Flask app with HTTPS"""
    print("🔒 Starting HTTPS Robot Dashboard...")
    print("📍 HTTPS Access URLs:")
    print("   🌐 Network: https://172.20.10.2:5002")
    print("   🏠 Local: https://localhost:5002")
    print("   📱 Mobile: https://172.20.10.2:5002")
    print("")
    print("🔐 Certificate Info:")
    print("   📄 Self-signed certificate (browser will show warning)")
    print("   🔓 Click 'Advanced' → 'Proceed to 172.20.10.2 (unsafe)'")
    print("   📹 Camera will work after accepting certificate")
    print("")
    print("🤖 ESP32 Connection:")
    print("   📡 ESP32 can still use HTTP: http://172.20.10.2:5002")
    print("   🔧 Or update ESP32 to HTTPS: https://172.20.10.2:5002")
    print("")
    print("⚡ Press Ctrl+C to stop")
    
    try:
        # Try to create certificate if it doesn't exist
        if not (os.path.exists('dashboard.crt') and os.path.exists('dashboard.key')):
            print("📋 Creating SSL certificate...")
            if not create_self_signed_cert():
                print("⚠️ Using Flask's built-in SSL (less secure)")
                ssl_context = 'adhoc'
            else:
                ssl_context = ('dashboard.crt', 'dashboard.key')
        else:
            print("📋 Using existing SSL certificate...")
            ssl_context = ('dashboard.crt', 'dashboard.key')
        
        # Run with HTTPS
        app.run(debug=True, host='0.0.0.0', port=5002, ssl_context=ssl_context)
        
    except Exception as e:
        print(f"❌ HTTPS startup failed: {e}")
        print("💡 Trying fallback options...")
        
        # Fallback to adhoc SSL
        try:
            print("🔄 Attempting with built-in SSL...")
            app.run(debug=True, host='0.0.0.0', port=5002, ssl_context='adhoc')
        except Exception as e2:
            print(f"❌ All HTTPS options failed: {e2}")
            print("📍 Starting HTTP server (camera won't work on IP access)")
            app.run(debug=True, host='0.0.0.0', port=5002)

if __name__ == '__main__':
    run_https_server()