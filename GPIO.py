#!/usr/bin/env python3
###############################################################################
# Program   : GPIO.py
# Created by: Derek Ripper
# Date      : 16 Jan 2016
# Modified  : 04 Feb 2016 
# Purpose: To read input status of a GPIO pin AND SEND
#          EMAIL WITH STATUS OF pin. Used for Boiler Lockout status.
#
# 04 Feb 2016 - add code for float switch in sewer manhole No 1
#               Achieve make pin reading routine into a class so that it is
#               easy to add more checks in future.
#
###############################################################################
# 10 June 2016 at cottage
# change poll from 1 to 10 secs
# change PiID to #1
# Change still alive emails to 4 hours (14400 secs)# 10 June 2016 at cottage
###############################################################################
# 8 Aug 2016 - Changes made at Home :
# 0 - Rename to Version 3 and write to log file!!
# 1 - add facility for mutilple attachments from a common folder
# 2 - also reorderd commands and corrected error checking message
# 3-  Added temperature sensor code for first time
#     based on 1-wire network- default pin has not been used and moved to BCM pin 22 (Pi pin 15)
#     (see /boot/config.txt where 1-wire code has been added)
# 4 - Now wil be launched by bash script (runit.bsh)  so that std out and err can be captured.
#
# 21 September 2016 changes  - Mk 4  Installed in Cottage 10/09/2016
#  1 New vero board made up to replace the 2 mini breadboards - same functionallioty except
#       - added polling led to give visible indication that program is still alive
#
#  2 Temp sensor id's changed to those used with new vero board I/F
#  3 New - log added exclusive to temperature values
#        & have removed temperature entries in  main GPIO.log
#  4 corrected KeepAlive msg as "cottage" hard coded 
#    - also now just says OK in email subject.
#    - email "subject" now shows "ok" or "failure" status for sensors
###############################################################################
# 06 Dec 2016
# 0 - update Program name to Mk5
# 1 - added version to DU utils but still import as DU 
###############################################################################
# 08 Jan 2018
# 0 - Fix undefined variable msg that only results from instantiating the email
#     object. Alas looks like this was only a problem with a CTRL-C interupt
#     ie not in normal running.
###############################################################################
# 12 Apr 2018  Installed at cottage w/c 18 June 2018
#
# 1 - Add "read config" file added for Pi name and sensor ID's
#
# 2 - debug for random hangs -- Cause was SMTP not returning control
#     Fixed by adding smtp timeout of 10 seconds!
#
# 3 - New cable with dupont 2x6 connector at Pi computer end   
#     "GRD" and LED "ALIVE" leads  moved into this connector
#
# 4 - Removed s/w Pull Up on GPIO Output definition
#     as class code common for all GPIO scenarios it was applied to sewer sensor
#     Not wrong but not necessary. Now done in HARDWARE with 10Kohmn resistor
#
# 5 - Updated gpio_input_status (the check method) to allow a pin to be defined    
#     as HIGH or LOW for a fault condition  
#
# 6   Code module renamed to GPIO.py - ie have dropped the Version as code
#     is now in GITHub as at 8 June 2018 (also true for DU.py)
#######################################################################
# 16 Jan 2020
# 1 - start up delay increase to 4 mins from 3mins. needed as new sky router
#     takes longer to boot so we dont  miss the first generated email at Pi 
#     boot up.
# 2 - change boiler sensor to water level sensor. logic is inverted.
###############################################################################
import os
import smtplib
from email                import encoders
from email.mime.base      import MIMEBase
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
    
def SendEMail(bodytext, Device,  ElapsedTime):	

    smtpServer,smtpPort,smtpTimeout,emailAddress,emailPassword = emailCreds()
    #xsmtp = repr(smtpServer)
    #o_LOG.write("server :"+xsmtp)
    #xport = repr(smtpPort)
    #o_LOG.write("port   :"+xport)
    #xtime = repr(smtpTimeout)
    #o_LOG.write("timeout:"+xtime)
    #xmail = repr(emailAddress)
    #o_LOG.write("email  :"+xmail)
    #xpw = repr(emailPassword)
    #o_LOG.write("pw     :"+xpw)
        
    SMTP_SERVER    = smtpServer
    SMTP_PORT      = smtpPort
    SMTP_TIMEOUT   = smtpTimeout
    EMAIL_USERNAME = emailAddress
    EMAIL_PASSWORD = emailPassword 
    
    EMAIL_RECIPIENT      = 'derek.ripper@gmail.com'
  
    # Create the enclosing (outer) message
    outer = MIMEMultipart('mixed')
    outer['Subject'] = 'Msg from: '+ Device
    outer['From']    =  EMAIL_USERNAME
    outer['To']      =  EMAIL_RECIPIENT
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
     
    # gather tech info and  append to body text in email
    bodytext = GetInfo(bodytext)
    content  = MIMEText(bodytext,'plain')
 
    outer.attach(content)
     
    # add multiple attachments from a single defined folder
    # dir = "/home/pi/Documents/Live/logs/"
    dir = o_LOG.GetLogDirName()	
    attachments = ()  # empty list
    attachments = os.listdir(dir)
   
    for file in attachments:
     file = os.path.join(dir,file)
     
     try:  
        with open(file,'rb') as fh:
           msg = MIMEBase('application',"octet-stream")
           msg.set_payload(fh.read())
		   
        encoders.encode_base64(msg)	
        msg.add_header('Content-Disposition','attachment',
        filename=os.path.basename(file))	
        outer.attach(msg)
     except:   
        print("Attachment Error: "+sys.exc_info()[0])    
          
    composed = outer.as_string()
    
    # Now try and  send completed mail with attachments    
    try:
      session = None
      lmsg    = "ERROR - Undefined message"
    
      o_LOG.write("***** Before smtp setup session")
      session = smtplib.SMTP( host=SMTP_SERVER, port=SMTP_PORT, timeout=SMTP_TIMEOUT)    
      o_LOG.write("***** After  smtp setup session")
	  #added Mon 24/04/2018
      session.set_debuglevel(0) # 0= not active, 1=log, 2=log with date/time

      session.ehlo()
      session.starttls()
      session.ehlo
	  
      session.login   (EMAIL_USERNAME, EMAIL_PASSWORD)
      session.sendmail(EMAIL_USERNAME,EMAIL_RECIPIENT, composed)

  
      lmsg = "No exceptions detected from smtplib processing"  
    
    except KeyboardInterrupt:
        lmsg = "Err_00: smtplib.smtp() did not return control!"    
    except smtplib.SMTPServerDisconnected :
        lmsg = "Err_01: smtplib.SMTPServerDisconnected"
    except smtplib.SMTPResponseException as e:
        lmsg = "Err_02 : " + "smtplib.SMTPResponseExceptiosqn: " + str(e.smtp_code) + " " + str(e.smtp_error)
    except smtplib.SMTPSenderRefused:
        lmsg = "Err_03: smtplib.SMTPSenderRefused"
    except smtplib.SMTPRecipientsRefused:
        lmsg = "Err_04: smtplib.SMTPRecipientsRefused"
    except smtplib.SMTPDataError:
        lmsg = "Err_05: smtplib.SMTPDataError"
    except smtplib.SMTPConnectError:
        lmsg = "Err_06: smtplib.SMTPConnectError"
    except smtplib.SMTPHeloError:
        lmsg = "Err_07: smtplib.SMTPHeloError"
    except smtplib.SMTPAuthenticationError:
        lmsg = "Err_08: smtplib.SMTPAuthenticationError"
    except Exception :
        lmsg = "Err_09: Exception in handling SMTPLIB - Typically NO NETWORK or No reponse from SMTP host!"
    
    finally:
      if session != None:
          o_LOG.write(lmsg)
          # check lmsg is not error related!"
          if (lmsg.find("Err") >= 0 ):
             o_LOG.write("ERROR: Email NOT Sent ! - Quit SMTPLIB object for: " + Device)
          else:
             o_LOG.write("INFO:  Email Sent ! - Quit SMTPLIB object for: " + Device)
             
          o_LOG.write("*****pre  session quit() method")
          try:
            session.quit()
          except:
            # session object can still exists after an smtp related error 
            o_LOG.write("*****FAILED! Unable to execute session.quit() ")
            
          o_LOG.write("*****post session quit() method\n")
      else:
          o_LOG.write("FAILED! SMTPLIB object not instantiated for: " + Device)
          o_LOG.write(lmsg)
          o_LOG.write("")

###############################################################################    
def emailCreds():
    filename = os.environ['RASPPI_DATA']
    
    try:
        o_LOG.write("EMAIL DATA  FILE: "+filename)
        
        key_file = open(filename,"r")
        smtp_data = key_file.readline()

        server, port, timeout, user, pw = smtp_data.split("=")
	
        key_file.close()
    except:
        o_LOG.write("ERROR - Cannot open file for email credentials: "+filename)
        server = "Unknown"
        port    = "123"
        timeout = "123"
        user    = "No_one"
        pw      = "Not_set"
        
  
    return server.strip(),int(port),int(timeout),user.strip(), pw.strip()

###############################################################################    
def cmdline(command):
    #Execute shell command and capture the answer!
    
    from subprocess import PIPE, Popen
    process = Popen(
        args   = command,
        stdout = PIPE,
        shell  = True
                    )
    return process.communicate()[0]

###############################################################################
def GetInfo(msg):
    
    msg = msg + "\n\n" + "Time since last reboot:"+str(cmdline("uptime -p"))[4:-3]     +"\n"
    msg = msg +          "CPU "+str(cmdline("/opt/vc/bin/vcgencmd measure_temp"))[2:-3]+"\n"
    msg = msg + "\nOn Board Temp: " + str(DU.gettemp("On_Board",o_cfg))+"\n"
    msg = msg +   "External Temp: " + str(DU.gettemp("External",o_cfg))+"\n" 
    msg = msg +   "Inside   Temp: " + str(DU.gettemp("Internal",o_cfg))+"\n"

    return msg
###############################################################################    
def MsgFaultFound(Device):
    msg = Device + " : Failure detected!" +"\n\n"
    msg = msg    +"Time program has been running: " + ElapsedTime
    return msg

###############################################################################
def MsgNoFault(Device):
    msg = Device + " : Checked and OK!" +"\n\n"
    msg = msg    +"Time program has been running: " + ElapsedTime
    return msg

###############################################################################
def MsgEmailKeepAlive(Device):
    msg = Device +" is Alive!" +"\n\n"
    msg = msg    +"Time program has been running: " + ElapsedTime
    return msg

###############################################################################
class gpio_input_status(object):

    #initialise object variables
    def __init__(self, pin, pout, Device, NoFault):
        self.AlertSent = False  # Only send for 1st time a change in GPIO pin state
        self.ReScan    = True   # Indicates that the first Alert has been sent

        self.pin       = pin
        self.pout      = pout
        self.msg       = Device
        self.FaultTest = NoFault
        
        # set appropriate GPIO pin text as we use both conventions
        # ie Logical 1 may be both OK & NOT OK depending on type of sensor
        if(self.FaultTest):
            self.FaultTxtOK     = "HIGH"
            self.FaultTxtNotOK  = "LOW "           
        else:    
            self.FaultTxtOK     = "LOW "
            self.FaultTxtNotOK  = "HIGH"

        if(self.pin == 16):
            GPIO.setup(PIN_E, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
             GPIO.setup(self.pin, GPIO.IN)
             
        GPIO.setup(self.pout,GPIO.OUT)

    def check(self):
        if(GPIO.input(self.pin) == self.FaultTest):
            # NO Fault condition
            if(self.ReScan == True):
                lmsg = "BCM Pin\t" + str(self.pin) + "\tis "+self.FaultTxtOK+" for " + self.msg + "\t- take no action"
                o_LOG.write(lmsg)
                print(lmsg)
                GPIO.output(self.pout, GPIO.LOW)
                SendEMail(MsgNoFault(self.msg), self.msg + " - is OK",ElapsedTime)
                self.AlertSent = False 
                self.ReScan    = False
        else:
            # Fault detected condition
            if(self.AlertSent == False):                
                lmsg = "BCM Pin\t" + str(self.pin) +"\tis "+self.FaultTxtNotOK+" for "+ self.msg + "\t- !!!!!send ALERT msg!!!!!"
                o_LOG.write(lmsg)
                print(lmsg)
                GPIO.output(self.pout, GPIO.HIGH)
                SendEMail(MsgFaultFound(self.msg), self.msg + " - Failure Detected",ElapsedTime)
                self.AlertSent = True
                self.ReScan    = True
                
#end class gpio_input_status(object)            


###############################################################################
# Main Program Starts Here ............
###############################################################################
import RPi.GPIO as GPIO   # Rapberry Pi GPIO support library
import time     as T
import sys
import DU                 # Derek's Utilities
import config   as CFG    # Reads data for site specefic Pi eg: temp sensors, location,etc

# instantiate objects for run
o_cfg     = CFG.ReadConfig('config.txt')

DATA_DIR  = o_cfg.GetConfigValue('DataPath')
LOGS_DIR  = DATA_DIR+"logs/"

o_DT      = DU.c_datetime()
o_LOG     = DU.c_logger(LOGS_DIR,"GPIO_log.txt")
o_TempLOG = DU.c_logger(LOGS_DIR,"Temperature_log.txt")

### In case of recovery from mains power failure
#   allow time for router and TPLink (Ethernet over mains) units to initialise! 
wait2start = 60 * 4 #temp reduction
T.sleep(wait2start)
o_LOG.write("Starting program after a wait of  " + str(wait2start) + " seconds.") 
               
# Set GPIO numbering convention 
GPIO.setmode(GPIO.BCM)

##### Set CONSTANTS
PROGRAM     = "GPIO.py    V6.00"
PI_ID       = o_cfg.GetConfigValue('Pi_Name')
poll        = 12     # pollimg interval in seconds
Ncount      = 0      # Count number of polls
ElapsedTime = 0

# GPIO pin usage ......
PIN_B       = 27     # Pi pin 13 Water level (moved for RTC in Ver Mk4 of s/w)
PIN_S       = 17     # Pi pin 11 Sewer  Flooded ( ditto )
PIN_X       = 10     # Pi pin 19 was Boiler "lockout" - now garage water level Spare
PIN_E       = 16     # Pi pin 36  Used to force an email to be sent


POUT_B      = 24     # Pi pin 18 Water level LED(Red)
POUT_S      = 25     # Pi pin 22 Sewer  LED(Green)
POUT_X      = 23     # Pi pin 16  
POUT_E      =  6     # Pi pin 31  No LED attached to this pin! 


POUT_BLINK  = 18     # Pi pin 12 Flasing LED(Yellow)

# NB 1-wire networking for temperature sensors is on BCM pin 22 (Pi pin 15)
#    As of this version all DS18B20 hex id's  are held in config.txt
#    and read at runtime.

###### Instantiate GPIO checking objects
chk_B = gpio_input_status(PIN_B, POUT_B, PI_ID +"-Water level",False)# False  indicates state of pin in NON-FAULT condition = logical 1 or 3v
chk_S = gpio_input_status(PIN_S, POUT_S, PI_ID +"-SEWER" ,     False)# False sensor chaged 08/09/2023
chk_X = gpio_input_status(PIN_X, POUT_X, PI_ID +"-B.PRESSURE", False)# FALSE indicates state of pin in NON-FAULT condition = logical 0 or 0v
chk_E = gpio_input_status(PIN_E, POUT_E, PI_ID +"-Test Email", False)# FALSE indicates state of pin in NON-FAULT condition = logical 0 or 0v

o_LOG.write("Data from Pi device: " + PI_ID )  
o_LOG.write("Program Name       : " + PROGRAM )  

########################################################################
##### Start main Polling Loop 
try:       
    while True:   
        Ncount      = Ncount +1
        blinktime   = 2
        sleeptime   = poll/3 - blinktime 
        ElapsedTime = o_DT.elapsedtime()
        	
		# write temperature readings to log file every hour

        if(int(poll*Ncount) % 3600 == 0 or Ncount == 1):
            OBtemp = str(DU.gettemp("On_Board",o_cfg))  
            INtemp = str(DU.gettemp("Internal",o_cfg))  
            EXtemp = str(DU.gettemp("External",o_cfg))  
            o_TempLOG.write("On Board: " + OBtemp +" INtemp: " + INtemp +" EXtemp: " + EXtemp)	
        
        # Periodic I'm "ALIVE" email - set to 4 hrs (14400 secs)
        if(int(poll*Ncount) % 14400 == 0 or Ncount == 1):
            o_LOG.write("Heart Beat - Count = " + str(Ncount)+" Elapsed Time: "+ ElapsedTime)
            SendEMail(MsgEmailKeepAlive(PI_ID),PI_ID + " - is ALIVE!",ElapsedTime)
        
        T.sleep(sleeptime)         
        chk_B.check() # Boiler check via neon / LDR
        DU.blink(GPIO, blinktime, POUT_BLINK)  
        
        T.sleep(sleeptime)
        chk_S.check() # Sewer check via mini float switch in manhole
        DU.blink(GPIO, blinktime, POUT_BLINK)  
                
        T.sleep(sleeptime)
        chk_X.check() # ON/OFF sensor -- hopefully for LOW Boiler Pressure switch
        DU.blink(GPIO, blinktime, POUT_BLINK)  
        
        T.sleep(sleeptime)
        chk_E.check() # Used to send a test email - pin control by seperate CL program
        DU.blink(GPIO, blinktime, POUT_BLINK)  

except KeyboardInterrupt:
    print("\nControlled exit!")
    o_LOG.write("User aborted via CTRL-C !")
    GPIO.cleanup()
##### End of main Polling Loop code  
########################################################################





