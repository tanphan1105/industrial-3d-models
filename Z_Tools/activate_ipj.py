import win32com.client
import os

try:
    inv = win32com.client.GetActiveObject("Inventor.Application")
    ipj_path = "D:\\INVENTOR_DATA\\MASTER_LIBRARIES.ipj"
    pjs = inv.DesignProjectManager.DesignProjects
    try:
        pj = pjs.AddExisting(ipj_path)
    except:
        pj = pjs.ItemByName("MASTER_LIBRARIES")
    if pj:
        pj.Activate()
        print("SUCCESS: Da kich hoat truc tiep MASTER_LIBRARIES.ipj vao Autodesk Inventor!")
except Exception as e:
    print("Inventor chua mo hoac da cap nhat san file .ipj tren dia:", e)
