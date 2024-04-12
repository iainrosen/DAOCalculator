from astropy import units as u
from astropy.coordinates import SkyCoord,EarthLocation,AltAz
from datetime import datetime, timezone
from astropy.time import Time
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class target:
    def __init__(self, name, coord):
        self.name=name
        self.coord=coord

def plot_point_on_graph(targets):
    # Define the range for the axes
    HA_range = (-6, 6)
    DEC_range = (-15, 90)
    
    # Create a new figure
    plt.figure(figsize=(8, 6))
    
    # Load the background image
    img = mpimg.imread('zones2.png')
    
    # Display the background image
    plt.imshow(img, extent=[HA_range[0], HA_range[1], DEC_range[0], DEC_range[1]], aspect='auto')
    
    # Convert HA and DEC to coordinates
    for x in targets:
        HA_coord = (getHA(x.coord) - HA_range[0]) / (HA_range[1] - HA_range[0])
        DEC_coord = (x.coord.dec.degree - DEC_range[0]) / (DEC_range[1] - DEC_range[0])
    
        # Plot the point
        if inRange(x.coord):
            plt.plot(HA_coord * (HA_range[1] - HA_range[0]) + HA_range[0],DEC_coord * (DEC_range[1] - DEC_range[0]) + DEC_range[0],'ro')  # 'ro' specifies red color and circle marker
        else:
            plt.plot(HA_coord * (HA_range[1] - HA_range[0]) + HA_range[0],DEC_coord * (DEC_range[1] - DEC_range[0]) + DEC_range[0],'rx')
    
        # Add label to the plot point
        plt.text(getHA(x.coord), x.coord.dec.degree, x.name, fontsize=12, ha='left', va='bottom')

    # Set x and y axis limits
    plt.xlim(HA_range)
    plt.ylim(DEC_range)
    
    # Label the axes
    plt.xlabel('Hour Angle (HA)')
    plt.ylabel('Declination (DEC)')
    
    # Show the plot
    plt.grid(False)
    plt.show()

#zone 1:
# p1: -1<HA<3.5, 50<DEC<75
# p2: 3.5<HA<5.5, 50<DEC<80

def isZone1(coord):
    ha=getHA(coord)
    dec=coord.dec.degree
    if ha>=-1 and ha<=3.5 and dec>=50 and dec<=75:
        return True
    elif ha>=3.5 and ha<=5.5 and dec>=50 and dec<=80:
        return True
    else:
        return False

#zone 2:
# p1: -1<HA<-0.5, 0<DEC<50
# p2: -0.5<HA<1, -10<DEC<50
# p3: 1<HA<2, 0<DEC<50
# p4: 2<HA<5, (15HA-30)<DEC<50
def isZone2(coord):
    ha=getHA(coord)
    dec=coord.dec.degree
    if ha>=-1 and ha<=-0.5 and dec>=0 and dec<=50: #p1
        return True
    elif ha>=-0.5 and ha<=1 and dec>=-10 and dec<=50: #p2
        return True
    elif ha>=1 and ha<=2 and dec>=0 and dec<=50: #p3
        return True
    elif ha>=2 and ha<=5 and dec>=(15*ha-30) and dec<=50:
        return True
    else:
        return False
    
def isZone3(coord):
    ha=getHA(coord)
    dec=coord.dec.degree
    if ha>=-2 and ha<=-1 and dec>=0 and dec<=50:
        return True
    elif ha>=-4 and ha<=-2 and dec>=(-15*ha-30) and dec<=30:
        return True
    elif ha>=-4 and ha<=-2 and dec>=30 and dec<=50:
        return True
    else:
        return False
#zone 3:
#p1: -2<HA<-1, 0<DEC<50
#p2: -4<HA<-2, (-15HA-30)<DEC<30
#p3: -4<HA<-2, 30<DEC<50

def zoneRange(coord):
    if isZone1(coord):
        return "Zone 1"
    elif isZone2(coord):
        return "Zone 2"
    elif isZone3(coord):
        return "Zone 3"
    else:
        return "Out of Range!"

def inRange(coord):
    if isZone1(coord) or isZone2(coord) or isZone3(coord):
        return True
    else:
        return False


#48.51984503416932, -123.41835768751552
obslocation=EarthLocation(lat=48.51984503416932*u.deg, lon=-123.41835768751552*u.deg, height=230*u.m)

def getLST():
    #obstime=Time(datetime.now(timezone.pst), scale='utc', location=obslocation)
    obstime=Time.now()
    return obstime.sidereal_time('apparent', obslocation).hour

def getHA(target):
    return getLST()-target.ra.hour

targets=[]
while True:
    print()
    cmd=input(">>> ")
    if cmd=="add":
        try:
            targetName=input("Enter target name: ")
            targets.append(target(targetName,SkyCoord.from_name(targetName)))
        except:
            print("Couldn't find target "+targetName)
            try:
                targets.append(target(targetName,SkyCoord(ra=input('Enter RA (J2000): '), dec=input('Enter DEC (J2000): '), frame='icrs', unit=(u.hourangle,u.deg))))
            except:
                print("Error entering target manually.")
    elif cmd=="remove" or cmd=="del":
        try:
            targets.pop(int(input("Enter target number to remove: ")))
        except:
            print("Error removing target.")
    elif cmd=="list" or cmd=="ls":
        displayTargets=[]
        for i, x in enumerate(targets):
            displayTargets.append([i,x.name,str(round(getHA(x.coord),4)),str(round(x.coord.ra.hour,4)),str(round(x.coord.dec.degree,4)),zoneRange(x.coord)])
        print()
        print(tabulate(displayTargets,headers=['#','Target Name','Hour Angle','RA','DEC', "Target Zone"]))
    elif cmd=="chart" or cmd=="c":
        plot_point_on_graph(targets)
    elif cmd=="bye" or cmd=="exit":
        break
    elif cmd=="time":
        print("Local Sidereal Time: "+str(round(getLST(),4)))
    else:
        print("Available Commands: add, remove, list, chart, time, bye")