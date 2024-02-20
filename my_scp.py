from pydicom.uid import ExplicitVRLittleEndian
from pydicom.dataset import Dataset

from pynetdicom import (
    AE, debug_logger, evt,
    AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES
)

from pynetdicom.sop_class import CTImageStorage, PatientRootQueryRetrieveInformationModelFind

debug_logger()

def handle_store(event):  # need to define handlers for EVT_C_STORE (what C-STORE should do)
    """Handle EVT_C_STORE events."""
    ds = event.dataset  # decoded dataset from the SCU received as a pydicom dataset
    ds.file_meta = event.file_meta  # meta information
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)  # save it to a file named after its (0008,0018) SOP Instance UID,
    return 0x0000

def handle_find(event):  # need to define handlers for EVT_C_FIND (what C-FIND should do)
    """Handle EVT_C_FIND events."""
    ds = event.identifier  # extract the query dataset
    matches_found = False
    if 'PatientName' in ds:  # this needs to be modified depending on what info we are looking for!
        matches_found = True
        # Create a new dataset for each match you find
        matching_ds = Dataset()
        matching_ds.PatientName = ds.PatientName
        matching_ds.StudyInstanceUID = "1.2.3.4.5"
        matching_ds.SeriesInstanceUID = "1.2.3.4.5.1"
        matching_ds.SOPInstanceUID = "1.2.3.4.5.1.1"
        matching_ds.QueryRetrieveLevel = ds.QueryRetrieveLevel
        yield 0xFF00, matching_ds  # yield the matching dataset

    if not matches_found:
        yield 0x0000, None  # no matches found


handlers = [
    (evt.EVT_C_STORE, handle_store),    # add C-STORE handler
    (evt.EVT_C_FIND, handle_find)       # add C-FIND handler
]

ae = AE()  # create AE (application entity) instance

# Add support for C-STORE ---------------------------------
# define handling of all the storage service’s SOP Classes by adding more supported presentation contexts
storage_sop_classes = [
    # AllStoragePresentationContexts is a list of pre-built presentation contexts, one for every SOP Class in the storage service
    cx.abstract_syntax for cx in AllStoragePresentationContexts
]
for uid in storage_sop_classes:
    # ALL_TRANSFER_SYNTAXES supports both compressed and uncompressed transfer syntax
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)  # add *supported* presentation context
# ---------------------------------------------------------

# Add support for C-FIND ----------------------------------
ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind, ALL_TRANSFER_SYNTAXES)
# ---------------------------------------------------------

ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)  # start listening for association requests on port 11112
