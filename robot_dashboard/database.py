import sqlite3
import json
from datetime import datetime
import os

class RobotDatabase:
    def __init__(self, db_path='data/robot_data.db'):
        self.db_path = db_path
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # GPS and sensor data table (UPDATED with gas sensors)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robot_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                latitude REAL,
                longitude REAL,
                front_distance REAL,
                back_distance REAL,
                motion_detected BOOLEAN,
                battery_level REAL,
                status TEXT,
                gps_valid BOOLEAN DEFAULT 0,
                satellites INTEGER DEFAULT 0,
                altitude REAL DEFAULT 0.0,
                speed REAL DEFAULT 0.0,
                heading REAL DEFAULT 0.0,
                mq2_gas_level REAL DEFAULT 0.0,
                mq2_gas_detected BOOLEAN DEFAULT 0,
                mq135_air_quality REAL DEFAULT 0.0,
                mq135_alert_detected BOOLEAN DEFAULT 0,
                temperature REAL DEFAULT 0.0,
                orientation REAL DEFAULT 0.0,
                is_stable BOOLEAN DEFAULT 1,
                sound_detected BOOLEAN DEFAULT 0,
                distance_traveled REAL DEFAULT 0.0,
                search_pattern INTEGER DEFAULT 0,
                system_healthy BOOLEAN DEFAULT 1,
                current_state TEXT DEFAULT 'Unknown',
                methane_ppm REAL DEFAULT 0.0,
                hydrogen_ppm REAL DEFAULT 0.0,
                lpg_ppm REAL DEFAULT 0.0,
                smoke_ppm REAL DEFAULT 0.0,
                alcohol_ppm REAL DEFAULT 0.0,
                mq2_resistance REAL DEFAULT 0.0,
                emergency_mode BOOLEAN DEFAULT 0
            )
        ''')
        
        
        # Add new columns to existing table if they don't exist
        self._add_column_if_not_exists(cursor, 'robot_data', 'gps_valid', 'BOOLEAN DEFAULT 0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'satellites', 'INTEGER DEFAULT 0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'altitude', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'speed', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'heading', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'mq2_gas_level', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'mq2_gas_detected', 'BOOLEAN DEFAULT 0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'mq135_air_quality', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'mq135_alert_detected', 'BOOLEAN DEFAULT 0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'temperature', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'orientation', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'is_stable', 'BOOLEAN DEFAULT 1')
        self._add_column_if_not_exists(cursor, 'robot_data', 'sound_detected', 'BOOLEAN DEFAULT 0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'distance_traveled', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'search_pattern', 'INTEGER DEFAULT 0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'system_healthy', 'BOOLEAN DEFAULT 1')
        self._add_column_if_not_exists(cursor, 'robot_data', 'current_state', 'TEXT DEFAULT "Unknown"')
        self._add_column_if_not_exists(cursor, 'robot_data', 'methane_ppm', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'hydrogen_ppm', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'lpg_ppm', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'smoke_ppm', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'alcohol_ppm', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'mq2_resistance', 'REAL DEFAULT 0.0')
        self._add_column_if_not_exists(cursor, 'robot_data', 'emergency_mode', 'BOOLEAN DEFAULT 0')
        
        # Human detection results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                detection_type TEXT,
                confidence REAL,
                latitude REAL,
                longitude REAL,
                file_path TEXT,
                bbox_data TEXT
            )
        ''')
        
        # Upload history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS upload_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                file_name TEXT,
                file_type TEXT,
                detection_result TEXT,
                confidence REAL
            )
        ''')
        
        # Gas monitoring history table (NEW)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gas_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                mq2_level REAL,
                mq135_level REAL,
                latitude REAL,
                longitude REAL,
                alert_triggered BOOLEAN DEFAULT 0,
                alert_type TEXT,
                methane_ppm REAL DEFAULT 0.0,
                hydrogen_ppm REAL DEFAULT 0.0,
                lpg_ppm REAL DEFAULT 0.0,
                smoke_ppm REAL DEFAULT 0.0,
                alcohol_ppm REAL DEFAULT 0.0
            )
        ''')
        
        # Emergency alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT,
                severity TEXT,
                message TEXT,
                latitude REAL,
                longitude REAL,
                acknowledged BOOLEAN DEFAULT 0,
                response_time DATETIME
            )
        ''')
        
        # System status table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL DEFAULT 0.0,
                memory_usage REAL DEFAULT 0.0,
                disk_usage REAL DEFAULT 0.0,
                network_status TEXT DEFAULT 'connected',
                sensor_status TEXT DEFAULT 'operational',
                last_maintenance DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _add_column_if_not_exists(self, cursor, table_name, column_name, column_def):
        """Helper method to add column if it doesn't exist"""
        try:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")
        except sqlite3.OperationalError:
            # Column already exists
            pass
    
    def add_robot_data(self, data_dict):
        """Add comprehensive robot sensor data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract all possible fields with defaults
        fields = {
            'latitude': data_dict.get('latitude', 0.0),
            'longitude': data_dict.get('longitude', 0.0),
            'front_distance': data_dict.get('front_distance', 0.0),
            'back_distance': data_dict.get('back_distance', 0.0),
            'motion_detected': data_dict.get('motion_detected', False),
            'battery_level': data_dict.get('battery_level', 0.0),
            'status': data_dict.get('status', 'Unknown'),
            'gps_valid': data_dict.get('gps_valid', False),
            'satellites': data_dict.get('satellites', 0),
            'altitude': data_dict.get('altitude', 0.0),
            'speed': data_dict.get('speed', 0.0),
            'heading': data_dict.get('heading', 0.0),
            'mq2_gas_level': data_dict.get('mq2_gas_level', 0.0),
            'mq2_gas_detected': data_dict.get('mq2_gas_detected', False),
            'mq135_air_quality': data_dict.get('mq135_air_quality', 0.0),
            'mq135_alert_detected': data_dict.get('mq135_alert_detected', False),
            'temperature': data_dict.get('temperature', 0.0),
            'orientation': data_dict.get('orientation', 0.0),
            'is_stable': data_dict.get('is_stable', True),
            'sound_detected': data_dict.get('sound_detected', False),
            'distance_traveled': data_dict.get('distance_traveled', 0.0),
            'search_pattern': data_dict.get('search_pattern', 0),
            'system_healthy': data_dict.get('system_healthy', True),
            'current_state': data_dict.get('current_state', 'Unknown'),
            'methane_ppm': data_dict.get('methane_ppm', 0.0),
            'hydrogen_ppm': data_dict.get('hydrogen_ppm', 0.0),
            'lpg_ppm': data_dict.get('lpg_ppm', 0.0),
            'smoke_ppm': data_dict.get('smoke_ppm', 0.0),
            'alcohol_ppm': data_dict.get('alcohol_ppm', 0.0),
            'mq2_resistance': data_dict.get('mq2_resistance', 0.0),
            'emergency_mode': data_dict.get('emergency_mode', False)
        }
        
        cursor.execute('''
            INSERT INTO robot_data 
            (latitude, longitude, front_distance, back_distance, motion_detected, battery_level, status,
             gps_valid, satellites, altitude, speed, heading,
             mq2_gas_level, mq2_gas_detected, mq135_air_quality, mq135_alert_detected,
             temperature, orientation, is_stable, sound_detected, distance_traveled,
             search_pattern, system_healthy, current_state, methane_ppm, hydrogen_ppm,
             lpg_ppm, smoke_ppm, alcohol_ppm, mq2_resistance, emergency_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fields['latitude'], fields['longitude'], fields['front_distance'], fields['back_distance'],
            fields['motion_detected'], fields['battery_level'], fields['status'],
            fields['gps_valid'], fields['satellites'], fields['altitude'], fields['speed'], fields['heading'],
            fields['mq2_gas_level'], fields['mq2_gas_detected'], fields['mq135_air_quality'], fields['mq135_alert_detected'],
            fields['temperature'], fields['orientation'], fields['is_stable'], fields['sound_detected'],
            fields['distance_traveled'], fields['search_pattern'], fields['system_healthy'], fields['current_state'],
            fields['methane_ppm'], fields['hydrogen_ppm'], fields['lpg_ppm'], fields['smoke_ppm'],
            fields['alcohol_ppm'], fields['mq2_resistance'], fields['emergency_mode']
        ))
        
        # Also log gas data if levels are significant
        if fields['mq2_gas_level'] > 20 or fields['mq135_air_quality'] > 100:
            self._log_gas_event(cursor, fields)
        
        # Log emergency if in emergency mode
        if fields['emergency_mode']:
            self._log_emergency_alert(cursor, fields)
        
        conn.commit()
        conn.close()
    
    def _log_gas_event(self, cursor, fields):
        """Log significant gas events to gas_history table"""
        alert_triggered = False
        alert_type = "normal"
        
        # Determine alert level
        if fields['mq2_gas_level'] > 70 or fields['mq135_air_quality'] > 350:
            alert_triggered = True
            alert_type = "critical"
        elif fields['mq2_gas_level'] > 50 or fields['mq135_air_quality'] > 250:
            alert_triggered = True
            alert_type = "warning"
        elif fields['mq2_gas_level'] > 30 or fields['mq135_air_quality'] > 150:
            alert_type = "elevated"
        
        cursor.execute('''
            INSERT INTO gas_history
            (mq2_level, mq135_level, latitude, longitude, alert_triggered, alert_type,
             methane_ppm, hydrogen_ppm, lpg_ppm, smoke_ppm, alcohol_ppm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fields['mq2_gas_level'], fields['mq135_air_quality'],
            fields['latitude'], fields['longitude'],
            alert_triggered, alert_type,
            fields['methane_ppm'], fields['hydrogen_ppm'], fields['lpg_ppm'],
            fields['smoke_ppm'], fields['alcohol_ppm']
        ))
    
    def _log_emergency_alert(self, cursor, fields):
        """Log emergency alerts"""
        severity = "critical" if fields['mq2_gas_level'] > 80 or fields['mq135_air_quality'] > 400 else "high"
        
        message = f"Emergency detected - Gas levels: MQ2={fields['mq2_gas_level']:.1f}, MQ135={fields['mq135_air_quality']:.1f}"
        if fields['motion_detected']:
            message += ", Human detected"
        
        cursor.execute('''
            INSERT INTO emergency_alerts
            (alert_type, severity, message, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        ''', ("gas_emergency", severity, message, fields['latitude'], fields['longitude']))
    
    def add_detection(self, detection_type, confidence, lat, lon, file_path, bbox_data):
        """Add detection result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO detections 
            (detection_type, confidence, latitude, longitude, file_path, bbox_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (detection_type, confidence, lat, lon, file_path, json.dumps(bbox_data)))
        
        conn.commit()
        conn.close()
    
    def get_recent_data(self, limit=100):
        """Get recent robot data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM robot_data 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_gas_history(self, limit=100, hours=24):
        """Get recent gas monitoring data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM gas_history 
            WHERE timestamp > datetime('now', '-{} hours')
            ORDER BY timestamp DESC 
            LIMIT ?
        '''.format(hours), (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_gas_alerts(self, limit=20):
        """Get recent gas alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM gas_history 
            WHERE alert_triggered = 1
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_recent_detections(self, limit=50):
        """Get recent detections"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM detections 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def add_upload_history(self, file_name, file_type, result, confidence):
        """Add upload history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO upload_history 
            (file_name, file_type, detection_result, confidence)
            VALUES (?, ?, ?, ?)
        ''', (file_name, file_type, result, confidence))
        
        conn.commit()
        conn.close()
    
    def get_upload_history(self, limit=20):
        """Get upload history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM upload_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_emergency_alerts(self, limit=10, acknowledged=None):
        """Get emergency alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if acknowledged is not None:
            cursor.execute('''
                SELECT * FROM emergency_alerts 
                WHERE acknowledged = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (acknowledged, limit))
        else:
            cursor.execute('''
                SELECT * FROM emergency_alerts 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    
    def acknowledge_alert(self, alert_id):
        """Acknowledge an emergency alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE emergency_alerts 
            SET acknowledged = 1, response_time = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (alert_id,))
        
        conn.commit()
        conn.close()
    
    def log_system_status(self, cpu_usage=0.0, memory_usage=0.0, disk_usage=0.0, 
                         network_status='connected', sensor_status='operational'):
        """Log system status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_status 
            (cpu_usage, memory_usage, disk_usage, network_status, sensor_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (cpu_usage, memory_usage, disk_usage, network_status, sensor_status))
        
        conn.commit()
        conn.close()
    
    def get_system_status(self, limit=10):
        """Get recent system status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM system_status 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        data = cursor.fetchall()
        conn.close()
        return data