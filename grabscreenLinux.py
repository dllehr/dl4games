import cv2
import numpy as np
import mss
def grab_screen(region=None):

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
            monitor = {"top": top, "left": left, "width": width, "height": height}
    with mss.mss() as sct:
    #print("REGION: {}".format((left, top, width, height)))
    #img = sct.screenshot(region=(left, top, width, height))
        #monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
        img = np.array(sct.grab(monitor))
        
        
    # hwindc = win32gui.GetWindowDC(hwin)
    # srcdc = win32ui.CreateDCFromHandle(hwindc)
    # memdc = srcdc.CreateCompatibleDC()
    # bmp = win32ui.CreateBitmap()
    # bmp.CreateCompatibleBitmap(srcdc, width, height)
    # memdc.SelectObject(bmp)
    # memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    # signedIntsArray = bmp.GetBitmapBits(True)
    # img = np.fromstring(signedIntsArray, dtype='uint8')
    # img.shape = (height,width,4)


    # srcdc.DeleteDC()
    # memdc.DeleteDC()
    # win32gui.ReleaseDC(hwin, hwindc)
    # win32gui.DeleteObject(bmp.GetHandle())

    return  cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2RGB)
