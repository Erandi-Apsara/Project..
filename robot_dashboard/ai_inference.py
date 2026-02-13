import os
import random
from PIL import Image, ImageDraw, ImageFont
import json
import numpy as np
from datetime import datetime

class AIInference:
    def __init__(self):
        self.thermal_model = None
        self.visual_model = None
        self.voice_model = None
        self.gas_analysis_model = None
        
        # Gas detection thresholds and patterns
        self.gas_thresholds = {
            'mq2': {
                'safe': 60,
                'caution': 80,
                'danger': 90,
                'critical': 100
            },
            'mq135': {
                'good': 150,
                'moderate': 300,
                'poor': 400,
                'hazardous': 500
            },
            'methane': {
                'safe': 500,
                'caution': 2000,
                'danger': 2500,
                'critical': 5000
            },
            'lpg': {
                'safe': 200,
                'caution': 1000,
                'danger': 1000,
                'critical': 2000
            },
            'smoke': {
                'safe': 100,
                'caution': 499,
                'danger': 500,
                'critical': 1000
            },
            'hydrogen': {
                'safe': 1000,
                'caution': 3999,
                'danger': 10000,
                'critical': 20000
            },
            'alcohol': {
                'safe': 50,
                'caution': 199,
                'danger': 200,
                'critical': 500
            }
        }
        
        # Gas danger classifications
        self.gas_properties = {
            'methane': {
                'explosive_range': '5-15%',
                'density': 'lighter_than_air',
                'health_risk': 'asphyxiant',
                'ignition_temp': '537°C'
            },
            'lpg': {
                'explosive_range': '1.8-9.5%',
                'density': 'heavier_than_air',
                'health_risk': 'narcotic',
                'ignition_temp': '470°C'
            },
            'hydrogen': {
                'explosive_range': '4-75%',
                'density': 'lighter_than_air',
                'health_risk': 'asphyxiant',
                'ignition_temp': '560°C'
            },
            'smoke': {
                'composition': 'particles_and_gases',
                'health_risk': 'respiratory_toxin',
                'visibility_impact': 'severe',
                'temperature_indicator': 'fire_presence'
            }
        }
        
        self.load_models()
    
    def load_models(self):
        """Load all AI models - enhanced with gas analysis"""
        try:
            # Check if model files exist
            thermal_model_path = "models/thermal/best.pt"
            visual_model_path = "models/visual/best.pt"
            gas_model_path = "models/gas/gas_analyzer.pt"
            
            if os.path.exists(thermal_model_path):
                print("Thermal model path found")
                self.thermal_model = "loaded"  # Placeholder
            else:
                print("Thermal model not found at:", thermal_model_path)
            
            if os.path.exists(visual_model_path):
                print("Visual model path found")
                self.visual_model = "loaded"  # Placeholder
            else:
                print("Visual model not found at:", visual_model_path)
            
            if os.path.exists(gas_model_path):
                print("Gas analysis model found")
                self.gas_analysis_model = "loaded"
            else:
                print("Gas analysis model not found - using threshold-based detection")
            
            print("AI models initialized (enhanced mode with advanced gas detection)")
            
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def detect_thermal_human(self, image_path):
        """Detect humans in thermal images - enhanced simulation"""
        try:
            if not os.path.exists(image_path):
                return {"error": "Image file not found"}
            
            # Open image to get dimensions
            with Image.open(image_path) as img:
                width, height = img.size
            
            # Simulate random detections for demo
            num_detections = random.randint(0, 3)
            detections = []
            
            for i in range(num_detections):
                # Random bounding box coordinates
                x1 = random.randint(0, width // 2)
                y1 = random.randint(0, height // 2)
                x2 = x1 + random.randint(50, width // 3)
                y2 = y1 + random.randint(50, height // 3)
                
                # Ensure coordinates are within image bounds
                x2 = min(x2, width)
                y2 = min(y2, height)
                
                confidence = random.uniform(0.6, 0.95)
                
                # Simulate temperature data for thermal detection
                temperature = random.uniform(36.0, 38.5)  # Human body temperature range
                heat_signature = random.choice(['strong', 'moderate', 'weak'])
                
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': confidence,
                    'class_id': 0,
                    'label': 'human',
                    'temperature': temperature,
                    'heat_signature': heat_signature,
                    'thermal_signature': 'human_detected',
                    'body_parts': {
                        'head': temperature + random.uniform(-0.5, 0.5),
                        'torso': temperature + random.uniform(-1.0, 0.5),
                        'limbs': temperature + random.uniform(-2.0, 0.0)
                    }
                })
            
            return {
                'detections': detections,
                'count': len(detections),
                'highest_confidence': max([d['confidence'] for d in detections]) if detections else 0,
                'average_temperature': sum([d['temperature'] for d in detections]) / len(detections) if detections else 0,
                'temperature_range': {
                    'min': min([d['temperature'] for d in detections]) if detections else 0,
                    'max': max([d['temperature'] for d in detections]) if detections else 0
                },
                'detection_type': 'thermal',
                'environmental_temperature': random.uniform(20, 35),
                'note': 'Enhanced thermal detection with detailed temperature analysis'
            }
            
        except Exception as e:
            return {"error": f"Thermal detection error: {e}"}
    
    def detect_visual_human(self, image_path):
        """Detect humans in normal images - enhanced simulation"""
        try:
            if not os.path.exists(image_path):
                return {"error": "Image file not found"}
            
            with Image.open(image_path) as img:
                width, height = img.size
            
            # Simulate detection
            num_detections = random.randint(0, 2)
            detections = []
            
            for i in range(num_detections):
                x1 = random.randint(0, width // 2)
                y1 = random.randint(0, height // 2)
                x2 = x1 + random.randint(50, width // 3)
                y2 = y1 + random.randint(50, height // 3)
                
                x2 = min(x2, width)
                y2 = min(y2, height)
                
                confidence = random.uniform(0.7, 0.98)
                
                # Simulate additional visual features
                pose = random.choice(['standing', 'sitting', 'walking', 'lying', 'crouching'])
                clothing_color = random.choice(['dark', 'light', 'bright', 'camouflage', 'reflective'])
                movement_status = random.choice(['stationary', 'moving', 'fast_movement'])
                estimated_distance = random.uniform(5, 100)  # meters
                
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': confidence,
                    'class_id': 0,
                    'label': 'human',
                    'pose': pose,
                    'clothing': clothing_color,
                    'visibility': 'clear',
                    'movement_status': movement_status,
                    'estimated_distance': estimated_distance,
                    'threat_level': self._assess_threat_level(pose, movement_status, estimated_distance),
                    'biometric_estimate': {
                        'height': random.uniform(150, 190),  # cm
                        'build': random.choice(['slim', 'average', 'heavy'])
                    }
                })
            
            return {
                'detections': detections,
                'count': len(detections),
                'highest_confidence': max([d['confidence'] for d in detections]) if detections else 0,
                'average_distance': sum([d['estimated_distance'] for d in detections]) / len(detections) if detections else 0,
                'detection_type': 'visual',
                'lighting_conditions': random.choice(['good', 'poor', 'artificial', 'natural']),
                'weather_impact': random.choice(['none', 'fog', 'rain', 'glare']),
                'note': 'Enhanced visual detection with behavioral analysis'
            }
            
        except Exception as e:
            return {"error": f"Visual detection error: {e}"}
    
    def _assess_threat_level(self, pose, movement, distance):
        """Assess threat level based on human behavior"""
        threat_score = 0
        
        # Pose assessment
        if pose in ['crouching', 'lying']:
            threat_score += 2
        elif pose == 'standing':
            threat_score += 1
        
        # Movement assessment
        if movement == 'fast_movement':
            threat_score += 3
        elif movement == 'moving':
            threat_score += 1
        
        # Distance assessment
        if distance < 10:
            threat_score += 2
        elif distance < 25:
            threat_score += 1
        
        if threat_score >= 5:
            return 'high'
        elif threat_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def detect_voice_human(self, audio_path):
        """Detect human voice in audio files - enhanced simulation"""
        try:
            if not os.path.exists(audio_path):
                return {"error": "Audio file not found"}
            
            # Simulate voice detection with more detailed analysis
            detected = random.choice([True, False, True])  # 2/3 chance of detection
            confidence = random.uniform(0.5, 0.9) if detected else random.uniform(0.1, 0.3)
            
            # Simulate duration (you can get actual duration later)
            duration = random.uniform(1.0, 10.0)
            
            # Enhanced voice characteristics
            voice_features = {
                'gender': random.choice(['male', 'female', 'unknown']),
                'age_estimate': random.choice(['child', 'young_adult', 'adult', 'elderly', 'unknown']),
                'language': random.choice(['english', 'sinhala', 'tamil', 'unknown']),
                'emotion': random.choice(['calm', 'distressed', 'shouting', 'whispering', 'crying', 'panic']),
                'clarity': random.uniform(0.3, 1.0),
                'background_noise': random.uniform(0.0, 0.8),
                'speech_rate': random.choice(['slow', 'normal', 'fast', 'rapid']),
                'volume_level': random.choice(['whisper', 'normal', 'loud', 'shouting'])
            }
            
            # Distress indicators
            distress_indicators = []
            if voice_features['emotion'] in ['distressed', 'crying', 'panic']:
                distress_indicators.extend(['emotional_stress', 'potential_emergency'])
            if voice_features['volume_level'] == 'shouting':
                distress_indicators.append('elevated_voice')
            if voice_features['speech_rate'] == 'rapid':
                distress_indicators.append('rapid_speech')
            
            return {
                'detected': detected,
                'confidence': confidence,
                'duration': duration,
                'voice_features': voice_features,
                'distress_indicators': distress_indicators,
                'emergency_likelihood': len(distress_indicators) / 4.0,  # 0-1 scale
                'detection_type': 'audio',
                'analysis_timestamp': datetime.now().isoformat(),
                'note': 'Enhanced voice detection with emergency assessment'
            }
                
        except Exception as e:
            return {"error": f"Voice detection error: {e}"}
    
    def analyze_gas_levels(self, mq2_level, mq135_level, specific_gases=None):
        """Analyze gas levels and provide comprehensive safety assessment"""
        try:
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'mq2_analysis': self._analyze_mq2(mq2_level),
                'mq135_analysis': self._analyze_mq135(mq135_level),
                'overall_safety': 'safe',
                'recommendations': [],
                'risk_level': 0,  # 0-10 scale
                'emergency_actions': [],
                'environmental_factors': self._assess_environmental_factors()
            }
            
            # Analyze specific gases if provided
            if specific_gases:
                analysis['specific_gas_analysis'] = {}
                for gas_type, level in specific_gases.items():
                    if gas_type in self.gas_thresholds:
                        analysis['specific_gas_analysis'][gas_type] = self._analyze_specific_gas(gas_type, level)
            
            # Determine overall risk
            mq2_risk = analysis['mq2_analysis']['risk_level']
            mq135_risk = analysis['mq135_analysis']['risk_level']
            specific_risk = 0
            
            if 'specific_gas_analysis' in analysis:
                specific_risks = [gas['risk_level'] for gas in analysis['specific_gas_analysis'].values()]
                specific_risk = max(specific_risks) if specific_risks else 0
            
            overall_risk = max(mq2_risk, mq135_risk, specific_risk)
            
            # Set overall safety status and recommendations
            if overall_risk >= 8:
                analysis['overall_safety'] = 'critical'
                analysis['emergency_actions'].extend([
                    'IMMEDIATE EVACUATION REQUIRED',
                    'Contact emergency services (119/110)',
                    'Do not use electrical equipment',
                    'Ventilate area if safely possible',
                    'Account for all personnel'
                ])
            elif overall_risk >= 6:
                analysis['overall_safety'] = 'dangerous'
                analysis['emergency_actions'].extend([
                    'Evacuate area immediately',
                    'Ensure maximum ventilation',
                    'Monitor levels continuously',
                    'Prepare for emergency evacuation',
                    'Contact safety personnel'
                ])
            elif overall_risk >= 4:
                analysis['overall_safety'] = 'caution'
                analysis['recommendations'].extend([
                    'Limit exposure time',
                    'Increase ventilation',
                    'Monitor for symptoms',
                    'Identify gas source',
                    'Have evacuation plan ready'
                ])
            elif overall_risk >= 2:
                analysis['overall_safety'] = 'elevated'
                analysis['recommendations'].extend([
                    'Monitor levels regularly',
                    'Check ventilation systems',
                    'Investigate potential sources'
                ])
            
            analysis['risk_level'] = overall_risk
            
            # Add gas-specific recommendations
            analysis['gas_specific_guidance'] = self._generate_gas_specific_guidance(analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Gas analysis error: {e}"}
    
    def _analyze_mq2(self, level):
        """Analyze MQ2 combustible gas levels"""
        analysis = {
            'level': level,
            'unit': 'raw_reading',
            'gas_type': 'combustible (LPG, propane, methane, hydrogen)',
            'status': 'safe',
            'risk_level': 0,
            'health_impact': 'none',
            'fire_risk': 'low',
            'explosion_potential': 'minimal'
        }
        
        if level >= self.gas_thresholds['mq2']['critical']:
            analysis.update({
                'status': 'critical',
                'risk_level': 10,
                'health_impact': 'severe - explosion risk imminent',
                'fire_risk': 'extreme',
                'explosion_potential': 'high'
            })
        elif level >= self.gas_thresholds['mq2']['danger']:
            analysis.update({
                'status': 'dangerous',
                'risk_level': 8,
                'health_impact': 'high - fire/explosion risk',
                'fire_risk': 'high',
                'explosion_potential': 'moderate'
            })
        elif level >= self.gas_thresholds['mq2']['caution']:
            analysis.update({
                'status': 'caution',
                'risk_level': 5,
                'health_impact': 'moderate - potential fire risk',
                'fire_risk': 'moderate',
                'explosion_potential': 'low'
            })
        elif level >= self.gas_thresholds['mq2']['safe']:
            analysis.update({
                'status': 'elevated',
                'risk_level': 2,
                'health_impact': 'low - monitor levels',
                'fire_risk': 'low',
                'explosion_potential': 'minimal'
            })
        
        return analysis
    
    def _analyze_mq135(self, level):
        """Analyze MQ135 air quality levels"""
        analysis = {
            'level': level,
            'unit': 'ppm',
            'gas_type': 'air quality (CO2, NH3, NOx, benzene, alcohol)',
            'status': 'good',
            'risk_level': 0,
            'health_impact': 'none',
            'breathing_safety': 'safe',
            'long_term_effects': 'none'
        }
        
        if level >= self.gas_thresholds['mq135']['hazardous']:
            analysis.update({
                'status': 'hazardous',
                'risk_level': 9,
                'health_impact': 'severe - toxic exposure',
                'breathing_safety': 'dangerous',
                'long_term_effects': 'serious health consequences'
            })
        elif level >= self.gas_thresholds['mq135']['poor']:
            analysis.update({
                'status': 'poor',
                'risk_level': 7,
                'health_impact': 'high - avoid prolonged exposure',
                'breathing_safety': 'unsafe',
                'long_term_effects': 'potential health impacts'
            })
        elif level >= self.gas_thresholds['mq135']['moderate']:
            analysis.update({
                'status': 'moderate',
                'risk_level': 4,
                'health_impact': 'moderate - limit exposure',
                'breathing_safety': 'caution',
                'long_term_effects': 'monitor health'
            })
        elif level >= self.gas_thresholds['mq135']['good']:
            analysis.update({
                'status': 'elevated',
                'risk_level': 2,
                'health_impact': 'low - acceptable for short periods',
                'breathing_safety': 'acceptable',
                'long_term_effects': 'minimal'
            })
        
        return analysis
    
    def _analyze_specific_gas(self, gas_type, level):
        """Analyze specific gas levels"""
        thresholds = self.gas_thresholds.get(gas_type, {})
        properties = self.gas_properties.get(gas_type, {})
        
        analysis = {
            'gas_type': gas_type,
            'level': level,
            'unit': 'ppm',
            'status': 'safe',
            'risk_level': 0,
            'properties': properties,
            'health_impact': 'minimal',
            'fire_explosion_risk': 'low'
        }
        
        if level >= thresholds.get('critical', float('inf')):
            analysis.update({
                'status': 'critical',
                'risk_level': 10,
                'health_impact': 'life_threatening',
                'fire_explosion_risk': 'extreme'
            })
        elif level >= thresholds.get('danger', float('inf')):
            analysis.update({
                'status': 'dangerous',
                'risk_level': 8,
                'health_impact': 'severe',
                'fire_explosion_risk': 'high'
            })
        elif level >= thresholds.get('caution', float('inf')):
            analysis.update({
                'status': 'caution',
                'risk_level': 5,
                'health_impact': 'moderate',
                'fire_explosion_risk': 'moderate'
            })
        elif level >= thresholds.get('safe', float('inf')):
            analysis.update({
                'status': 'elevated',
                'risk_level': 2,
                'health_impact': 'low',
                'fire_explosion_risk': 'low'
            })
        
        return analysis
    
    def _assess_environmental_factors(self):
        """Assess environmental factors affecting gas behavior"""
        return {
            'temperature': random.uniform(20, 35),
            'humidity': random.uniform(40, 80),
            'air_pressure': random.uniform(1000, 1020),
            'wind_conditions': random.choice(['calm', 'light_breeze', 'moderate_wind', 'strong_wind']),
            'ventilation_status': random.choice(['poor', 'adequate', 'good', 'excellent']),
            'building_type': random.choice(['open_area', 'enclosed_space', 'basement', 'multi_story'])
        }
    
    def _generate_gas_specific_guidance(self, analysis):
        """Generate gas-specific safety guidance"""
        guidance = {
            'immediate_actions': [],
            'safety_equipment': [],
            'monitoring_recommendations': [],
            'prevention_measures': []
        }
        
        risk_level = analysis['risk_level']
        
        if risk_level >= 8:
            guidance['immediate_actions'].extend([
                'Evacuate immediately',
                'Call emergency services',
                'Account for all personnel',
                'Do not re-enter until cleared'
            ])
            guidance['safety_equipment'].extend([
                'Self-contained breathing apparatus',
                'Gas detection equipment',
                'Emergency communication devices'
            ])
        elif risk_level >= 6:
            guidance['immediate_actions'].extend([
                'Clear the area',
                'Increase ventilation',
                'Monitor continuously',
                'Prepare evacuation plan'
            ])
            guidance['safety_equipment'].extend([
                'Portable gas detectors',
                'Respiratory protection',
                'Communication equipment'
            ])
        
        guidance['monitoring_recommendations'].extend([
            'Install continuous gas monitoring',
            'Regular calibration of sensors',
            'Multiple detection points',
            'Data logging and trending'
        ])
        
        guidance['prevention_measures'].extend([
            'Regular equipment maintenance',
            'Leak detection surveys',
            'Ventilation system checks',
            'Personnel training programs'
        ])
        
        return guidance
    
    def detect_gas_patterns(self, gas_history):
        """Detect patterns in gas level history with advanced analytics"""
        try:
            if len(gas_history) < 5:
                return {"error": "Insufficient data for pattern analysis (minimum 5 readings required)"}
            
            mq2_levels = [reading.get('mq2_level', 0) for reading in gas_history]
            mq135_levels = [reading.get('mq135_level', 0) for reading in gas_history]
            
            analysis = {
                'trend_analysis': {
                    'mq2_trend': self._calculate_trend(mq2_levels),
                    'mq135_trend': self._calculate_trend(mq135_levels),
                    'correlation': self._calculate_correlation(mq2_levels, mq135_levels)
                },
                'anomaly_detection': {
                    'mq2_anomalies': self._detect_anomalies(mq2_levels),
                    'mq135_anomalies': self._detect_anomalies(mq135_levels),
                    'sudden_spikes': self._detect_sudden_spikes(gas_history)
                },
                'predictions': {
                    'mq2_forecast': self._advanced_forecast(mq2_levels),
                    'mq135_forecast': self._advanced_forecast(mq135_levels),
                    'risk_probability': self._calculate_risk_probability(gas_history)
                },
                'statistical_summary': {
                    'mq2_stats': self._calculate_statistics(mq2_levels),
                    'mq135_stats': self._calculate_statistics(mq135_levels)
                },
                'recommendations': []
            }
            
            # Add pattern-based recommendations
            if analysis['trend_analysis']['mq2_trend'] == 'increasing':
                analysis['recommendations'].append('MQ2 levels trending upward - investigate combustible gas sources')
            
            if analysis['trend_analysis']['mq135_trend'] == 'increasing':
                analysis['recommendations'].append('Air quality deteriorating - check ventilation and pollution sources')
            
            if analysis['anomaly_detection']['sudden_spikes'] > 2:
                analysis['recommendations'].append('Multiple sudden spikes detected - check for intermittent gas leaks')
            
            if analysis['predictions']['risk_probability'] > 0.7:
                analysis['recommendations'].append('High probability of dangerous gas levels - implement preventive measures')
            
            # Correlation analysis
            correlation = analysis['trend_analysis']['correlation']
            if abs(correlation) > 0.7:
                if correlation > 0:
                    analysis['recommendations'].append('Strong positive correlation between gas sensors - common source likely')
                else:
                    analysis['recommendations'].append('Strong negative correlation detected - investigate opposing factors')
            
            return analysis
            
        except Exception as e:
            return {"error": f"Pattern detection error: {e}"}
    
    def _calculate_trend(self, values):
        """Calculate trend direction with statistical analysis"""
        if len(values) < 3:
            return 'insufficient_data'
        
        # Linear regression for trend
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'stable'
        
        slope = numerator / denominator
        
        # Recent trend analysis (last 1/3 of data)
        recent_third = len(values) // 3
        recent_avg = sum(values[-recent_third:]) / recent_third if recent_third > 0 else values[-1]
        earlier_avg = sum(values[:-recent_third]) / (len(values) - recent_third) if recent_third > 0 else values[0]
        
        recent_change = ((recent_avg - earlier_avg) / earlier_avg) * 100 if earlier_avg > 0 else 0
        
        if abs(slope) < 0.1 and abs(recent_change) < 5:
            return 'stable'
        elif slope > 0.2 or recent_change > 10:
            return 'increasing'
        elif slope < -0.2 or recent_change < -10:
            return 'decreasing'
        else:
            return 'fluctuating'
    
    def _calculate_correlation(self, values1, values2):
        """Calculate correlation coefficient between two datasets"""
        if len(values1) != len(values2) or len(values1) < 2:
            return 0
        
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        
        numerator = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n))
        
        sum_sq1 = sum((values1[i] - mean1) ** 2 for i in range(n))
        sum_sq2 = sum((values2[i] - mean2) ** 2 for i in range(n))
        
        denominator = (sum_sq1 * sum_sq2) ** 0.5
        
        return numerator / denominator if denominator > 0 else 0
    
    def _detect_anomalies(self, values):
        """Enhanced anomaly detection using statistical methods"""
        if len(values) < 5:
            return 0
        
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        # Z-score method
        z_scores = [(x - mean_val) / std_dev if std_dev > 0 else 0 for x in values]
        z_anomalies = sum(1 for z in z_scores if abs(z) > 2)
        
        # Interquartile range method
        sorted_values = sorted(values)
        n = len(sorted_values)
        q1 = sorted_values[n // 4]
        q3 = sorted_values[3 * n // 4]
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        iqr_anomalies = sum(1 for x in values if x < lower_bound or x > upper_bound)
        
        return max(z_anomalies, iqr_anomalies)
    
    def _detect_sudden_spikes(self, gas_history):
        """Detect sudden spikes in gas levels"""
        spike_count = 0
        
        for i in range(1, len(gas_history)):
            prev_mq2 = gas_history[i-1].get('mq2_level', 0)
            curr_mq2 = gas_history[i].get('mq2_level', 0)
            prev_mq135 = gas_history[i-1].get('mq135_level', 0)
            curr_mq135 = gas_history[i].get('mq135_level', 0)
            
            # Check for significant increases
            mq2_increase = (curr_mq2 - prev_mq2) / prev_mq2 if prev_mq2 > 0 else 0
            mq135_increase = (curr_mq135 - prev_mq135) / prev_mq135 if prev_mq135 > 0 else 0
            
            if mq2_increase > 0.5 or mq135_increase > 0.5:  # 50% increase
                spike_count += 1
        
        return spike_count
    
    def _advanced_forecast(self, values):
        """Advanced forecasting using trend analysis and pattern recognition"""
        if len(values) < 3:
            return values[-1] if values else 0
        
        # Simple exponential smoothing
        alpha = 0.3  # Smoothing factor
        forecast = values[0]
        
        for value in values[1:]:
            forecast = alpha * value + (1 - alpha) * forecast
        
        # Trend component
        if len(values) >= 5:
            recent_trend = (values[-1] - values[-5]) / 4
            forecast += recent_trend
        
        return max(0, forecast)  # Don't predict negative values
    
    def _calculate_risk_probability(self, gas_history):
        """Calculate probability of dangerous gas levels"""
        if len(gas_history) < 3:
            return 0
        
        danger_count = 0
        for reading in gas_history:
            mq2_level = reading.get('mq2_level', 0)
            mq135_level = reading.get('mq135_level', 0)
            
            if mq2_level > self.gas_thresholds['mq2']['caution'] or \
               mq135_level > self.gas_thresholds['mq135']['moderate']:
                danger_count += 1
        
        return danger_count / len(gas_history)
    
    def _calculate_statistics(self, values):
        """Calculate comprehensive statistics for gas level data"""
        if not values:
            return {}
        
        n = len(values)
        mean_val = sum(values) / n
        sorted_values = sorted(values)
        
        # Calculate percentiles
        def percentile(data, p):
            k = (len(data) - 1) * p
            f = int(k)
            c = k - f
            if f + 1 < len(data):
                return data[f] * (1 - c) + data[f + 1] * c
            else:
                return data[f]
        
        return {
            'count': n,
            'mean': mean_val,
            'median': sorted_values[n // 2],
            'min': min(values),
            'max': max(values),
            'range': max(values) - min(values),
            'std_dev': (sum((x - mean_val) ** 2 for x in values) / n) ** 0.5,
            'percentiles': {
                '25th': percentile(sorted_values, 0.25),
                '75th': percentile(sorted_values, 0.75),
                '90th': percentile(sorted_values, 0.90),
                '95th': percentile(sorted_values, 0.95)
            }
        }
    
    def draw_detections(self, image_path, detections):
        """Draw bounding boxes on image with enhanced gas-aware annotations"""
        try:
            # Open the original image
            with Image.open(image_path) as img:
                draw = Image.ImageDraw.Draw(img)
                
                # Try to load a font
                try:
                    font = ImageFont.truetype("arial.ttf", 16)
                except:
                    font = ImageFont.load_default()
                
                # Draw each detection
                for i, detection in enumerate(detections):
                    bbox = detection['bbox']
                    confidence = detection['confidence']
                    label = detection.get('label', 'human')
                    
                    # Choose color based on confidence and threat level
                    threat_level = detection.get('threat_level', 'low')
                    if threat_level == 'high':
                        color = (255, 0, 0)  # Red for high threat
                    elif threat_level == 'medium':
                        color = (255, 165, 0)  # Orange for medium threat
                    elif confidence > 0.8:
                        color = (0, 255, 0)  # Green for high confidence
                    elif confidence > 0.6:
                        color = (255, 255, 0)  # Yellow for medium confidence
                    else:
                        color = (255, 0, 0)  # Red for low confidence
                    
                    # Draw bounding box
                    draw.rectangle(bbox, outline=color, width=3)
                    
                    # Prepare label text
                    label_text = f"{label} {confidence:.2f}"
                    
                    # Add additional information if available
                    if 'temperature' in detection:
                        label_text += f"\nTemp: {detection['temperature']:.1f}°C"
                    if 'pose' in detection:
                        label_text += f"\nPose: {detection['pose']}"
                    if 'threat_level' in detection:
                        label_text += f"\nThreat: {detection['threat_level']}"
                    if 'estimated_distance' in detection:
                        label_text += f"\nDist: {detection['estimated_distance']:.1f}m"
                    
                    # Draw label background
                    text_bbox = draw.textbbox((bbox[0], bbox[1] - 60), label_text, font=font)
                    draw.rectangle(text_bbox, fill=color)
                    
                    # Draw label text
                    draw.text((bbox[0], bbox[1] - 60), label_text, fill=(255, 255, 255), font=font)
                
                # Save processed image
                base_name = os.path.splitext(image_path)[0]
                ext = os.path.splitext(image_path)[1]
                output_path = f"{base_name}_processed{ext}"
                
                img.save(output_path)
                
                print(f"Drew {len(detections)} detections on {image_path}")
                return output_path
            
        except Exception as e:
            print(f"Error drawing detections: {e}")
            # Fallback: just copy the original image
            import shutil
            base_name = os.path.splitext(image_path)[0]
            ext = os.path.splitext(image_path)[1]
            output_path = f"{base_name}_processed{ext}"
            shutil.copy2(image_path, output_path)
            return output_path
    
    def generate_safety_report(self, robot_data, gas_history):
        """Generate comprehensive safety report with enhanced analytics"""
        try:
            # Get latest data
            latest_data = robot_data[0] if robot_data else {}
            
            # Analyze current gas levels
            current_mq2 = latest_data.get('mq2_gas_level', 0)
            current_mq135 = latest_data.get('mq135_air_quality', 0)
            
            # Specific gas data if available
            specific_gases = {}
            for gas_type in ['methane_ppm', 'lpg_ppm', 'smoke_ppm', 'hydrogen_ppm', 'alcohol_ppm']:
                if gas_type in latest_data:
                    specific_gases[gas_type.replace('_ppm', '')] = latest_data[gas_type]
            
            gas_analysis = self.analyze_gas_levels(current_mq2, current_mq135, specific_gases)
            
            # Pattern analysis if we have history
            pattern_analysis = {}
            if len(gas_history) > 5:
                pattern_analysis = self.detect_gas_patterns(gas_history)
            
            # Emergency status
            emergency_mode = latest_data.get('emergency_mode', False)
            
            report = {
                'report_timestamp': datetime.now().isoformat(),
                'report_id': f"SR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'executive_summary': self._generate_executive_summary(gas_analysis, emergency_mode),
                'current_conditions': {
                    'location': {
                        'latitude': latest_data.get('latitude', 0),
                        'longitude': latest_data.get('longitude', 0),
                        'gps_valid': latest_data.get('gps_valid', False),
                        'satellites': latest_data.get('satellites', 0)
                    },
                    'environmental': {
                        'temperature': latest_data.get('temperature', 0),
                        'system_health': latest_data.get('system_healthy', True),
                        'battery_level': latest_data.get('battery_level', 0)
                    },
                    'gas_levels': gas_analysis,
                    'emergency_status': emergency_mode
                },
                'historical_analysis': pattern_analysis,
                'risk_assessment': self._generate_comprehensive_risk_assessment(gas_analysis, pattern_analysis, latest_data),
                'recommendations': self._generate_detailed_recommendations(gas_analysis, pattern_analysis, emergency_mode),
                'emergency_procedures': self._generate_emergency_procedures(gas_analysis['overall_safety']),
                'monitoring_requirements': self._generate_monitoring_requirements(gas_analysis),
                'regulatory_compliance': self._check_regulatory_compliance(gas_analysis)
            }
            
            return report
            
        except Exception as e:
            return {"error": f"Report generation error: {e}"}
    
    def _generate_executive_summary(self, gas_analysis, emergency_mode):
        """Generate comprehensive executive summary"""
        safety_status = gas_analysis.get('overall_safety', 'unknown')
        risk_level = gas_analysis.get('risk_level', 0)
        
        if emergency_mode:
            return "🚨 EMERGENCY SITUATION: Robot has activated emergency mode due to multiple hazard detection. Immediate response required."
        elif safety_status == 'critical':
            return "🔴 CRITICAL: Life-threatening gas levels detected. Immediate evacuation and emergency response required."
        elif safety_status == 'dangerous':
            return "🟠 DANGER: Hazardous gas levels detected. Area evacuation and safety measures required immediately."
        elif safety_status == 'caution':
            return "🟡 CAUTION: Elevated gas levels require monitoring and limited exposure with safety precautions."
        elif safety_status == 'elevated':
            return "🔵 NOTICE: Gas levels slightly elevated but within acceptable ranges with continued monitoring."
        else:
            return "🟢 SAFE: All gas levels are within normal parameters. Continue standard monitoring procedures."
    
    def _generate_comprehensive_risk_assessment(self, gas_analysis, pattern_analysis, latest_data):
        """Generate detailed risk assessment"""
        assessment = {
            'overall_risk_score': gas_analysis.get('risk_level', 0),
            'fire_explosion_risk': gas_analysis.get('mq2_analysis', {}).get('fire_risk', 'low'),
            'health_risk': gas_analysis.get('mq135_analysis', {}).get('health_impact', 'none'),
            'environmental_factors': gas_analysis.get('environmental_factors', {}),
            'immediate_threats': self._identify_immediate_threats(gas_analysis, latest_data),
            'long_term_concerns': self._identify_long_term_concerns(gas_analysis, pattern_analysis),
            'vulnerable_populations': self._assess_vulnerable_populations(gas_analysis),
            'business_continuity_impact': self._assess_business_impact(gas_analysis)
        }
        
        return assessment
    
    def _generate_detailed_recommendations(self, gas_analysis, pattern_analysis, emergency_mode):
        """Generate comprehensive recommendations"""
        recommendations = gas_analysis.get('recommendations', [])
        
        # Add pattern-based recommendations
        if pattern_analysis and 'recommendations' in pattern_analysis:
            recommendations.extend(pattern_analysis['recommendations'])
        
        # Add emergency-specific recommendations
        if emergency_mode:
            recommendations.extend([
                'Activate emergency response team',
                'Implement crisis communication plan',
                'Document all emergency actions',
                'Coordinate with local authorities'
            ])
        
        # Add general safety recommendations
        risk_level = gas_analysis.get('risk_level', 0)
        
        if risk_level >= 6:
            recommendations.extend([
                'Install additional gas detection systems',
                'Establish emergency evacuation procedures',
                'Train personnel on emergency response',
                'Maintain emergency equipment inventory',
                'Establish communication with emergency services'
            ])
        elif risk_level >= 4:
            recommendations.extend([
                'Increase monitoring frequency',
                'Improve ventilation systems',
                'Conduct safety training',
                'Review emergency procedures',
                'Implement buddy system for personnel'
            ])
        elif risk_level >= 2:
            recommendations.extend([
                'Regular equipment maintenance',
                'Periodic safety inspections',
                'Update safety documentation',
                'Monitor trending data'
            ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _generate_emergency_procedures(self, safety_status):
        """Generate emergency procedures based on safety status"""
        procedures = {
            'immediate_actions': [],
            'evacuation_procedures': [],
            'communication_plan': [],
            'medical_response': [],
            'incident_documentation': []
        }
        
        if safety_status in ['critical', 'dangerous']:
            procedures['immediate_actions'] = [
                'Sound alarm immediately',
                'Shut down non-essential electrical equipment',
                'Activate emergency lighting',
                'Initiate evacuation procedures',
                'Contact emergency services'
            ]
            
            procedures['evacuation_procedures'] = [
                'Use designated evacuation routes',
                'Proceed to assembly points',
                'Account for all personnel',
                'Do not use elevators',
                'Assist those needing help'
            ]
            
            procedures['communication_plan'] = [
                'Notify all personnel via emergency system',
                'Contact facility management',
                'Inform local emergency services',
                'Update stakeholders on situation',
                'Coordinate with neighboring facilities'
            ]
            
            procedures['medical_response'] = [
                'Assess personnel for exposure symptoms',
                'Provide first aid as needed',
                'Call medical emergency services',
                'Document any injuries or exposures',
                'Provide exposure information to medical personnel'
            ]
            
        procedures['incident_documentation'] = [
            'Record time and nature of incident',
            'Document gas levels and readings',
            'List personnel present and actions taken',
            'Photograph conditions if safe to do so',
            'Preserve all monitoring data'
        ]
        
        return procedures
    
    def _generate_monitoring_requirements(self, gas_analysis):
        """Generate monitoring requirements based on risk level"""
        risk_level = gas_analysis.get('risk_level', 0)
        
        requirements = {
            'monitoring_frequency': 'standard',
            'calibration_schedule': 'monthly',
            'data_retention': '1_year',
            'alert_thresholds': 'standard',
            'personnel_requirements': 'trained_operator'
        }
        
        if risk_level >= 8:
            requirements.update({
                'monitoring_frequency': 'continuous_with_redundancy',
                'calibration_schedule': 'weekly',
                'data_retention': '5_years',
                'alert_thresholds': 'enhanced_sensitivity',
                'personnel_requirements': 'certified_gas_technician'
            })
        elif risk_level >= 6:
            requirements.update({
                'monitoring_frequency': 'continuous',
                'calibration_schedule': 'bi_weekly',
                'data_retention': '3_years',
                'alert_thresholds': 'high_sensitivity',
                'personnel_requirements': 'trained_specialist'
            })
        elif risk_level >= 4:
            requirements.update({
                'monitoring_frequency': 'every_15_minutes',
                'calibration_schedule': 'weekly',
                'data_retention': '2_years',
                'alert_thresholds': 'moderate_sensitivity',
                'personnel_requirements': 'certified_operator'
            })
        
        return requirements
    
    def _check_regulatory_compliance(self, gas_analysis):
        """Check regulatory compliance status"""
        compliance = {
            'occupational_safety': 'compliant',
            'environmental_regulations': 'compliant',
            'fire_safety_codes': 'compliant',
            'building_codes': 'compliant',
            'reporting_requirements': []
        }
        
        risk_level = gas_analysis.get('risk_level', 0)
        
        if risk_level >= 8:
            compliance.update({
                'occupational_safety': 'non_compliant_critical',
                'environmental_regulations': 'requires_immediate_reporting',
                'fire_safety_codes': 'emergency_response_required',
                'reporting_requirements': [
                    'Immediate notification to regulatory authorities',
                    'Incident report within 24 hours',
                    'Corrective action plan within 72 hours',
                    'Follow-up monitoring report'
                ]
            })
        elif risk_level >= 6:
            compliance.update({
                'occupational_safety': 'non_compliant',
                'reporting_requirements': [
                    'Incident notification required',
                    'Investigation report needed',
                    'Corrective action plan required'
                ]
            })
        elif risk_level >= 4:
            compliance['reporting_requirements'] = [
                'Document incident in safety log',
                'Review safety procedures',
                'Consider preventive measures'
            ]
        
        return compliance
    
    def _identify_immediate_threats(self, gas_analysis, latest_data):
        """Identify immediate threats from gas analysis"""
        threats = []
        
        mq2_risk = gas_analysis.get('mq2_analysis', {}).get('risk_level', 0)
        mq135_risk = gas_analysis.get('mq135_analysis', {}).get('risk_level', 0)
        emergency_mode = latest_data.get('emergency_mode', False)
        
        if mq2_risk >= 8:
            threats.append('Imminent fire/explosion risk from combustible gases')
        if mq135_risk >= 8:
            threats.append('Life-threatening toxic exposure risk')
        if mq2_risk >= 6 and mq135_risk >= 6:
            threats.append('Multiple gas hazards present simultaneously')
        if emergency_mode:
            threats.append('Robot emergency mode indicates multiple hazard conditions')
        
        # Check for motion detection during gas emergency
        if latest_data.get('motion_detected') and (mq2_risk >= 6 or mq135_risk >= 6):
            threats.append('Personnel detected in hazardous gas environment')
        
        return threats
    
    def _identify_long_term_concerns(self, gas_analysis, pattern_analysis):
        """Identify long-term concerns from analysis"""
        concerns = []
        
        mq2_risk = gas_analysis.get('mq2_analysis', {}).get('risk_level', 0)
        mq135_risk = gas_analysis.get('mq135_analysis', {}).get('risk_level', 0)
        
        if mq2_risk >= 4:
            concerns.append('Potential chronic combustible gas exposure')
        if mq135_risk >= 4:
            concerns.append('Air quality degradation affecting long-term health')
        
        if pattern_analysis:
            if pattern_analysis.get('trend_analysis', {}).get('mq2_trend') == 'increasing':
                concerns.append('Worsening combustible gas conditions over time')
            if pattern_analysis.get('trend_analysis', {}).get('mq135_trend') == 'increasing':
                concerns.append('Deteriorating air quality trend')
            if pattern_analysis.get('predictions', {}).get('risk_probability', 0) > 0.5:
                concerns.append('High probability of future dangerous conditions')
        
        if mq2_risk >= 2 or mq135_risk >= 2:
            concerns.append('Need for continuous monitoring and maintenance')
        
        return concerns
    
    def _assess_vulnerable_populations(self, gas_analysis):
        """Assess impact on vulnerable populations"""
        risk_level = gas_analysis.get('risk_level', 0)
        
        if risk_level >= 6:
            return {
                'elderly': 'high_risk',
                'children': 'high_risk',
                'pregnant_women': 'high_risk',
                'respiratory_conditions': 'extreme_risk',
                'heart_conditions': 'high_risk'
            }
        elif risk_level >= 4:
            return {
                'elderly': 'moderate_risk',
                'children': 'moderate_risk',
                'pregnant_women': 'moderate_risk',
                'respiratory_conditions': 'high_risk',
                'heart_conditions': 'moderate_risk'
            }
        else:
            return {
                'elderly': 'low_risk',
                'children': 'low_risk',
                'pregnant_women': 'low_risk',
                'respiratory_conditions': 'moderate_risk',
                'heart_conditions': 'low_risk'
            }
    
    def _assess_business_impact(self, gas_analysis):
        """Assess business continuity impact"""
        risk_level = gas_analysis.get('risk_level', 0)
        
        impact = {
            'operational_status': 'normal',
            'evacuation_required': False,
            'equipment_shutdown': False,
            'estimated_downtime': 'none',
            'financial_impact': 'minimal'
        }
        
        if risk_level >= 8:
            impact.update({
                'operational_status': 'emergency_shutdown',
                'evacuation_required': True,
                'equipment_shutdown': True,
                'estimated_downtime': '24-72_hours',
                'financial_impact': 'severe'
            })
        elif risk_level >= 6:
            impact.update({
                'operational_status': 'partial_shutdown',
                'evacuation_required': True,
                'equipment_shutdown': True,
                'estimated_downtime': '4-24_hours',
                'financial_impact': 'significant'
            })
        elif risk_level >= 4:
            impact.update({
                'operational_status': 'restricted_operations',
                'evacuation_required': False,
                'equipment_shutdown': False,
                'estimated_downtime': '1-4_hours',
                'financial_impact': 'moderate'
            })
        
        return impact