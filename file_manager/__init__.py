VERSION = (1, 0, 0, 'rc', 1)

def get_version():
    version = '%s.%s.%s %s' % (VERSION[0], VERSION[1], VERSION[2], VERSION[3]) 
    
    if VERSION[3] != 'final':
        version = '%s %s' % (version, VERSION[4])

    return version

