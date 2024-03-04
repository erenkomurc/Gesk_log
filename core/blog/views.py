from django.shortcuts import render
import paramiko 
from paramiko import SSHClient
from django.http import HttpResponse
import json
import time



# Create your views here.


def RemoteClient(request):
    # try:
        
        selected_gw_id = request.GET.get('selected_gw_id', None)
        selected_node_id = request.GET.get('selected_node_id', None)
        selected_filter = request.GET.get('filter', None)
        min_value = request.GET.get('min_value', -99)
        max_value = request.GET.get('max_value', 99)
    

        hostname = '2.56.154.117'
        port = 22
        username = 'root'
        password = 'gesk2017'

        # transport  = paramiko.Transport((hostname, port))
        # transport.connect(username=username, password=password)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=hostname, username=username, password=password, port=port, )
        print("bsğlandı")
        
    # if pub_{gw_id} in filename:
            
        # asd = f"/root/amazon_dh_logger/pub_{gw_id}_{node_id}.txt"
        context = dict()
        nodes_with_gw_ids= dict()
        gw_ids = set()
        messages = list()
        # local_path = 'logs/pub_083a8d01d0a0_4175154.txt'

        # dir = 'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/'

        # filename_list = os.listdir(dir)
        sftp_client = ssh.open_sftp()
        filename_list = sftp_client.listdir("/root/amazon_dh_logger/")
        print(sftp_client.listdir("/root/amazon_dh_logger/"))
        for filename in filename_list:
            if 'pub_' in filename:
                # print(filename)
                gw_id = filename.split('_')[1]
                gw_ids.add(gw_id)

                

        for gw_id in gw_ids:
            for file in filename_list:
                if f"pub_{gw_id}" in file:
                    if "conf" not in file:
                        node_id = file.split('_')[2][:7]
                        if not selected_filter:
                            if gw_id not in nodes_with_gw_ids.keys():
                                nodes_with_gw_ids[gw_id] = set()
                            nodes_with_gw_ids[gw_id].add(node_id)
                        else:
                            # local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/pub_{gw_id}_{node_id}.txt'
                            remote_path = f'/root/amazon_dh_logger/pub_{gw_id}_{node_id}.txt'

                            with open(remote_path, "r") as filea:
                                filea = sftp_client.file(remote_path, "r")
                                all_message = filea.readlines()
                                all_message.reverse()
                                for line in all_message:
                                    line_for_json = line.split('|')[1]
                                    line_json = json.loads(line_for_json)
                                    line_json['timestamp'] = line.split('|')[0]

                                    if (line_json[selected_filter] >= int(min_value) and line_json[selected_filter] <= int(max_value)):
                                        if gw_id not in nodes_with_gw_ids.keys():
                                            nodes_with_gw_ids[gw_id] = set()
                                        nodes_with_gw_ids[gw_id].add(node_id)
        
        # print(nodes_with_gw_ids)
        # transport.close()
        # print(gw_ids)
        
        if (selected_gw_id):
            context['selected_gw_id'] = selected_gw_id
            context['node_ids'] = nodes_with_gw_ids[selected_gw_id]

            if (selected_node_id):
                context['selected_node_id'] = selected_node_id
                remote_path = f'/root/amazon_dh_logger/pub_{selected_gw_id}_{selected_node_id}.txt'
                # local_path = f'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/pub_{selected_gw_id}_{selected_node_id}.txt'
                with open(remote_path, "r") as filea:
                    filea = sftp_client.file(remote_path, "r")
                    all_message = filea.readlines()
                    all_message.reverse()
                    for line in all_message:
                        line_for_json = line.split('|')[1]
                        line_json = json.loads(line_for_json)
                        line_json['timestamp'] = line.split('|')[0]

                        if not selected_filter:
                           messages.append(line_json)
                        else:
                            if line_json[selected_filter] >= int(min_value) and line_json[selected_filter] <= int(max_value):
                                messages.append(line_json)
               
        context['all_message'] = messages
        context['gw_ids'] = gw_ids

        ssh.close()
        return render(request, 'remote.html', context=context)

    # except Exception as e:
    #     print(f"download error:{str(e)}")
    #     return render(request, 'remote.html') 




# import paramiko
# from django.http import HttpResponse
# from django.shortcuts import render, HttpResponse

# def RemoteClient(request):
#     try:
#         hostname = '2.56.154.117'
#         port = 22
#         username = 'root'
#         password = 'gesk2017'

#         transport = paramiko.Transport((hostname, port))
#         transport.connect(username=username, password=password)

#         sftp = paramiko.SFTPClient.from_transport(transport)

       
#         remote_path = '/root/amazon_dh_logger/pub_083a8d01d0a0_4175154.txt'

      
#         local_path = 'logs/pub_083a8d01d0a0_4175154.txt'

     
#         sftp.get(remote_path, local_path)

       
#         sftp.close()
#         transport.close()

#         print("File download successful")

#         return HttpResponse("SUCCESSFUL")
  
#     except Exception as e:
#         print(f"Error dosya yolu: {str(e)}")
#         return HttpResponse("EROR:REMEMEMM")
#         return render(request, 'remote.html')
    


   # f = open('all_message' , 'r')
            # lines  = f.readlines()
            # column_names = ["ID", "DATE"]
            # list=[]

            # for line in lines[::-1]:
            #     test = line.split("|")
            #     test[-1]=line.split("|")[-1].strip()
            #     list.append(test)

            #     context = {'list': list, 'column_names':column_names}
            #     return render(request, "remote.html", context)
    
def ReplaceClient(request):
     return render(request, 'replaces.html', {'message': 'Django hakkında bilgi'})
