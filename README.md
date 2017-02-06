# Unsupervised_classification_EO
With remote sensing we often talk about the 3 resolutions: spatial, temporal and spectral. In recent years a massive step change has occurred with temporal data. Even this week there has been another huge leap forward.

Planet have just announced that they are to launch a world record 88 of its doves and, if successful, they will be able to cover the whole of the earth every day.

You can read about that announcement here https://www.planet.com/pulse/record-breaking-88-satellites/

A few years ago the starting gun was fired on the race to very high spatial resolution imagery. Today Worldview 4 (would have been GeoEye 2) has just come online with a resolution of 31cm; you can have a look at some of the sample imagery on this page. Or you can, like me, marvel at the image WorldView-2 took of the launch of WorldView-4

https://twitter.com/DigitalGlobe/status/827593797534089216

Wow!

Let us not forget the spectral resolution though. I am going to look at the unsupervised classification of multispectral data; in this case I am going to use Landsat 8 data, but exactly the same method would apply to Sentinel 2 or in fact any image. At this stage, I am just looking at extract the values and grouping them using an unsupervised classifier - generating a raster... that is perhaps for a future post.

I wrote about extracting the values from satellite data here http://www.acgeospatial.co.uk/blog/extracting-values-sat-imagery/



And now let’s build on this. My workflow looks like this

-         Get boundary image coordinates

-         Randomly generate (10000, you can change this) points with the boundary

-         Extract the values from all bands of the imagery

-         Check that every point has a value

-         Run k means unsupervised classification

-         Plot it!

Simple(?)!

Getting the boundary from the image(s) is very nicely done here. This gives 2 nice functions. I will use the ‘extract the values all bands’ function from my previous tutorial, so all that is left to do is to randomly generate the points within this boundary, push it into scikit-learn to generate an unsupervised classification and plot it (matplotlib).

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image1.png)

My image extents are defined at geo_ext (min x and max x, min y and max y) I am generating 10000 random points, then writing them out to a csv and creating 2 lists with the X (mx) and Y (my) coordinates. After that I call the training point function like this

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image2.png)


You can call it as many times as you need (depending on what bands you want to use)

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image3.png)

I call it 6 times for bands 2,3,4,5,6&7 and then I write it out to a csv

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image4.png)

Load this textfile into a numpy array, and classify it (3lines!), 5 clusters are specified (n_cluster=5), but feel free to change!

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image5.png)

Now all that is left to do is plot it. y_pred is the predicted data. Below I am plotting the bands values and colouring the scatter based on the group.

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image6.png)

![alt tag](http://www.acgeospatial.co.uk/wp-content/uploads/2017/02/image7.png)

And there you go. Unsupervised classification of (points from) satellite data.

This is just the start to what can be done. Quite often the battle is getting the data so you can start working with it.
