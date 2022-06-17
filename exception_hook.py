
import sys, traceback

# needed to access my other Pyton std. modules
import sys, os
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))
import DU
o_log = DU.c_logger("/home/pi/dev/logs/","error_hook.log") 

def my_exception_hook(err_type, err_value, err_tb):
    """
    Intended to be assigned to sys.exception as a hook.
    Gives programmer opportunity to do something useful with info from uncaught exceptions.

    Parameters
    type: Exception type
    value: Exception's value
    tb: Exception's traceback
    """
    LF="\n"
    o_log.write(LF)
    o_log.write("'excepthook.sys' CAPTURE UNTRAPPED ERRORS!")

    err_tb_details = "\n".join(traceback.extract_tb(err_tb).format())

    o_log.write("*** ERROR TYPE     :")
    o_log.write(str(err_type))
    o_log.write(LF)
    o_log.write("*** ERROR VALUE    :")
    o_log.write(str(err_value))
    o_log.write(LF)
    o_log.write("*** ERROR TRACEBACK:")
    o_log.write(str(err_tb_details))
    o_log.write("*** ALL DONE IN TRACEBACK ***")
    
    print(LF+"################## ERROR type start")
    print(err_type)
    print(LF+"################## ERROR value start")
    print(err_value)
    print(LF+"################## Traceback start")
    print(err_tb_details)
    print(LF+"################## Traceback finish")


sys.excepthook = my_exception_hook




