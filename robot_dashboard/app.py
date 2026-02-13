from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import random
from werkzeug.utils import secure_filename
from database import RobotDatabase
from ai_inference import AIInference

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

# Initialize database and AI inference
db = RobotDatabase()
ai = AIInference()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/receive-robot-data', methods=['POST'])
def receive_robot_data():
    """Receive real robot data from ESP32 with enhanced gas monitoring"""
    try:
        data = request.get_json()
        print(f"🤖 Received robot data: {data}")  # Debug print
        
        # Create comprehensive data dictionary with all ESP32 fields
        robot_data = {
            # Basic location and sensors
            'latitude': float(data.get('latitude', 0.0)),
            'longitude': float(data.get('longitude', 0.0)),
            'front_distance': float(data.get('front_distance', 0.0)),
            'back_distance': float(data.get('back_distance', 0.0)),
            'motion_detected': bool(data.get('motion_detected', False)),
            'battery_level': float(data.get('battery_level', 0.0)),
            'status': str(data.get('status', 'Unknown')),
            
            # Enhanced GPS data
            'gps_valid': bool(data.get('gps_valid', False)),
            'satellites': int(data.get('satellites', 0)),
            'altitude': float(data.get('altitude', 0.0)),
            'speed': float(data.get('speed', 0.0)),
            'heading': float(data.get('heading', 0.0)),
            
            # Gas sensor data (NEW)
            'mq2_gas_level': float(data.get('mq2_analog', 0.0)),
            'mq2_gas_detected': bool(data.get('mq2_digital', False)),
            'mq135_air_quality': float(data.get('mq135_reading', 0.0)),
            'mq135_alert_detected': bool(data.get('mq135_reading', 0.0) > 500),
            
            # Environmental sensors
            'temperature': float(data.get('temperature', 0.0)),
            'orientation': float(data.get('orientation', 0.0)),
            'is_stable': bool(data.get('is_stable', True)),
            'sound_detected': bool(data.get('sound_detected', False)),
            
            # Movement tracking
            'distance_traveled': float(data.get('distance_traveled', 0.0)),
            'search_pattern': int(data.get('search_pattern', 0)),
            'system_healthy': bool(data.get('system_healthy', True)),
            'current_state': str(data.get('current_state', 'Unknown')),
            
            # Advanced gas analysis (from ESP32)
            'methane_ppm': float(data.get('methane_ppm', 0.0)),
            'hydrogen_ppm': float(data.get('hydrogen_ppm', 0.0)),
            'lpg_ppm': float(data.get('lpg_ppm', 0.0)),
            'smoke_ppm': float(data.get('smoke_ppm', 0.0)),
            'alcohol_ppm': float(data.get('alcohol_ppm', 0.0)),
            'mq2_resistance': float(data.get('mq2_resistance', 0.0)),
            'emergency_mode': bool(data.get('emergency_mode', False))
        }
        
        # Add to database using new comprehensive method
        db.add_robot_data(robot_data)
        
        # Enhanced detection logging
        if robot_data['motion_detected']:
            print(f"⚠️ Motion detected at {robot_data['latitude']}, {robot_data['longitude']}")
            db.add_detection('motion', 0.8, robot_data['latitude'], robot_data['longitude'], '', [])
        
        # Gas hazard detection and logging
        gas_alerts = []
        
        # MQ2 (Combustible gas) alerts
        if robot_data['mq2_gas_level'] > 70 or robot_data['mq2_gas_detected']:
            print(f"🔥 FIRE RISK: MQ2 gas level at {robot_data['mq2_gas_level']}%")
            db.add_detection('gas_fire_risk', robot_data['mq2_gas_level']/100, 
                           robot_data['latitude'], robot_data['longitude'], '', [])
            gas_alerts.append('FIRE_RISK')
        elif robot_data['mq2_gas_level'] > 50:
            print(f"⚠️ High combustible gas: MQ2 at {robot_data['mq2_gas_level']}%")
            gas_alerts.append('HIGH_GAS')
        
        # MQ135 (Air quality) alerts
        if robot_data['mq135_air_quality'] > 350 or robot_data['mq135_alert_detected']:
            print(f"☠️ TOXIC AIR: MQ135 air quality at {robot_data['mq135_air_quality']}ppm")
            db.add_detection('toxic_air', robot_data['mq135_air_quality']/500, 
                           robot_data['latitude'], robot_data['longitude'], '', [])
            gas_alerts.append('TOXIC_AIR')
        elif robot_data['mq135_air_quality'] > 250:
            print(f"⚠️ Poor air quality: MQ135 at {robot_data['mq135_air_quality']}ppm")
            gas_alerts.append('POOR_AIR')
        
        # Specific gas alerts (from advanced ESP32 analysis)
        if robot_data['methane_ppm'] > 1000:
            print(f"🔥 METHANE ALERT: {robot_data['methane_ppm']} ppm detected!")
            gas_alerts.append('METHANE_HIGH')
        
        if robot_data['lpg_ppm'] > 500:
            print(f"🔥 LPG ALERT: {robot_data['lpg_ppm']} ppm detected!")
            gas_alerts.append('LPG_HIGH')
        
        if robot_data['smoke_ppm'] > 500:
            print(f"🔥 SMOKE ALERT: {robot_data['smoke_ppm']} ppm detected!")
            gas_alerts.append('SMOKE_HIGH')
        
        # System health alerts
        if not robot_data['system_healthy']:
            print(f"🚨 System health issues detected")
            gas_alerts.append('SYSTEM_FAILURE')
        
        # Emergency mode alert
        if robot_data['emergency_mode']:
            print(f"🚨 EMERGENCY MODE ACTIVATED")
            gas_alerts.append('EMERGENCY_ACTIVE')
        
        response_data = {
            'message': 'Enhanced data received successfully',
            'status': 'ok',
            'received_at': datetime.now().isoformat(),
            'gas_alerts': gas_alerts,
            'processed_fields': len(robot_data),
            'emergency_status': robot_data['emergency_mode']
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error processing robot data: {e}")
        return jsonify({'error': f'Error processing data: {e}'}), 400

@app.route('/api/robot-data')
def get_robot_data():
    """Get recent robot data with enhanced fields"""
    data = db.get_recent_data(50)
    
    # Convert to JSON format with all fields
    robot_data = []
    for row in data:
        # Handle different database schema versions
        try:
            data_dict = {
                'id': row[0],
                'timestamp': row[1],
                'latitude': row[2],
                'longitude': row[3],
                'front_distance': row[4],
                'back_distance': row[5],
                'motion_detected': row[6],
                'battery_level': row[7],
                'status': row[8],
                'last_updated': datetime.now().isoformat()
            }
            
            # Add new fields if they exist in the database
            if len(row) > 9:
                data_dict.update({
                    'gps_valid': row[9] if len(row) > 9 else False,
                    'satellites': row[10] if len(row) > 10 else 0,
                    'altitude': row[11] if len(row) > 11 else 0.0,
                    'speed': row[12] if len(row) > 12 else 0.0,
                    'heading': row[13] if len(row) > 13 else 0.0,
                    'mq2_gas_level': row[14] if len(row) > 14 else 0.0,
                    'mq2_gas_detected': row[15] if len(row) > 15 else False,
                    'mq135_air_quality': row[16] if len(row) > 16 else 0.0,
                    'mq135_alert_detected': row[17] if len(row) > 17 else False,
                    'temperature': row[18] if len(row) > 18 else 0.0,
                    'orientation': row[19] if len(row) > 19 else 0.0,
                    'is_stable': row[20] if len(row) > 20 else True,
                    'sound_detected': row[21] if len(row) > 21 else False,
                    'distance_traveled': row[22] if len(row) > 22 else 0.0,
                    'search_pattern': row[23] if len(row) > 23 else 0,
                    'system_healthy': row[24] if len(row) > 24 else True,
                    'current_state': row[25] if len(row) > 25 else 'Unknown',
                    'methane_ppm': row[26] if len(row) > 26 else 0.0,
                    'hydrogen_ppm': row[27] if len(row) > 27 else 0.0,
                    'lpg_ppm': row[28] if len(row) > 28 else 0.0,
                    'smoke_ppm': row[29] if len(row) > 29 else 0.0,
                    'alcohol_ppm': row[30] if len(row) > 30 else 0.0,
                    'mq2_resistance': row[31] if len(row) > 31 else 0.0,
                    'emergency_mode': row[32] if len(row) > 32 else False
                })
            
            robot_data.append(data_dict)
            
        except Exception as e:
            print(f"Warning: Error processing row {row[0]}: {e}")
            # Add basic data for compatibility
            robot_data.append({
                'id': row[0],
                'timestamp': row[1],
                'latitude': row[2] if len(row) > 2 else 0.0,
                'longitude': row[3] if len(row) > 3 else 0.0,
                'front_distance': row[4] if len(row) > 4 else 0.0,
                'back_distance': row[5] if len(row) > 5 else 0.0,
                'motion_detected': row[6] if len(row) > 6 else False,
                'battery_level': row[7] if len(row) > 7 else 0.0,
                'status': row[8] if len(row) > 8 else 'Unknown',
                'mq2_gas_level': 0.0,
                'mq135_air_quality': 0.0,
                'methane_ppm': 0.0,
                'lpg_ppm': 0.0,
                'smoke_ppm': 0.0,
                'emergency_mode': False,
                'last_updated': datetime.now().isoformat()
            })
    
    return jsonify(robot_data)

@app.route('/api/gas-data')
def get_gas_data():
    """Get recent gas monitoring data"""
    gas_history = db.get_gas_history(100, 24)  # Last 24 hours
    
    # Convert to JSON format
    gas_data = []
    for row in gas_history:
        gas_data.append({
            'id': row[0],
            'timestamp': row[1],
            'mq2_level': row[2],
            'mq135_level': row[3],
            'latitude': row[4],
            'longitude': row[5],
            'alert_triggered': row[6],
            'alert_type': row[7],
            'methane_ppm': row[8] if len(row) > 8 else 0.0,
            'hydrogen_ppm': row[9] if len(row) > 9 else 0.0,
            'lpg_ppm': row[10] if len(row) > 10 else 0.0,
            'smoke_ppm': row[11] if len(row) > 11 else 0.0,
            'alcohol_ppm': row[12] if len(row) > 12 else 0.0
        })
    
    return jsonify(gas_data)

@app.route('/api/gas-alerts')
def get_gas_alerts():
    """Get recent gas alerts"""
    alerts = db.get_gas_alerts(20)
    
    # Convert to JSON format
    alert_data = []
    for row in alerts:
        alert_data.append({
            'id': row[0],
            'timestamp': row[1],
            'mq2_level': row[2],
            'mq135_level': row[3],
            'latitude': row[4],
            'longitude': row[5],
            'alert_type': row[7],
            'methane_ppm': row[8] if len(row) > 8 else 0.0,
            'lpg_ppm': row[10] if len(row) > 10 else 0.0,
            'smoke_ppm': row[11] if len(row) > 11 else 0.0
        })
    
    return jsonify(alert_data)

@app.route('/api/emergency-alerts')
def get_emergency_alerts():
    """Get emergency alerts"""
    acknowledged = request.args.get('acknowledged')
    limit = int(request.args.get('limit', 10))
    
    if acknowledged is not None:
        acknowledged = acknowledged.lower() == 'true'
    
    alerts = db.get_emergency_alerts(limit, acknowledged)
    
    alert_data = []
    for row in alerts:
        alert_data.append({
            'id': row[0],
            'timestamp': row[1],
            'alert_type': row[2],
            'severity': row[3],
            'message': row[4],
            'latitude': row[5],
            'longitude': row[6],
            'acknowledged': row[7],
            'response_time': row[8]
        })
    
    return jsonify(alert_data)

@app.route('/api/acknowledge-alert/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an emergency alert"""
    try:
        db.acknowledge_alert(alert_id)
        return jsonify({'message': 'Alert acknowledged successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to acknowledge alert: {e}'}), 500

@app.route('/api/gas-analysis', methods=['POST'])
def analyze_gas_levels():
    """Analyze gas levels using AI"""
    try:
        data = request.get_json()
        mq2_level = float(data.get('mq2_level', 0))
        mq135_level = float(data.get('mq135_level', 0))
        
        analysis = ai.analyze_gas_levels(mq2_level, mq135_level)
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': f'Gas analysis error: {e}'}), 400

@app.route('/api/safety-report')
def generate_safety_report():
    """Generate comprehensive safety report"""
    try:
        robot_data = db.get_recent_data(10)
        gas_history = db.get_gas_history(50, 24)
        
        report = ai.generate_safety_report(robot_data, gas_history)
        return jsonify(report)
        
    except Exception as e:
        return jsonify({'error': f'Report generation error: {e}'}), 500

@app.route('/api/detections')
def get_detections():
    """Get recent detection data"""
    data = db.get_recent_detections(30)
    
    # Convert to JSON format
    detections = []
    for row in data:
        detections.append({
            'id': row[0],
            'timestamp': row[1],
            'detection_type': row[2],
            'confidence': row[3],
            'latitude': row[4],
            'longitude': row[5],
            'file_path': row[6],
            'bbox_data': json.loads(row[7]) if row[7] else None
        })
    
    return jsonify(detections)

@app.route('/api/upload-history')
def get_upload_history():
    """Get upload history"""
    data = db.get_upload_history(20)
    
    # Convert to JSON format
    history = []
    for row in data:
        history.append({
            'id': row[0],
            'timestamp': row[1],
            'file_name': row[2],
            'file_type': row[3],
            'detection_result': row[4],
            'confidence': row[5]
        })
    
    return jsonify(history)

@app.route('/api/map')
def get_map():
    """Generate enhanced map data with gas monitoring"""
    data = db.get_recent_data(10)
    
    # Return JSON data for map
    map_data = {
        'robot_locations': [],
        'detections': [],
        'gas_alerts': [],
        'emergency_alerts': [],
        'center': [6.0329, 80.2168]  # Default Negombo location
    }
    
    # Add robot locations with gas data
    for row in data:
        if row[2] and row[3]:  # Check if lat/lon exist
            location_data = {
                'lat': row[2],
                'lng': row[3],
                'timestamp': row[1],
                'battery': row[7],
                'status': row[8],
                'motion': row[6]
            }
            
            # Add gas data if available
            if len(row) > 14:
                location_data.update({
                    'mq2_gas_level': row[14] if len(row) > 14 else 0.0,
                    'mq2_gas_detected': row[15] if len(row) > 15 else False,
                    'mq135_air_quality': row[16] if len(row) > 16 else 0.0,
                    'mq135_alert_detected': row[17] if len(row) > 17 else False,
                    'system_healthy': row[24] if len(row) > 24 else True,
                    'methane_ppm': row[26] if len(row) > 26 else 0.0,
                    'lpg_ppm': row[28] if len(row) > 28 else 0.0,
                    'smoke_ppm': row[29] if len(row) > 29 else 0.0,
                    'emergency_mode': row[32] if len(row) > 32 else False
                })
            
            map_data['robot_locations'].append(location_data)
    
    # Add detection locations
    detections = db.get_recent_detections(10)
    for detection in detections:
        if detection[4] and detection[5]:  # Check if lat/lon exist
            map_data['detections'].append({
                'lat': detection[4],
                'lng': detection[5],
                'type': detection[2],
                'confidence': detection[3],
                'timestamp': detection[1]
            })
    
    # Add gas alerts
    gas_alerts = db.get_gas_alerts(5)
    for alert in gas_alerts:
        if alert[4] and alert[5]:  # Check if lat/lon exist
            map_data['gas_alerts'].append({
                'lat': alert[4],
                'lng': alert[5],
                'mq2_level': alert[2],
                'mq135_level': alert[3],
                'alert_type': alert[7],
                'timestamp': alert[1]
            })
    
    # Add emergency alerts
    emergency_alerts = db.get_emergency_alerts(5, False)  # Unacknowledged alerts
    for alert in emergency_alerts:
        if alert[5] and alert[6]:  # Check if lat/lon exist
            map_data['emergency_alerts'].append({
                'lat': alert[5],
                'lng': alert[6],
                'alert_type': alert[2],
                'severity': alert[3],
                'message': alert[4],
                'timestamp': alert[1]
            })
    
    # Calculate center from available data
    if map_data['robot_locations']:
        avg_lat = sum([loc['lat'] for loc in map_data['robot_locations']]) / len(map_data['robot_locations'])
        avg_lng = sum([loc['lng'] for loc in map_data['robot_locations']]) / len(map_data['robot_locations'])
        map_data['center'] = [avg_lat, avg_lng]
    
    return jsonify(map_data)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and run inference"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    file_type = request.form.get('type', 'auto')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Determine file type if auto
        if file_type == 'auto':
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_type = 'visual'
            elif filename.lower().endswith(('.wav', '.mp3', '.flac')):
                file_type = 'audio'
        
        # Run inference based on file type
        result = None
        if file_type == 'thermal':
            result = ai.detect_thermal_human(filepath)
        elif file_type == 'visual':
            result = ai.detect_visual_human(filepath)
        elif file_type == 'audio':
            result = ai.detect_voice_human(filepath)
        
        # Save to database
        if result and 'error' not in result:
            if file_type in ['thermal', 'visual']:
                confidence = result.get('highest_confidence', 0)
                detection_result = f"Detected {result.get('count', 0)} humans"
            else:  # audio
                confidence = result.get('confidence', 0)
                detection_result = f"Voice detected: {result.get('detected', False)}"
            
            db.add_upload_history(filename, file_type, detection_result, confidence)
            
            # If image, draw detections
            if file_type in ['thermal', 'visual'] and result.get('detections'):
                processed_path = ai.draw_detections(filepath, result['detections'])
                result['processed_image'] = processed_path.replace('static/', '')
        
        return jsonify(result)
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/api/simulate-robot-data', methods=['POST'])
def simulate_robot_data():
    """Simulate comprehensive robot data for testing"""
    # Generate random data for testing with gas sensors
    robot_data = {
        'latitude': 6.0329 + random.uniform(-0.01, 0.01),  # Around Negombo
        'longitude': 80.2168 + random.uniform(-0.01, 0.01),
        'front_distance': random.uniform(10, 200),
        'back_distance': random.uniform(10, 200),
        'motion_detected': random.choice([True, False]),
        'battery_level': random.uniform(20, 100),
        'status': random.choice(['Moving', 'Scanning', 'Stopped', 'Charging']),
        'gps_valid': random.choice([True, True, False]),  # Usually valid
        'satellites': random.randint(3, 12),
        'altitude': random.uniform(0, 50),
        'speed': random.uniform(0, 5),
        'heading': random.uniform(0, 360),
        'mq2_gas_level': random.uniform(0, 60),  # Usually safe
        'mq2_gas_detected': random.choice([False, False, False, True]),  # Rarely triggered
        'mq135_air_quality': random.uniform(50, 300),  # Variable air quality
        'mq135_alert_detected': random.choice([False, False, True]),  # Sometimes triggered
        'temperature': random.uniform(20, 35),
        'orientation': random.uniform(-180, 180),
        'is_stable': random.choice([True, True, True, False]),  # Usually stable
        'sound_detected': random.choice([True, False]),
        'distance_traveled': random.uniform(0, 1000),
        'search_pattern': random.randint(0, 2),
        'system_healthy': random.choice([True, True, True, False]),  # Usually healthy
        'current_state': random.choice(['Searching', 'Moving Forward', 'Scanning', 'Obstacle Avoidance']),
        'methane_ppm': random.uniform(0, 800),
        'hydrogen_ppm': random.uniform(0, 500),
        'lpg_ppm': random.uniform(0, 400),
        'smoke_ppm': random.uniform(0, 300),
        'alcohol_ppm': random.uniform(0, 200),
        'mq2_resistance': random.uniform(1000, 50000),
        'emergency_mode': random.choice([False, False, False, False, True])  # Rarely in emergency
    }
    
    # Add to database
    db.add_robot_data(robot_data)
    
    return jsonify({
        'message': 'Enhanced robot data simulated successfully',
        'simulated_fields': len(robot_data),
        'gas_data_included': True,
        'emergency_simulated': robot_data['emergency_mode']
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/system-status')
def get_system_status():
    """Get overall system status including gas monitoring"""
    try:
        # Get latest robot data
        recent_data = db.get_recent_data(1)
        gas_alerts = db.get_gas_alerts(5)
        emergency_alerts = db.get_emergency_alerts(5, False)  # Unacknowledged
        
        status = {
            'system_online': len(recent_data) > 0,
            'last_update': recent_data[0][1] if recent_data else None,
            'active_gas_alerts': len(gas_alerts),
            'active_emergency_alerts': len(emergency_alerts),
            'gas_monitoring_active': True,
            'database_status': 'connected'
        }
        
        if recent_data:
            latest = recent_data[0]
            if len(latest) > 16:
                status.update({
                    'current_gas_levels': {
                        'mq2': latest[14] if len(latest) > 14 else 0,
                        'mq135': latest[16] if len(latest) > 16 else 0,
                        'methane_ppm': latest[26] if len(latest) > 26 else 0,
                        'lpg_ppm': latest[28] if len(latest) > 28 else 0,
                        'smoke_ppm': latest[29] if len(latest) > 29 else 0
                    },
                    'environmental_status': 'safe' if (latest[14] < 30 and latest[16] < 150) else 'elevated',
                    'emergency_mode': latest[32] if len(latest) > 32 else False
                })
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'system_online': False,
            'error': str(e),
            'gas_monitoring_active': False
        })

if __name__ == '__main__':
    print("🚀 Starting Enhanced Robot Dashboard with Gas Monitoring...")
    print("📍 Dashboard will be available at:")
    print("   Local: http://localhost:5002")        
    print("   Network: http://0.0.0.0:5002")       
    print("   ESP32 should connect to: http://172.20.10.2:5002")
    print("🤖 Waiting for robot data...")
    print("💨 Gas monitoring: MQ2 (combustible) + MQ135 (air quality)")
    print("🔬 Advanced gas analysis: Methane, LPG, Smoke, Hydrogen, Alcohol")
    print("🚨 Emergency alert system active")
    print("⚡ Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5002, threaded=True)