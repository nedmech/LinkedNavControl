from settings import debug_mode

def log(msg):
    if not debug_mode:
        return
    try:
        f = open(
            __file__.replace('.pyc', '.py').replace(
                'Logging.py','LinkedNavControl.log'),
            'a')
        f.write(msg+"\n")
        f.close()
    except:
        # Logging is not a critical operation - OK to fail.
        pass
