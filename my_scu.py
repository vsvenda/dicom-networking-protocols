from pynetdicom import AE, debug_logger

debug_logger()  # send logging output to terminal

ae = AE()  # create AE (application entity) instance
ae.add_requested_context('1.2.840.10008.1.1')  # add *requested* presentation context
assoc = ae.associate("127.0.0.1", 11112)  # initiate association negotiation with IP and port
if assoc.is_established:
    print('Association established with Echo SCP!')
    status = assoc.send_c_echo()  # request verification service (echo)
    assoc.release()
else:
    # Association rejected, aborted or never connected
    print('Failed to associate')
