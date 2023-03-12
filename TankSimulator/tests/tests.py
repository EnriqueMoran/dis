import cinematicManagerTest

def run_cinematic_tests():
    test = cinematicManagerTest.TestCinematicManager()
    test.test_set_initial_position()
    test.test_set_initial_position_2()
    print("Set initial position tests passed. OK")
    test.test_set_position()
    test.test_set_position_2()
    print("Set position tests passed. OK")
    test.test_set_heading()
    print("Set heading test passed. OK")
    test.test_set_speed()
    print("Set speed test passed. OK")
    
    