import subprocess
import re
def GetWindowPlacement(hwnd):
    cmd = 'xwininfo -id ' + hwnd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    out = out.decode("utf-8")
    #print("TOTAL WINDOW INFO: {}".format(out))
    top_X = int(re.search(r' Absolute upper-left X:[ ]+(\d+)',out, re.MULTILINE).group(1))
    top_Y = int(re.search(r' Absolute upper-left Y:[ ]+(\d+)',out, re.MULTILINE).group(1))
    width = int(re.search(r' Width:[ ]+(\d+)',out, re.MULTILINE).group(1))
    height = int(re.search(r' Height:[ ]+(\d+)',out, re.MULTILINE).group(1))
    #for row in out.split('\n'):
    #    print(re_width.search(row))
    return [top_X, top_Y, top_X + width, top_Y + height]

def findTopWindow(wantedText=None):
    cmd = 'wmctrl -l | awk \'/' + wantedText + '/ {print $1}\''
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    return out.strip().decode("utf-8")

if __name__ == '__main__':
    hwnd = findTopWindow("Slack")
    print(hwnd)
    print(GetWindowPlacement(hwnd))
