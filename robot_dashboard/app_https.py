#!/usr/bin/env python3
"""
HTTPS Flask App for IP Address Camera Access with Gas Monitoring
Save this as: app_https.py

This provides HTTPS support for the robot dashboard to enable camera access
from IP addresses (required by modern browsers for getUserMedia API).
"""

from app import app
import ssl
import os
import sys

def create_self_signed_cert():
    """Create a self-signed certificate for HTTPS"""
    try:
        from OpenSSL import crypto
        import socket
        
        print("🔐 Creating self-signed SSL certificate...")
        
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
                                b"IP:172.20.10.2,DNS:localhost,IP:127.0.0.1,IP:0.0.0.0")
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
        print("💡 Install with: pip install pyOpenSSL")
        return False
    except Exception as e:
        print(f"❌ Certificate creation failed: {e}")
        return False

def install_pyopenssl():
    """Attempt to install PyOpenSSL automatically"""
    try:
        import subprocess
        import sys
        
        print("🔄 Attempting to install PyOpenSSL...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyOpenSSL"])
        print("✅ PyOpenSSL installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install PyOpenSSL: {e}")
        return False

def check_certificate_files():
    """Check if certificate files exist and are valid"""
    if not (os.path.exists('dashboard.crt') and os.path.exists('dashboard.key')):
        return False
    
    # Check if files are not empty
    try:
        with open('dashboard.crt', 'r') as f:
            cert_content = f.read()
        with open('dashboard.key', 'r') as f:
            key_content = f.read()
        
        if len(cert_content) < 100 or len(key_content) < 100:
            return False
        
        if not ('BEGIN CERTIFICATE' in cert_content and 'BEGIN PRIVATE KEY' in key_content):
            return False
        
        return True
    except Exception:
        return False

def run_https_server():
    """Run Flask app with HTTPS"""
    print("🚀 Starting HTTPS Robot Dashboard with Gas Monitoring...")
    print("=" * 60)
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
    print("💨 Gas Monitoring Features:")
    print("   📊 Real-time MQ2 combustible gas monitoring")
    print("   🌬️ Real-time MQ135 air quality monitoring")
    print("   🔬 Advanced gas analysis (Methane, LPG, Smoke, Hydrogen, Alcohol)")
    print("   📈 Historical gas level charts")
    print("   🚨 Automated gas hazard alerts")
    print("   📋 Comprehensive safety reports")
    print("   🆘 Emergency alert system")
    print("")
    print("🔬 Enhanced Features:")
    print("   🎯 High-precision GPS tracking")
    print("   📷 Live camera detection")
    print("   🗺️ Ultra-detail maps (building-level zoom)")
    print("   📊 Real-time sensor fusion")
    print("   📱 Mobile-responsive interface")
    print("")
    print("⚡ Press Ctrl+C to stop")
    print("=" * 60)
    
    ssl_context = None
    
    try:
        # Check if certificate files exist and are valid
        if check_certificate_files():
            print("📋 Using existing SSL certificate...")
            ssl_context = ('dashboard.crt', 'dashboard.key')
        else:
            print("📋 Creating new SSL certificate...")
            
            # Try to create certificate
            if create_self_signed_cert():
                ssl_context = ('dashboard.crt', 'dashboard.key')
            else:
                # Try to install PyOpenSSL and create certificate
                if install_pyopenssl():
                    if create_self_signed_cert():
                        ssl_context = ('dashboard.crt', 'dashboard.key')
                
                # If still no certificate, use Flask's built-in SSL
                if ssl_context is None:
                    print("⚠️ Using Flask's built-in SSL (less secure)")
                    ssl_context = 'adhoc'
        
        # Run with HTTPS
        print(f"🔒 Starting HTTPS server with SSL context: {ssl_context}")
        app.run(debug=True, host='0.0.0.0', port=5002, ssl_context=ssl_context, threaded=True)
        
    except Exception as e:
        print(f"❌ HTTPS startup failed: {e}")
        print("💡 Trying fallback options...")
        
        # Fallback 1: Try adhoc SSL
        try:
            print("🔄 Attempting with built-in SSL...")
            app.run(debug=True, host='0.0.0.0', port=5002, ssl_context='adhoc', threaded=True)
        except Exception as e2:
            print(f"❌ Built-in SSL failed: {e2}")
            
            # Fallback 2: HTTP with warning
            print("🔄 Falling back to HTTP server...")
            print("⚠️ WARNING: Camera features may not work on IP access")
            print("💡 For camera access, try:")
            print("   • Use localhost instead of IP address")
            print("   • Install PyOpenSSL: pip install pyOpenSSL")
            print("   • Use Chrome with --unsafely-treat-insecure-origin-as-secure flag")
            app.run(debug=True, host='0.0.0.0', port=5002, threaded=True)

def run_http_server():
    """Run Flask app with HTTP (fallback option)"""
    print("🚀 Starting HTTP Robot Dashboard with Gas Monitoring...")
    print("=" * 60)
    print("📍 HTTP Access URLs:")
    print("   🌐 Network: http://172.20.10.2:5002")
    print("   🏠 Local: http://localhost:5002")
    print("")
    print("⚠️ HTTP Mode Limitations:")
    print("   📹 Camera may not work on IP addresses")
    print("   🔒 Less secure than HTTPS")
    print("   💡 Use HTTPS mode for full functionality")
    print("")
    print("🤖 ESP32 Connection:")
    print("   📡 ESP32 HTTP: http://172.20.10.2:5002")
    print("")
    print("💨 Gas Monitoring Features:")
    print("   📊 Real-time MQ2 combustible gas monitoring")
    print("   🌬️ Real-time MQ135 air quality monitoring")
    print("   🔬 Advanced gas analysis (Methane, LPG, Smoke, Hydrogen, Alcohol)")
    print("   📈 Historical gas level charts")
    print("   🚨 Automated gas hazard alerts")
    print("   🆘 Emergency alert system")
    print("")
    print("🔬 Enhanced Features:")
    print("   🎯 High-precision GPS tracking")
    print("   📊 Real-time sensor fusion")
    print("   🗺️ Ultra-detail maps")
    print("   📱 Mobile-responsive interface")
    print("")
    print("⚡ Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5002, threaded=True)

def show_help():
    """Show help information"""
    print("🤖 Robot Dashboard with Enhanced Gas Monitoring")
    print("=" * 50)
    print("")
    print("Usage:")
    print("  python app_https.py [option]")
    print("")
    print("Options:")
    print("  https    Start HTTPS server (default)")
    print("  http     Start HTTP server")
    print("  cert     Create new SSL certificate")
    print("  help     Show this help")
    print("  status   Show system status")
    print("")
    print("Examples:")
    print("  python app_https.py          # Start HTTPS server")
    print("  python app_https.py https    # Start HTTPS server") 
    print("  python app_https.py http     # Start HTTP server")
    print("  python app_https.py cert     # Create certificate only")
    print("  python app_https.py status   # Check system status")
    print("")
    print("🔬 Enhanced Features:")
    print("  • Real-time robot tracking with ultra-precision GPS")
    print("  • Advanced human detection with AI-powered analysis")
    print("  • Multi-sensor gas monitoring (MQ2 + MQ135)")
    print("  • Specific gas detection (Methane, LPG, Smoke, Hydrogen, Alcohol)")
    print("  • Live camera with real-time detection")
    print("  • Interactive ultra-detail maps (building-level zoom)")
    print("  • Comprehensive gas hazard alerts")
    print("  • Emergency response system")
    print("  • Safety report generation")
    print("  • Mobile-responsive interface")
    print("")
    print("💨 Gas Monitoring Capabilities:")
    print("  • MQ2 Sensor: Combustible gases (LPG, Propane, Methane)")
    print("  • MQ135 Sensor: Air quality (CO2, NH3, NOx, Benzene)")
    print("  • Real-time PPM calculations for specific gases")
    print("  • Multi-level alert system (Safe → Caution → Danger → Critical)")
    print("  • Historical trending and pattern analysis")
    print("  • Automatic emergency notifications")
    print("")
    print("📋 Requirements:")
    print("  • Python 3.7+")
    print("  • Flask")
    print("  • PyOpenSSL (for HTTPS)")
    print("  • ESP32 with enhanced sensor package:")
    print("    - GPS module")
    print("    - MQ2 gas sensor")
    print("    - MQ135 air quality sensor")
    print("    - PIR motion sensor")
    print("    - MPU6050 accelerometer/gyroscope")
    print("    - SIM800L module (for emergency alerts)")
    print("")
    print("🌐 Network Setup:")
    print("  • ESP32 connects to WiFi network")
    print("  • Dashboard accessible via web browser")
    print("  • Mobile devices can access dashboard")
    print("  • Emergency SMS/call capabilities")

def create_certificate_only():
    """Create certificate without starting server"""
    print("🔐 Creating SSL certificate...")
    
    if create_self_signed_cert():
        print("✅ Certificate created successfully!")
        print("📄 Files created:")
        print("   • dashboard.crt (certificate)")
        print("   • dashboard.key (private key)")
        print("")
        print("🔒 Certificate Details:")
        print("   • Valid for: 1 year")
        print("   • Subject: CN=172.20.10.2")
        print("   • Alternative Names: localhost, 127.0.0.1, 0.0.0.0")
        print("   • Key Size: 2048-bit RSA")
        print("")
        print("💡 You can now run: python app_https.py https")
    else:
        print("❌ Certificate creation failed")
        print("💡 Try installing PyOpenSSL: pip install pyOpenSSL")

def show_system_status():
    """Show system status and diagnostics"""
    print("🔍 System Status and Diagnostics")
    print("=" * 40)
    print("")
    
    # Python version
    print(f"🐍 Python Version: {sys.version}")
    print("")
    
    # Check dependencies
    print("📦 Dependencies:")
    dependencies = [
        ('Flask', 'flask'),
        ('PyOpenSSL', 'OpenSSL'),
        ('Werkzeug', 'werkzeug'),
        ('SQLite3', 'sqlite3')
    ]
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"   ✅ {name}: Available")
        except ImportError:
            print(f"   ❌ {name}: Not available")
    
    print("")
    
    # Check files
    print("📁 Files:")
    files = [
        ('app.py', 'Main application'),
        ('database.py', 'Database module'),
        ('ai_inference.py', 'AI inference module'),
        ('templates/index.html', 'Dashboard template'),
        ('dashboard.crt', 'SSL certificate'),
        ('dashboard.key', 'SSL private key')
    ]
    
    for filename, description in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {filename}: {size} bytes ({description})")
        else:
            print(f"   ❌ {filename}: Missing ({description})")
    
    print("")
    
    # Check network
    print("🌐 Network Configuration:")
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"   🏠 Hostname: {hostname}")
        print(f"   📍 Local IP: {local_ip}")
        print(f"   🔗 Recommended URL: http://{local_ip}:5002")
    except Exception as e:
        print(f"   ❌ Network error: {e}")
    
    print("")
    
    # Check SSL certificate
    print("🔐 SSL Certificate:")
    if check_certificate_files():
        print("   ✅ Certificate files exist and are valid")
        try:
            with open('dashboard.crt', 'r') as f:
                cert_content = f.read()
            print(f"   📄 Certificate size: {len(cert_content)} bytes")
        except:
            pass
    else:
        print("   ❌ Certificate files missing or invalid")
        print("   💡 Run: python app_https.py cert")
    
    print("")
    
    # Performance recommendations
    print("⚡ Performance Recommendations:")
    print("   • Use HTTPS for camera functionality")
    print("   • Ensure ESP32 is on same network")
    print("   • Use modern browser (Chrome/Firefox/Safari)")
    print("   • Close other applications using camera")
    print("   • For production: use proper SSL certificate")

def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'help' or command == '--help' or command == '-h':
            show_help()
            return
        elif command == 'http':
            run_http_server()
            return
        elif command == 'https':
            run_https_server()
            return
        elif command == 'cert':
            create_certificate_only()
            return
        elif command == 'status':
            show_system_status()
            return
        else:
            print(f"❌ Unknown command: {command}")
            print("💡 Use 'python app_https.py help' for usage information")
            return
    
    # Default: run HTTPS server
    run_https_server()

if __name__ == '__main__':
    main()