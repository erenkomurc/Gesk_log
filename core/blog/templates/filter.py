

def RemoteClient(request):
    try:
        
        selected_gw_id    = request.GET.get('selected_gw_id', None)
        selected_node_id  = request.GET.get('selected_node_id', None)
        # filter_type       = request.GET.get('smaller-bigger-buttons', None)
        # column            = request.GET.get('table-column-fields', None)
        # value             = int(request.GET.get('value', 0))    

        hostname = '2.56.154.117'
        port = 22
        username = 'root'
        password = 'gesk2017'

        # transport  = paramiko.Transport((hostname, port))
        # transport.connect(username=username, password=password)

        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        # ssh.connect(hostname=hostname, username=username, password=password, port=port, )
        # print("bsğlandı")
        
        # if pub_{gw_id} in filename:
            
        # asd = f"/root/amazon_dh_logger/pub_{gw_id}_{node_id}.txt"
        context = dict()
        nodes_with_gw_ids= dict()
        gw_ids = set()
        messages = list()
        # local_path = 'logs/pub_083a8d01d0a0_4175154.txt'

        dir = 'C:/Users/gesku/OneDrive/Desktop/amazon_dh_logger/'

        filename_list = os.listdir(dir)
        # sftp_client = ssh.open_sftp()
        # filename_list = sftp_client.listdir("/root/amazon_dh_logger/")
        # print(sftp_client.listdir("/root/amazon_dh_logger/"))
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
                        nodes_with_gw_ids.setdefault(gw_id, set().add(node_id))
                        if gw_id not in nodes_with_gw_ids.keys():
                            nodes_with_gw_ids[gw_id] = set()
                        # nodes_with_gw_ids[gw_id].add(node_id)
        
        # print(nodes_with_gw_ids)
        # transport.close()
        # print(gw_ids)
        if (selected_gw_id):
            context['selected_gw_id'] = selected_gw_id
            context['node_ids'] = nodes_with_gw_ids[selected_gw_id]
            if (selected_node_id):
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

                        # if filter_type and column in line_json:
                        #     if filter_type == 'search-filter-smaller' and line_json[column] > value:
                        #         continue
                            
                        #     elif filter_type == 'search-filter-bigger' and line_json[column] < value:
                        
                        messages.append(line_json)
                # all_message.reverse()
                # all_message =  '\n'.join(all_message)
                # context['all_message'] = all_message

               
                # context['found_message_id'] = parsed_found_message
        context['all_message'] = messages
        context['gw_ids'] = gw_ids

        print(len(messages))

        # ssh.close()
        return render(request, 'remote.html', context=context)

    except Exception as e:
        print(f"download error:{str(e)}")
    #   return HttpResponse("error: file upload")
        return render(request, 'remote.html') 
