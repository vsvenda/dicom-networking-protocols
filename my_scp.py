from pydicom.uid import ExplicitVRLittleEndian

from pynetdicom import (
    AE, debug_logger, evt,
    AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES
)

from pynetdicom.sop_class import CTImageStorage

debug_logger()

def handle_store(event):  # need to define handlers for EVT_C_STORE (what C_STORE should do)
    """Handle EVT_C_STORE events."""
    ds = event.dataset  # decoded dataset from the SCU received as a pydicom dataset
    ds.file_meta = event.file_meta  # meta information
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)  # save it to a file named after its (0008,0018) SOP Instance UID,
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()  # create AE (application entity) instance

# define handling of all the storage service’s SOP Classes by adding more supported presentation contexts
storage_sop_classes = [
    # AllStoragePresentationContexts is a list of pre-built presentation contexts, one for every SOP Class in the storage service
    cx.abstract_syntax for cx in AllStoragePresentationContexts
]
for uid in storage_sop_classes:
    # ALL_TRANSFER_SYNTAXES supports both compressed and uncompressed transfer syntax
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)  # add *supported* presentation context

ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)  # start listening for association requests on port 11112
