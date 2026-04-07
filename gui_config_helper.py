import json
from serialConnection import default_config as serial_default_config

def verify_int_input(prompt_str):
    v_flag = False
    while not v_flag:
        temp = input(prompt_str)
        try:
            temp = int(temp)
            v_flag = True
        except:
            print("Must be integer")        

    print(">>"+str(temp))
    return temp

def verify_float_input(prompt_str):
    v_flag = False
    while not v_flag:
        temp = input(prompt_str)
        try:
            temp = float(temp)
            v_flag = True
        except:
            print("Must be convertable to float")        

    print(">>"+str(temp))
    return temp

def verify_plot_input(plot_num):
    v_flag = False
    while not v_flag:
        temp = input("Which plot 1-" +str(plot_num)+":")
        try:
            temp = int(temp)
        except:
            print("Must be integer")
        if temp > plot_num: print("Out of range")
        else: v_flag = True

    print(">>"+str(temp))
    return temp

def verify_from_list(user_prompt, options_list,use_index = False):
    v_flag = False
    print("Select from options:")
    for i,option in enumerate(options_list):
        print(str(i)+":"+option)
    while not v_flag:

        ind = input(user_prompt)
        try:
            ind = int(ind)
            temp = options_list[ind]
            v_flag = True
        except:
            print("Must be int from selection") 
    if use_index:return ind
    else: return temp 

def bool_prompt(user_prompt):
    temp = input(user_prompt + " Y/n? ")
    if temp == "Y": return True
    else: return False

filename = input("config filename: ") + ".json"
print(">>"+filename)

savefilename = input("save filename: ")
print(">>"+savefilename + ".csv")

config_dict = {}
config_dict["serial"]=serial_default_config.copy()
config_dict["plotting"]={}

serial_baud_rate = verify_int_input("Serial Baud Rate: ")
config_dict["serial"]["baud rate"]=serial_baud_rate

if bool_prompt("See advanced serial settings"):
    parity_list= ["None","Even","Odd","Mark","Space"]
    config_dict["serial"]["parity"]=verify_from_list("Parity: ",parity_list)
    stop_list=["1","1.5","2"]
    config_dict["serial"]["stop bit"]=verify_from_list("Stop bit: ",stop_list)
    bits = ["5","6","7","8"]
    config_dict["serial"]["bits"]=verify_from_list("Bytesize: ",bits)
    config_dict["serial"]["timeout"]=verify_int_input("timeout")
    
      
channel_num = verify_int_input("Number of Data Channels: ")
config_dict["channel_num"] = channel_num

plot_num = verify_int_input("Number of Plots: ")
config_dict["plotting"]["plot_num"] = plot_num

config_dict["savefile"] = savefilename


config_dict["data"] = {}
print(config_dict)


default_plot = {
            "active": False,
            "name" : None,
            "plot num" : None,
            "color" : "r",
            "linestyle" : "",
            "buffersize": None,
            "displaytime": None
}

default_range = {
            "active": False,
            "low" : None,
            "high" : None

}

default_parse = {
            "active":False,
            "type": None,
            "start": None,
            "stop": None

}


for i in range(channel_num):
    channel_name = input("Channel "+str(i)+" Name: ")
    config_dict["data"][channel_name]={}
    plotting = input("Plot? Y/n: ")
    config_dict["data"][channel_name]["plotting"] = dict(default_plot)
    if plotting == "Y":
        config_dict["data"][channel_name]["plotting"]["active"]= True
        
        legend_name = input("name for legend: ")
        config_dict["data"][channel_name]["plotting"]["name"]= legend_name

        buffer_size = verify_int_input("Buffer Size: ")
        config_dict["data"][channel_name]["plotting"]["buffersize"]=buffer_size
        
        plot = verify_plot_input(plot_num)
        config_dict["data"][channel_name]["plotting"]["plot num"] = plot

        displaytime = verify_int_input("Time to display [seconds]: ")
        config_dict["data"][channel_name]["plotting"]["displaytime"]=displaytime

    range_check = input("Check Range? Y/n: ")
    config_dict["data"][channel_name]["range"] = dict(default_range)
    if range_check == "Y":
        config_dict["data"][channel_name]["range"]["active"] = True
        
        range_low = verify_float_input("Low Range Limit: ")
        config_dict["data"][channel_name]["range"]["low"] = range_low

        range_high = verify_float_input("High Range Limit: ")
        config_dict["data"][channel_name]["range"]["high"] = range_high

    
    parse = input("Parse Channel? Y/n: ")
    config_dict["data"][channel_name]["parse"] = dict(default_parse)
    if parse == "Y":
        config_dict["data"][channel_name]["parse"]["active"] = True
        parse_types = ["Scale Parse kg","Strip \\n","Scale Parse g","unallocated","unallocated","unallocated"]
        config_dict["data"][channel_name]["parse"]["type"] = verify_from_list("Parse Type: ",parse_types,use_index=True)     


with open(filename,"w") as json_file:
    json.dump(config_dict,json_file,indent=4)




