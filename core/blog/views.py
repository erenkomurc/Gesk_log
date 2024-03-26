from django.shortcuts import render
import paramiko 
from paramiko import SSHClient
from django.http import HttpResponse
from datetime import datetime

import json
import time
import datetime
import os



# Create your views here.
def parse_timestamp(element):
    return datetime.datetime.strptime(element['timestamp'], '%d.%m.%Y %H:%M:%S')

def RemoteClient(request):
    # try:
        
        selected_gw_id = request.GET.get('selected_gw_id', None)
        selected_node_id = request.GET.get('selected_node_id', None)
        selected_gateway_id = request.GET.get('gateway_id', None)
        selected_filter = request.GET.get('filter', None)
        min_value = request.GET.get('min_value', -99)
        max_value = request.GET.get('max_value', 99)
    

        hostname = '2.56.154.117'
        port = 22
        username = 'root'
        password = 'gesk2017'

        # transport  = paramiko.Transport((hostname, port))
        # transport.connect(username=username, password=password)

        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        # ssh.connect(hostname=hostname, username=username, password=password, port=port, )
        
    # if pub_{gw_id} in filename:
            
      
        context = dict()
        nodes_with_gw_ids= dict()
        gw_ids = set()
        messages = list()
        conf_node_ids = [] 
        selected_conf_node_ids = [] 
        node_ids = []
        interval = list()
        gateway_ids =set()
      
        gateway_messages = []  

        interval = []

    
      
   
        
        
        # local_path = 'logs/pub_083a8d01d0a0_4175154.txt'

        dir = 'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/'

        filename_list = os.listdir(dir)
        # sftp_client = ssh.open_sftp()
        # filename_list = sftp_client.listdir("/root/amazon_dh_logger/")
        for filename in filename_list:
            if 'pub_' in filename:
                gw_id = filename.split('_')[1]
                gw_ids.add(gw_id)
  
            elif 'gateway_' in filename:
                gateway_id = filename.split('_')[1].split('.')[0]
                if gateway_id not in ["discovery", "tasmota"]:
                  gateway_ids.add(gateway_id)
                

        print(f"gateway ids: {gateway_ids}")
        if selected_gw_id==None and selected_node_id ==None:
                    
            selected_gw_id = "083a8d01d068"
            selected_node_id = "5092660"

        print("selected_gateway_id", selected_gateway_id)
        print("selected_node_id", selected_node_id)
          
        
        for gw_id in gw_ids:
            if gw_id not in nodes_with_gw_ids.keys():
                nodes_with_gw_ids[gw_id] = set()
         
            if gw_id == selected_gw_id: 
                for file in filename_list:
                    # print(file)
                    if f"pub_{gw_id}" in file:
                        if "conf" not  in file:            
                            node_id = file.split('_')[2][:7]
                            nodes_with_gw_ids[gw_id].add(node_id)
                            # print(f"dosya: {selected_node_id}")
                            
                        elif "conf" in file and f"pub_{gw_id}_conf" in file:
                            local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/{file}'

                            with open(local_path, 'r') as filea:

                                conf_node_ids = filea.readlines()
                                conf_node_ids.reverse()
                            for line in conf_node_ids:
                           
                              line_for_json = line.split('|')[1]
                              line_json = json.loads(line_for_json)
                              line_json['timestamp'] = line.split('|')[0]
                            
                            interval.append(line_json)
                            # print(f"interval: {line_json}")
                            # print(type(line_json))
                        
                               # for line in conf_node_ids:
                        #     parts = line.split('|')
                        #     timestamp = parts[0]
                        #     line_for_json = parts[1]
                            
                        #     line_json = json.loads(line_for_json)
                        #     line_json['timestamp'] = timestamp
                            
                        #     print(line_json)
                            
                        if gw_id not in nodes_with_gw_ids.keys():
                            nodes_with_gw_ids[gw_id] = set()
                            nodes_with_gw_ids[gw_id].add(node_id)
                            print(f"dosya:{selected_node_id}")
                         

                    elif f"gateway_" in file:
                                local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/gateway_{selected_gw_id}.json'
                                print(f"Reading file: {local_path}")
                              
                                try:
                                    with open(local_path, 'r') as filea:
                                        jsonData = json.loads(filea.read())
                                        gateway_messages.append(jsonData)  
                                except Exception as e:
                                    print(f"Error reading file {local_path}: {e}")

                                    print(f"messages: {gateway_messages}")

            

                
                       
                      
        
        if (selected_gw_id):
            context['selected_gw_id'] = selected_gw_id
            
            context['node_ids'] = nodes_with_gw_ids[selected_gw_id]
            context['node_ids'].add("all")
            if (selected_node_id):
                if selected_node_id == "all":
                    context['selected_node_id'] = "all"
                    for node_id in nodes_with_gw_ids[selected_gw_id]:
                        if node_id != "all":
                            
                            # remote_path = f'/root/amazon_dh_logger/pub_{selected_gw_id}_{node_id}.txt'
                            local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/pub_{selected_gw_id}_{conf_node_ids}.txt'
                            
                            with open(local_path, "r") as filea:
                                # filea = sftp_client.file(remote_path, "r")
                                all_message = filea.readlines()
                                all_message.reverse()
                                for line in all_message:
                                    line_for_json = line.split('|')[1]
                                    line_json = json.loads(line_for_json)
                                    line_json['timestamp'] = line.split('|')[0]

                                    if not selected_filter:
                                        messages.append(line_json)
                                    else:
                                        if line_json[selected_filter] >= float(min_value) and line_json[selected_filter] <= float(max_value):
                                            messages.append(line_json)
                                    
                        else:
                            continue 
                else:
                    context['selected_node_id'] = selected_node_id
                    # remote_path = f'/root/amazon_dh_logger/pub_{selected_gw_id}_{selected_node_id}.txt'
                    local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/pub_{selected_gw_id}_{selected_node_id}.txt'
                    with open(local_path, "r") as filea:
                        # filea = sftp_client.file(remote_path, "r")
                        all_message = filea.readlines()
                        all_message.reverse()
                        for line in all_message:
                            line_for_json = line.split('|')[1]
                            line_json = json.loads(line_for_json)
                            line_json['timestamp'] = line.split('|')[0]
                            if not selected_filter:
                                messages.append(line_json)
                            else:
                           
                                if line_json[selected_filter] >= float(min_value) and line_json[selected_filter] <= float(max_value):
                                    messages.append(line_json)

            else:
                    # remote_path = f'/root/amazon_dh_logger/gateway_{selected_gw_id}.json'
                    local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/gateway_{selected_gw_id}.json'
                    try:
                        with open(local_path, "r") as filea:
                            all_message = filea.read()
                            nodes_data = json.loads(all_message)
                            print(nodes_data)
                            for node_data in nodes_data.values():
                                print("node data: ", node_data)
                                # if node_data.get("timestamp"):
                                #     messages.append({
                                #         "timestamp": "",
                                #         "id": "",
                                #         "temp": "",
                                #         "hum": "",
                                #         "rxRssi": "",
                                #         "txRssi": "",
                                #         "battery": ""
                                #     })
                                # else:
                                messages.append(node_data)
                    except Exception as e:
                            print(f"Error reading file {local_path}: {e}")

        if selected_node_id == "all":
            sorted_elements = sorted(messages, key=parse_timestamp)
            if not selected_filter:
                context['all_message'] = reversed(sorted_elements[-100:])
            else:
                context['all_message'] = reversed(sorted_elements)
        else :
            context['all_message'] = messages
        context['gw_ids'] = gw_ids
      
        context['selected_conf_node_ids'] = selected_conf_node_ids
        context['conf_node_ids']  = conf_node_ids
        context['selected_gateway_id'] = selected_gateway_id
        context[ 'gateway_messages'] = gateway_messages

        # ssh.close()
        return render(request, 'remote.html', context=context)

 
    
def ReplaceClient(request):
     return render(request, 'replaces.html', {'message': 'Django hakkında bilgi'})


