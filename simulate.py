import time
def simulate(*args, **kwargs):
    time.sleep(10)
    return 8., 2.

def build_geom(*args, **kwargs):
    print('COMPUTING')
    time.sleep(5)
    print('DONE')

def test(obj):
    if obj.parameters.Height > 10:
        for i in range(5):
            print(f"TESTING TEST SUITE {i}...",end=' ')
            time.sleep(2)
            if i == 3:
                print('FAILED')
            else:
                print('PASSED')
        
        return False, 'The test suite 3 has failed'
    else:
        for i in range(5):
            print(f"TESTING TEST SUITE {i}...",end=' ')
            time.sleep(2)
            print('PASSED')
        return True, None
