'''
This Function is the core of the module and should reduce total information size for a given mode(e.g 'research', 'bio')
from all data_packets in data_store.

Currently doing a simple merge by concating them all to a single string, and deliminating a break in data packets with a ' >< '.
'''
def merge_information(data_store, mode):
    ret_info = ""

    for data_packet in data_store:
        ret_info+=data_packet[mode]
        ret_info+=" >< "
    return ret_info


def consolidate_data(data_store):
    if len(data_store) == 0:
        return {}
    
    modes = data_store[0].keys()
    ret_data_packet = {i : "" for i in modes}

    for m in modes:
        ret_data_packet[m] = merge_information(data_store=data_store,mode=m)

    return ret_data_packet
