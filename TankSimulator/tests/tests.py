import kinematicsManagerTest

def run_kinematics_tests():
    test = kinematicsManagerTest.TestKinematicsManager()
    test.test_set_position()
    print("Set position tests passed. OK")
    test.test_set_heading()
    print("Set heading test passed. OK")
    test.test_set_speed()
    print("Set speed test passed. OK")
    
    