# dicom-networking-protocols

This code goes through the general workflow of dicom network protocols through pynetdicom.
pydicom: https://pydicom.github.io/pynetdicom/stable/index.html#pynetdicom

You should be able to connect to a scp of your liking, but if you do not have one use echoscp which comes with pynetdicom:
$ python -m pynetdicom echoscp 11112 -v

** my_scu.py **
Used to create a SCU application entity, associate it to the SCP and request its verification service.

For more info acout SCU see: https://pydicom.github.io/pynetdicom/stable/tutorials/create_scu.html
------------------------------------------------------------------------------------------------------------------------

** my_scp.py **
Used to create a SCP application entity.

To start the SCP:
$ python my_scp.py

To send dicom file:
$ python -m pynetdicom storescu 127.0.0.1 11112 CTImageStorage.dcm -v -cx

For more info about SCP see: https://pydicom.github.io/pynetdicom/stable/tutorials/create_scp.html