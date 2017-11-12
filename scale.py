# Weigh scale simulator
# Simulates scale output from the Health o meter 349KLX-AA
# written and tested with version 2.7.13
#
# Gary Marrs
# 11-5-17

import serial
import time
from Tkinter import *

class Application(Frame):
    """ GUI application which simulates weigh scale output """ 
    def __init__(self, master):
        """ Initialize the frame. """
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create button, text, and text box widgets. """
        # create instruction label
        self.inst_lbl = Label(self, text = "Weigh Scale Simulator")
        self.inst_lbl.grid(row = 0, column = 0, columnspan = 2, sticky = W)

        # create label to enter weight
        self.ew_lbl = Label(self, text = "Enter Weight: ")
        self.ew_lbl.grid(row = 1, column = 0, sticky = W)

        # create text box to accept weight      
        self.ew_ent = Entry(self)
        self.ew_ent.grid(row = 1, column = 1, sticky = W)
        
        # create label for entry error      
        self.sv = StringVar()
        self.error_lbl = Label(self, textvariable= self.sv)
        self.error_lbl.grid(row = 2, column = 1, sticky = W)
        self.sv.set("Enter Weight as xxx.x")
        
        # create submit button
        self.submit_bttn = Button(self, text = "Submit", command = self.send)
        self.submit_bttn.grid(row = 3, column = 1, sticky = W)

        # create text widget to display message
        self.send_txt = Text(self, width = 35, height = 5, wrap = WORD)
        self.send_txt.grid(row = 5, column = 0, columnspan = 2, sticky = W)
        
        # create label for weight Send     
        self.sv2 = StringVar()
        self.send_lbl = Label(self, textvariable= self.sv2)
        self.send_lbl.grid(row = 6, column = 0, columnspan=2,sticky = W)
        self.sv2.set("")

    def get_weight(self, e_weight):                     # e_weight is the user entered weight as a string 
        string_weight = "000.0"
        if e_weight == "" or e_weight == "0":
            return "000.0"
        if (float(e_weight))>999.9:                             # make sure number is under 1,000
            o_string = e_weight + " weight is too heavy, xxx.x"
            self.sv.set(o_string)
            self.ew_ent.delete(0, len(e_weight))                # clear text box
            print "over weight"
        else:
            self.sv.set("Enter Weight as xxx.x")
            o2_string =  "Sending weight = " + e_weight
            self.sv2.set(o2_string)
            self.ew_ent.delete(0, len(e_weight))                # clear text box
            f_weight = float(e_weight)                          # convert f_weight to a floating decimal
            f_weight = round(f_weight, 1)                       # so it can be rounded to 1 deciaml place
            # print "rounded ", f_weight
            string_weight = str(f_weight)                       # convert massaged weight back to a string
        
        return string_weight                                    # return weight as a string
    
    
    def send(self):
        """ send serial string out serial port """
        ser = serial.Serial(port='COM1', baudrate=2400, timeout =1)
        ser.isOpen()
        
        # get weight and error check
        contents = self.ew_ent.get()                    # contents is a string
        s_weight = self.get_weight(contents)            # s_weight is string value of weight
        print "s_weight", s_weight
        if s_weight == "0" or s_weight == "0.0":
            vweight = ["0", "0", "0", ".", "0"]
        else:
            vweight = list(s_weight)                        # create list of each char - vweight
        
        #print "len = ", vweight
        print "vweight = ", vweight
        
        #create serial packet
        packet = bytearray()
        packet.append(0x02)
        packet.append(0x80)
        packet.append(0xD7)
        packet.append(0xE4)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x2E)
        packet.append(0x30)
        packet.append(0x0D)
        
        ser.write(packet)                               # send initial packet
        
        packet[4] = vweight[0]
        packet[5] = vweight[1]
        packet[6] = vweight[2]
        packet[8] = vweight[4]

        #self.ew_ent.delete(0.0, END)
        
        self.send_txt.insert(0.0, contents)             # write weight to text box
        
        if (int(float(s_weight)) != 0):                 # make sure weight is not 0
            for x in range(0,3):                        # loop x times
                time.sleep(1)
                ser.write(packet)                       # write packet once per second
        
        
# main
root = Tk()
root.title("Weigh Scale Simulator")
root.geometry("350x250")

app = Application(root)

root.mainloop()
