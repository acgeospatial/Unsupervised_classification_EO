####  def GetExtent and def ReprojectCoord taken from here
####http://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings
## Also training points from here
## ## code adapted from below
### http://gis.stackexchange.com/questions/46893/getting-pixel-value-of-gdal-raster-under-ogr-point-without-numpy
## And if you want just extracting values from sat data and plotting in 3D https://github.com/acgeospatial/extract_values_to_points 


from osgeo import gdal,ogr,osr
import random
import struct
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
## this for the arrays
import numpy as np
## this for kmeans
from sklearn.cluster import KMeans


def GetExtent(gt,cols,rows):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
            print x,y
        yarr.reverse()
    return ext

def ReprojectCoords(coords,src_srs,tgt_srs):
    ''' Reproject a list of x,y coordinates.

        @type geom:     C{tuple/list}
        @param geom:    List of [[x,y],...[x,y]] coordinates
        @type src_srs:  C{osr.SpatialReference}
        @param src_srs: OSR SpatialReference object
        @type tgt_srs:  C{osr.SpatialReference}
        @param tgt_srs: OSR SpatialReference object
        @rtype:         C{tuple/list}
        @return:        List of transformed [[x,y],...[x,y]] coordinates
    '''
    trans_coords=[]
    transform = osr.CoordinateTransformation( src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords
	
	
	
def training_points(raster, mx, my):
	lsx=[]
	lsy=[]
	lsz=[]
	src_ds=gdal.Open(raster) 
	gt=src_ds.GetGeoTransform()
	rb=src_ds.GetRasterBand(1)
	
	for i in range(0,len(mx)):
		#Convert from map to pixel coordinates.
		#Only works for geotransforms with no rotation.
		px = int((mx[i] - gt[0]) / gt[1]) #x pixel
		py = int((my[i] - gt[3]) / gt[5]) #y pixel

		intval=rb.ReadAsArray(px,py,1,1)
		#print intval[0] #intval is a numpy array, length=1 as we only asked for 1 pixel value
		#print mx
		#print my

		value = float(intval[0])
		x = float(mx[i])
		y = float(my[i])
		lsz.append(value)
		lsx.append(x)
		lsy.append(y)
		
	return lsx, lsy, lsz

raster=r'D:\training_extract\band2.tif'
ds=gdal.Open(raster)

gt=ds.GetGeoTransform()
cols = ds.RasterXSize
rows = ds.RasterYSize
ext=GetExtent(gt,cols,rows)

src_srs=osr.SpatialReference()
src_srs.ImportFromWkt(ds.GetProjection())
tgt_srs=osr.SpatialReference()
tgt_srs.ImportFromEPSG(32630) #### force it
#tgt_srs = src_srs.CloneGeogCS() #### clone it the choice is yours!!

geo_ext=ReprojectCoords(ext,src_srs,tgt_srs)


#### random points

randPoints = []
count = 0
while count<10000:
    x = random.uniform(geo_ext[0][0], geo_ext[2][0])
    y = random.uniform(geo_ext[1][1], geo_ext[0][1])
    randPoints.append((x,y))
    count += 1
	
mx = []
my = []
with open('random_coords.csv', 'w') as f:
	f.write("X,Y" +"\n")
	for i in range(0, len(randPoints)):
		f.write(str(randPoints[i][0])+","+str(randPoints[i][1]) +"\n")
		mx.append(randPoints[i][0])
		my.append(randPoints[i][1])
		
		
		
lsx1, lsy1, lsz1 = training_points(raster, mx, my)
raster=r'D:\training_extract\band3.tif'
lsx1, lsy1, lsz2 = training_points(raster, mx, my)
raster=r'D:\training_extract\band4.tif'
lsx1, lsy1, lsz3 = training_points(raster, mx, my)
raster=r'D:\training_extract\band5.tif'
lsx1, lsy1, lsz4 = training_points(raster, mx, my)
raster=r'D:\training_extract\band6.tif'
lsx1, lsy1, lsz5 = training_points(raster, mx, my)
raster=r'D:\training_extract\band7.tif'
lsx1, lsy1, lsz6 = training_points(raster, mx, my)


with open('random_coords_z2.csv', 'w') as f:
	for i in range(0, len(lsx1)):
		if lsz1[i] > 0:
			f.write(str(lsx1[i])+","+str(lsy1[i])+","+str(lsz1[i])+","+str(lsz2[i])+","+str(lsz3[i])+","+str(lsz4[i])+","+str(lsz5[i])+","+str(lsz6[i]) +"\n")


### load data from txt to numpy array			
my_data = np.genfromtxt('random_coords_z2.csv', delimiter=',')
### Define the data to classify
data = my_data[:, [2,3,4,5,6,7]]
### Unsupervised classification with 5 classes
y_pred = KMeans(n_clusters=5).fit_predict(data)

plt.figure(1)

plt.subplot(321)
plt.scatter(my_data[:, 2], my_data[:, 3], c=y_pred, s=104)
plt.title("Band 2 and Band 3")
plt.subplot(322)
plt.scatter(my_data[:, 2], my_data[:, 4], c=y_pred, s=104)
plt.title("Band 2 and Band 4")
plt.subplot(323)
plt.scatter(my_data[:, 3], my_data[:, 4], c=y_pred, s=104)
plt.title("Band 3 and Band 4")
plt.subplot(324)
plt.scatter(my_data[:, 4], my_data[:, 5], c=y_pred, s=104)
plt.title("Band 4 and Band 5")
plt.subplot(325)
plt.scatter(my_data[:, 5], my_data[:, 6], c=y_pred, s=104)
plt.title("Band 5 and Band 6")
plt.subplot(326)
plt.scatter(my_data[:, 5], my_data[:, 7], c=y_pred, s=104)
plt.title("Band 5 and Band 7")

plt.show()

### If you want to save the data to a file this is below, not needed if you only want to plot in Matplotlib
lsclass = list(y_pred)
x = list(my_data[:, 0])
y = list(my_data[:, 1])


with open('random_coords_classed2.csv', 'w') as f:
	for i in range(0, len(x)):
		f.write(str(x[i])+","+str(y[i])+","+str(lsclass[i]) +"\n")
