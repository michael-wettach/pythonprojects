#! /usr/bin/python
# Rename photo image files according to Exif data
# There are loads of Python image renaming tools on the internet. 
# This one I found at https://gist.github.com/wh13371/475e5845b427254283e7
# and added an option to synchronize the time data from several cameras.
# See time_offset in line 61-64 and comments in line 87ff
# I also included the camera model in the image name, so we know who took the picture.
import sys, datetime, os, time
# # for <PIL> on Python 2.6 => "pip install Pillow" - for Python 2.7 <PIL> part of core modules
from PIL import Image 
from PIL.ExifTags import TAGS
from datetime import datetime, timedelta

# Assumes Python 2.7! Usage examples:
# ./exif.py ~/Pictures/*
# ./exif.py DSCF0155.JPG
# ./exif.py ~/Pictures/DSCF0155.JPG ~/Pictures/DSCF0156.JPG

def get_epoch():
 return '%f' % time.time()

def get_exif_data_from_file(filename):

 exif = {}
 try:
  print "FILENAME => " + filename
  img = Image.open(filename)
  if hasattr( img, '_getexif' ):
   exifinfo = img._getexif()
   if exifinfo != None:
    for tag, value in exifinfo.items():
     TAG2text = TAGS.get(tag) # TAG# => TEXT \ 36867 => DateTimeOriginal
     #print tag, TAG2text, value # DEBUG!
     exif[TAG2text] = value
 except IOError:
  print 'IOERROR ' + fname
 
 return exif

def get_filename_datetime_string(exif_datetime_string, format):
 datetime_object = datetime.strptime(exif_datetime_string, '%Y:%m:%d %H:%M:%S')
 return datetime.strftime(datetime_object, format)

def rename_image(new_filename, exif_datetime, filename_ext):

 if os.path.exists(new_filename):
  # print "WARNING! => <%s> already exists! - will pad with current epoch" % new_filename
  # new_filename = exif_datetime + "_" + get_epoch() + filename_ext
  print "WARNING! => <%s> already exists! - no action taken"

 else:
  print "NEW FILENAME => " + new_filename

  try:
   os.rename(f, new_filename)
   print('RENAMED => {0} >>> {1}'.format(f, new_filename))
  except OSError as e:
   print e


def time_offset(dt_string, dt_hours, dt_minutes, dt_seconds):
  dt_object = datetime.strptime(dt_string, '%Y_%m_%d_%H_%M_%S')
  dt_object += timedelta(hours=dt_hours, minutes=dt_minutes, seconds=dt_seconds)
  return dt_object.strftime('%Y_%m_%d_%H_%M_%S')


#-------------------------------------------
if __name__ == "__main__":
#-------------------------------------------

 for f in sys.argv[1:]:
  
  if f.endswith(".JPEG") or f.endswith(".JPG") or f.endswith(".jpg") or f.endswith(".jpeg"):

   print "<<<" # start
   myDir = os.path.dirname(f)
   original_filename, filename_ext = os.path.splitext(f)
   exif_data = get_exif_data_from_file(f)
   
   #for k, v in exif_data.iteritems(): print k, v
   #print ("%s : %s : %s" % (exif_data['Make'], exif_data['Model'], exif_data.get('DateTimeOriginal')))
   
   exif_datetime = get_filename_datetime_string((exif_data['DateTimeOriginal']), '%Y_%m_%d_%H_%M_%S')
   print "EXIF DateTimeOriginal => " + exif_datetime

   exif_model = exif_data['Model']
   # if 'DMC-TZ' in exif_model:
   #   exif_datetime = time_offset(exif_datetime, 0, -9, 0)
   # if 'PENTAX' in exif_model:
   #   exif_datetime = time_offset(exif_datetime, 0, 59, 0)
   
   exif_datetime = exif_datetime + '_' + exif_model.strip()
   new_filename = myDir + '/' + exif_datetime + filename_ext

   rename_image(new_filename, exif_datetime, filename_ext)

   print ">>>" # end
