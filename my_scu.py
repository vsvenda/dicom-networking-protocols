from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from pydicom.dataset import Dataset

debug_logger()  # send logging output to terminal

ae = AE()  # create AE (application entity) instance

ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)  # add *requested* presentation context (C-FIND)

ds = Dataset()  # create our Identifier dataset (what do we want to retrieve)
ds.PatientName = '*'  # interested in patients with any name (wildcard)
ds.QueryRetrieveLevel = 'PATIENT'  # interested in info related to patients (can also be STUDY, SERIES and IMAGE)

assoc = ae.associate("127.0.0.1", 11112)  # initiate association negotiation with IP and port
if assoc.is_established:
    print('Association established with SCP!')
    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)  # request C-FIND service
    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04X}'.format(status.Status))
            # Process the identifier dataset in some way
            if identifier:
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')
    assoc.release()
else:
    # Association rejected, aborted or never connected
    print('Failed to associate')
