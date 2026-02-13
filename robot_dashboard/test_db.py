#!/usr/bin/env python3
"""
Test script to verify database setup works correctly
Run this file to test your database before running the main application
"""

from database import RobotDatabase
import os

def test_database():
    print("🤖 Testing Robot Dashboard Database Setup...")
    print("=" * 50)
    
    try:
        # Initialize database
        print("1. Creating database connection...")
        db = RobotDatabase()
        print("   ✅ Database initialized successfully!")
        
        # Test adding robot data
        print("\n2. Testing robot data insertion...")
        db.add_robot_data(
            lat=6.0329,  # Negombo coordinates
            lon=80.2168,
            front_dist=45.5,
            back_dist=78.2,
            motion=True,
            battery=85.0,
            status="Testing"
        )
        print("   ✅ Robot data added successfully!")
        
        # Test adding detection data
        print("\n3. Testing detection data insertion...")
        db.add_detection(
            detection_type="thermal",
            confidence=0.85,
            lat=6.0329,
            lon=80.2168,
            file_path="test_image.jpg",
            bbox_data=[100, 100, 200, 200]
        )
        print("   ✅ Detection data added successfully!")
        
        # Test adding upload history
        print("\n4. Testing upload history insertion...")
        db.add_upload_history(
            file_name="test_thermal.jpg",
            file_type="thermal",
            result="1 human detected",
            confidence=0.92
        )
        print("   ✅ Upload history added successfully!")
        
        # Test reading data
        print("\n5. Testing data retrieval...")
        robot_data = db.get_recent_data(5)
        detections = db.get_recent_detections(5)
        upload_history = db.get_upload_history(5)
        
        print(f"   📊 Found {len(robot_data)} robot data entries")
        print(f"   🔍 Found {len(detections)} detection entries")
        print(f"   📁 Found {len(upload_history)} upload history entries")
        
        # Display sample data
        if robot_data:
            print("\n6. Sample robot data:")
            latest = robot_data[0]
            print(f"   Timestamp: {latest[1]}")
            print(f"   Location: {latest[2]}, {latest[3]}")
            print(f"   Status: {latest[8]}")
            print(f"   Battery: {latest[7]}%")
        
        print("\n🎉 All database tests passed!")
        print("🚀 Your database is ready for the main application!")
        
        # Check if database file was created
        db_path = "data/robot_data.db"
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"\n📁 Database file created: {db_path}")
            print(f"📏 Database size: {size} bytes")
        
    except Exception as e:
        print(f"\n❌ Database test failed!")
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're in the robot_dashboard folder")
        print("2. Check if the 'data' folder exists")
        print("3. Verify Python has write permissions in this directory")
        print("4. Make sure you installed sqlite3 (usually comes with Python)")
        
        return False
    
    return True

if __name__ == "__main__":
    test_database()
