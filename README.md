**Septoria-leaf**

Septoria-leaf is a free open source software for measuring the disease
percentage of leaves infected by *Parastagonospora nodorum* or
*Zymoseptoria tritici* in a computationally efficient manner. Software
automate labels reading from digital images and facilitates septoria
disease severity examination. Program analyses digital images, examines
the leaves on an image sample (each leaf individually) and summarizes
results in the table. Software creates also a pivot table of total leaf
area and disease area as pixel sums and average disease percentage of
each image sample.

**Getting Started**

**Requirements:**

Windows 10

Python 3.8.2 with following modules installed:\
pip	19.2.3\
opencv-python 4.2.0.32\
numpy 1.18.1\
pandas 1.0.3\
pyzbar 0.1.8\
pypng 0.0.20\
Pillow 7.1.2\
pyqrcode 1.2.1


**Installing:**

Download septoria-leaf.zip and unzip the folder. Make sure that program
path is encoded in Latin-1 (ISO-8859-1).

**Definitions:**

**Image sample** is a digital image of wheat or triticale leaves in a
seedling growth stage labelled with generated QR codes.

**label** should contain all necessary information to identify experimental 
object using alpha numeric characters description and generated QR code.

**sample\_name** is a text read from label QR code.

**leaf\_area** is a total area in pixels of one extracted leaf from an
image sample.

**disease\_area** is a total diseased area in pixels of leaf extracted
from an image sample.

**disease\_percetage** is a ratio of disease\_area to leaf\_area \*100.

**Preparation of image samples:**

Leaves in an image sample should be in one piece, using fragmented
leaves is not advised because the program will interpret them as a whole
leaf. Leaves should not touch each other, otherwise software will
interpret them as a single leaf. The suggested colour of background is
blue in order to easily extract leaves from image samples. Place generated QR code labels
on image samples in order to extract text for further analysis, otherwise the sleaves.py program
will use file names as a description of image samples.

**Run the program:**

lab_gener.py - is small software tool assisting with labels and QR codes 
generating in order to facilitate identification of experimental objects 
by sleaves.py. 

1.  Prepare a list of labels to read in *object\_list.txt* file located
    in the main directory - *septoria-leaf*. Each row should contain a
    single label name.
2.  Run the lab_gener.py to generate labels QR codes in *labels_output* 
directory.
3.  Print prepared QR codes on blue background and place them on each experimental object.


sleaves.py - the software evaluates diseased area percentage and
summarises results in tables. To run the program and optimize the
parameters follow the protocol:

1.  The sleaves.py program analyses files from the *labels\_output*
    folder.

2.  To enable extracted leaves and diseased tissue write, set the
    *save\_leaf\_im* and *save\_diseased\_im* variables to True. Files
    will be located in the *output* folder.

save\_leaf\_im = True \# True/False save an extracted leaf image

save\_diseased\_im = True \# True/False save an diseased image

3.  To calibrate the leaf HUE parameter *leaf\_hue\_min* and
    *leaf\_hue\_max* values can be modified:

leaf\_hue\_min = 0 \# Min leaf HUE, default 0\
leaf\_hue\_max = 90 \# Max leaf HUE, default 90

4.  To calibrate the diseased tissue HUE parameter, the
    *diseased\_hue\_min* and *diseased\_hue\_max* values can be
    modified:

diseased\_hue\_min = 0 \# Min diseased HUE, default 0\
diseased\_hue\_max = 45 \# Max diseased HUE, default 45

5.  Run the sleaves.py program.

6.  When the program completes analysis output files in \*.csv format
    will be created in the main folder *septoria-leaf*. The results.csv
    file contain results summary of all leaves disease percentage (sample leaf\_area,
    disease\_area and disease\_percentage). The pivot\_table.csv file is
    table summary of a results table grouped by sample name. The
    pivot\_table.csv contain leaf\_area and disease\_area aggregated by
    sum for each object name and average of a disease\_percentage.


**Acknowledgments**

Stack Overflow community.

Authors
-------
Sławomir Bartosiak
