VERSION = (1, 1, 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1]) 
    
    if VERSION[2] > 0: # BUG Fix releases.
        version = '%s.%s.%s' % (VERSION[0], VERSION[1], VERSION[2]) 

    return version
