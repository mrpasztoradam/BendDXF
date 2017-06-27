# Start
#            ____________________
#           |                    |
#           |                    |
#           |                    |
#           |                  W |
#        ˄  |                    |
#    Y+  |  |                    |
#        |  |                    |
#        |  |_________L__________|
#       (0,0)  -----˃
#                X+

"""
 ________________________________________________________________________________
 |Radius	    |Soft / Aluminum	|Medium / Steel	    |Hard / Stainless Steel |
 |------------------------------------------------------------------------------|
 |Air Bending   |                   |                   |                       |
 |------------------------------------------------------------------------------|
 |0 - Mt.	    |.33	            |.38	            |.40                    |
 |Mt. - 3*Mt.	|.40	            |.43	            |.45                    |
 |3*Mt. - >3*Mt.|.50	            |.50	            |.50                    |
 |------------------------------------------------------------------------------|
 |Bottom Bending|                   |                   |                       |
 |------------------------------------------------------------------------------|
 |0 - Mt.	    |.42	            |.44	            |.46                    |
 |Mt. - 3*Mt.	|.46    	        |.47	            |.48                    |
 |3*Mt. - >3*Mt.|.50	            |.50	            |.50                    |
 |------------------------------------------------------------------------------|
 |Coining       |                   |                   |                       |
 |------------------------------------------------------------------------------|
 |0 - Mt.	    |.38	            |.41	            |.44                    |
 |Mt. - 3*Mt.	|.44	            |.46	            |.47                    |
 |3*Mt. - >3*Mt.|.50	            |.50	            |.50                    |
 |______________________________________________________________________________|

"""

import math
import dxfwrite
from dxfwrite import DXFEngine as dxf

drawing = dxf.drawing('example.dxf')

ktext = """
 ________________________________________________________________________________
 |Radius	    |Soft / Aluminum	|Medium / Steel	    |Hard / Stainless Steel |
 |------------------------------------------------------------------------------|
 |Air Bending   |                   |                   |                       |
 |------------------------------------------------------------------------------|
 |0 - Mt.	    |.33	            |.38	            |.40                    |
 |Mt. - 3*Mt.	|.40	            |.43	            |.45                    |
 |3*Mt. - >3*Mt.|.50	            |.50	            |.50                    |
 |------------------------------------------------------------------------------|
 |Bottom Bending|                   |                   |                       |
 |------------------------------------------------------------------------------|
 |0 - Mt.	    |.42	            |.44	            |.46                    |
 |Mt. - 3*Mt.	|.46    	        |.47	            |.48                    |
 |3*Mt. - >3*Mt.|.50	            |.50	            |.50                    |
 |------------------------------------------------------------------------------|
 |Coining       |                   |                   |                       |
 |------------------------------------------------------------------------------|
 |0 - Mt.	    |.38	            |.41	            |.44                    |
 |Mt. - 3*Mt.	|.44	            |.46	            |.47                    |
 |3*Mt. - >3*Mt.|.50	            |.50	            |.50                    |
 |______________________________________________________________________________|
"""

# Prompt Variables

Wraw = None
while Wraw is None:
    try:
        Wraw = float(input("Enter width in mm: \n"))
    except ValueError:
        print("Not supported value...")

Hraw = None
while Hraw is None:
    try:
        Hraw = float(input("Enter height in mm: \n"))
    except ValueError:
        print("Not supported value...")

angle = None
while angle is None:
    try:
        angle = float(input("Enter angle in deg: \n"))
    except ValueError:
        print("Not supported value...")

length = None
while length is None:
    try:
        length = float(input("Enter length in mm: \n"))
    except ValueError:
        print("Not supported value...")

thick = None
while thick is None:
    try:
        thick = float(input("Enter thickness in mm: \n"))
    except ValueError:
        print("Not supported value...")

kfact = None
while kfact is None:
    try:
        print(ktext)
        kfact = float(input("Enter K-factor for the material:  \n"))
    except ValueError:
        print("Not supported value...")

# Constants

radii = thick
pi = math.pi

BAraw = angle * (pi/180)*(radii+(kfact*thick))

BA = round(BAraw, 3)

FlatW = (Wraw-(2*(radii+thick)))+(2*(Hraw-(radii+thick)))+(2*BA)

print('Bend allowance is', BA, 'mm')
print('Flat pattern width is ', FlatW, 'mm')
# Header

drawing.header['$EXTMIN'] = (0, 0, 0)
drawing.header['$EXTMAX'] = (5000, 5000, 500)

# Layers

drawing.add_layer('contour', color=4)
drawing.add_layer('bend', color=241, linetype='DASHED')

# Objects

drawing.add(dxf.rectangle((0, 0), length, FlatW, layer='contour'))
drawing.add(dxf.line((length, (Hraw-(radii+thick)+(BA/2))),
                     (0, (Hraw-(radii+thick))+(BA/2)),
                     layer='bend'))
drawing.add(dxf.line((length, (FlatW-(Hraw-(radii+thick)+(BA/2)))),
                     (0, (FlatW-(Hraw-(radii+thick))+(BA/2))),
                     layer='bend'))

# Save

drawing.save()
