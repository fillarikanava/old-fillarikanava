import sys, math, random

OFFSET=268435456
RADIUS=85445659.4471

clustering_debug=False

# -- The Point class represents points in n-dimensional space
class Point:

    # Instance variables
    # self.coords is a list of coordinates for this Point
    # self.n is the number of dimensions this Point lives in (ie, its space)
    # self.reference is an object bound to this Point
    # Initialize new Points
    def __init__(self, coords, reference=None, zoomlevel=12):
        self.coords = coords
        self.n = len(coords)
        self.reference = reference
        self.zoom=zoomlevel

    # Return a string representation of this Point
    def __repr__(self):
        return str(self.coords)

# -- The Cluster class represents clusters of points in n-dimensional space
class Cluster:

    # Instance variables
    # self.points is a list of Points associated with this Cluster
    # self.n is the number of dimensions this Cluster's Points live in
    # self.centroid is the sample mean Point of this Cluster
    # Initialize new Clusters
    def __init__(self, points):

        # We forbid empty Clusters (they don't make mathematical sense!)
        if len(points) == 0: raise Exception("ILLEGAL: EMPTY CLUSTER")
        self.points = points
        self.n = points[0].n

        # We also forbid Clusters containing Points in different spaces
        # Ie, no Clusters with 2D Points and 3D Points
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: MULTISPACE CLUSTER")

        # Figure out what the centroid of this Cluster should be
        self.centroid = self.calculateCentroid()

    # Return a string representation of this Cluster
    def __repr__(self):
        return str(self.points)

    # Update function for the K-means algorithm
    # Assigns a new list of Points to this Cluster, returns centroid difference
    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        return getDistance(old_centroid, self.centroid)

    # Calculates the centroid Point - the centroid is the sample mean Point
    # (in plain English, the average of all the Points in the Cluster)
    def calculateCentroid(self):
        centroid_coords = []

        # For each coordinate:
        for i in range(self.n):

            # Take the average across all Points
            centroid_coords.append(0.0)
            for p in self.points:
                centroid_coords[i] = centroid_coords[i]+p.coords[i]
            centroid_coords[i] = centroid_coords[i]/len(self.points)

        # Return a Point object using the average coordinates
        return Point(centroid_coords)

    # Return the single-linkage distance between this and another Cluster
    def getSingleDistance(self, cluster):
        ret = getDistance(self.points[0], cluster.points[0])
        for p in self.points:
            for q in cluster.points:
                distance = getDistance(p, q)
                if distance < ret: ret = distance
        return ret

    # Return the complete-linkage distance between this and another Cluster
    def getCompleteDistance(self, cluster):
        ret = getDistance(self.points[0], cluster.points[0])
        for p in self.points:
            for q in cluster.points:
                distance = getDistance(p, q)
                if distance > ret: ret = distance
        return ret

    # Return the centroid-linkage distance between this and another Cluster
    def getCentroidDistance(self, cluster):
        return getDistance(self.centroid, cluster.centroid)

    # Return the fusion of this and another Cluster
    def fuse(self, cluster):

        # Forbid fusion of Clusters in different spaces
        if self.n != cluster.n: raise Exception("ILLEGAL FUSION")
        points = self.points
        points.extend(cluster.points)
        return Cluster(points)


# -- Return a distance matrix which captures distances between all Clusters
def makeDistanceMatrix(clusters, linkage):
    ret = dict()
    for i in clusters.keys():
        ret[i] = dict()
        for j in clusters.keys():
            if j == i: break
            if linkage == 's':
                ret[i][j] = clusters[i].getSingleDistance(clusters[j])
            elif linkage == 'c':
                ret[i][j] = clusters[i].getCompleteDistance(clusters[j])
            elif linkage == 't':
                ret[i][j] = clusters[i].getCentroidDistance(clusters[j])
            else: raise Exception("INVALID LINKAGE")
    return ret

def removeFromDistancematrix(distances, node):

    if distances.has_key(node):
        del distances[node]

    for key in distances.keys():
        if distances[key].has_key(node):
            del distances[key][node]
    return distances


def addToDistancematrix(clusters, cluster_counter, distances, linkage):
    newnodeid = cluster_counter

    for i in distances.keys():
        if i == newnodeid:
            break
        elif linkage == 's':
            distances[i][newnodeid] = clusters[i].getSingleDistance(clusters[newnodeid])
        elif linkage == 'c':
            distances[i][newnodeid] = clusters[i].getCompleteDistance(clusters[newnodeid])
        elif linkage == 't':
            distances[i][newnodeid] = clusters[i].getCentroidDistance(clusters[newnodeid])
        else: raise Exception("INVALID LINKAGE")

    distances[cluster_counter] = dict()

    for j in distances.keys():
        if j == newnodeid:
            break
        elif linkage == 's':
            distances[newnodeid][j] = clusters[newnodeid].getSingleDistance(clusters[j])
        elif linkage == 'c':
            distances[newnodeid][j] = clusters[newnodeid].getCompleteDistance(clusters[j])
        elif linkage == 't':
            distances[newnodeid][j] = clusters[newnodeid].getCentroidDistance(clusters[j])
        else: raise Exception("INVALID LINKAGE")
    


    return distances
    

# -- Return Clusters of Points formed by agglomerative clustering
def agglo(points, linkage='c', cutoff='20'):

    # Currently, we only allow single, complete, or average linkage
    if not linkage in [ 's', 'c', 't' ]: raise Exception("INVALID LINKAGE")

    # Create singleton Clusters, one for each Point
    clusters = {}
    cluster_counter=-1
    for p in points: 
        cluster_counter+=1
        clusters[cluster_counter] = Cluster([p])
        clustering_debug=1

    

    # Set the min_distance between Clusters to zero
    min_distance = 0

    distances = makeDistanceMatrix(clusters, linkage)

    if clustering_debug == True:
        counter = 0
        counters = {}
        cutoffcount = 0
        sum = 0
        for k in distances.values():
            for p in k.values():
                counter += 1
                if not counters.has_key(p):
                    counters[p] = 0
                counters[p] += 1
                sum += p
        for k in counters.keys():
#            print str(k) + " " + str(counters[k])
            if k < cutoff:
                cutoffcount += counters[k]

#        print "Average distance " + str(sum/counter) 
#        print str(cutoffcount) +" links beneath clustering threshold "+ str(cutoff)
        
    clustering_round = 0
    # Loop until the break statement is made
    while (True):
        clustering_round += 1
        # Compute a distance matrix for all Clusters
        
        if len(clusters) == 1 or len (distances) == 0:
            break
        # Find the key for the Clusters which are closest together
        key0 = distances.keys()[0]

        min_key = [ clusters.keys()[1], clusters.keys()[0] ]
        min_distance = distances[ min_key[0] ][ min_key[1] ]
        
        small_distance_keys=[]
        
        for key1 in distances.keys():
            for key2 in distances[key1].keys():
                if distances[key1][key2] < min_distance:
                    min_key = [key1, key2]
                    min_distance = distances[key1][key2]
                if distances[key1][key2] < cutoff / 3:
                    small_distance_keys.append([key1, key2])


#        min_key = [0][0]
#        min_distance = distances[0][0]
#        
#        for i in range(len(distances)):
#            for j in range(len(distances)):
#                if distances[key] < min_distance:
#                    min_key = key
#                    min_distance = distances[key]
            
        # If the min_distance is bigger than the cutoff, terminate the loop
        # Otherwise, agglomerate the closest clusters
        if min_distance > cutoff or len(clusters) == 1: break
        else:
            if len(small_distance_keys) < 4 :
                c1, c2 = clusters[min_key[0]], clusters[min_key[1]]
                clusters.pop(min_key[0])            
                clusters.pop(min_key[1])
                c3 = c1.fuse(c2)
                cluster_counter += 1
                clusters[cluster_counter] = c3
                
    #            distances = makeDistanceMatrix(clusters, linkage)
    
                distances = removeFromDistancematrix(distances, min_key[0])
                distances = removeFromDistancematrix(distances, min_key[1]) 
                distances = addToDistancematrix(clusters, cluster_counter, distances, linkage)
            else:
                key_map={}
                for min_key in small_distance_keys:
                    while key_map.has_key(min_key[0]):
                        min_key[0] = key_map[min_key[0]]
                    while key_map.has_key(min_key[1]):
                        min_key[1] = key_map[min_key[1]]
                                            
                    c1 = clusters[min_key[0]]
                    c2 = clusters[min_key[1]]

                    if c1 != c2:

                        clusters.pop(min_key[0])            
                        clusters.pop(min_key[1])
                        c3 = c1.fuse(c2)
                        cluster_counter += 1
                        clusters[cluster_counter] = c3

                        key_map[min_key[0]] = cluster_counter;
                        key_map[min_key[1]] = cluster_counter;
                    
                distances = makeDistanceMatrix(clusters, linkage)


        
    # Return the list of Clusters
    return clusters




def lng_to_x(lng):
#    print "conversion lng to x: " + str(lng) + " " + str(round( OFFSET + RADIUS * float(lng) * math.pi / 180))
    return round( OFFSET + RADIUS * float(lng) * math.pi / 180)
    

def lat_to_y(lat):
#    print "conversion lat to y: " + str(lat) + " " + str(round( OFFSET - RADIUS * 
#                  math.log((1 + math.sin( float(lat) * math.pi / 180)) /
#                             (1 - math.sin(float(lat) * math.pi / 180))) / 2))
    return round( OFFSET - RADIUS * 
                  math.log((1 + math.sin( float(lat) * math.pi / 180)) /
                             (1 - math.sin(float(lat) * math.pi / 180))) / 2);

def x_to_lng(x):
#    print "conversion x to lng: " + str(x) +  " " + str(((round(x) - OFFSET) / RADIUS) * 180/ math.pi)
    return ((round(x) - OFFSET) / RADIUS) * 180/ math.pi;

def y_to_lat(y):
#    print "conversion y to lat: " + str(y) +  " " + str((math.pi / 2 - 2 * math.atan(math.exp((round(y) - OFFSET) / RADIUS))) * 180 / math.pi)

    return (math.pi / 2 - 2 * math.atan(math.exp((round(y) - OFFSET) / RADIUS))) * 180 / math.pi

def getDistance(a, b):
    # Forbid measurements between Points in different spaces
    if a.n != b.n: raise Exception("ILLEGAL: NON-COMPARABLE POINTS")


    # Euclidean distance between a and b is sqrt(sum((a[i]-b[i])^2) for all i)
    ret = 0.0
#    for i in range(a.n):
#        ret = ret+pow((a.coords[i]-b.coords[i]), 2)
    
#    print "distance: "+str(math.sqrt(ret))


    if a.zoom != b.zoom: raise Exception("ILLEGAL: DIFFERENT ZOOM LEVELS")

    x1 = a.coords[0] 
    y1 = a.coords[1] 

    x2 = b.coords[0]
    y2 = b.coords[1]

#    print "Marker pixel distance: " +str(int(round(math.sqrt(math.pow(( x1- x2),2) + math.pow(( y1- y2),2)))) >> (21 - a.zoom))
    return int(round(math.sqrt(math.pow(( x1- x2),2) + math.pow(( y1- y2),2)))) >> (21 - a.zoom)

    
#    return math.sqrt(ret)
    
#    x1 = point1.lng
#    y1 = point1.lat
#    
#    x2 = point2.lng
#    y2 = point2.lat
#    
#    return math.sqrt(math.exp((x1-x2),2) + math.exp((y1-y2),2)) >> (21 - zoom); 



def cluster_map_markers(places, zoomlevel, cluster_threshold_pixels=15):
    
        points = []
        for place_id in places.keys():
            points.append(Point([lng_to_x(places[place_id][1]), lat_to_y(places[place_id][0]) ], place_id, zoomlevel))

        #print points
        clusters = agglo(points, 't', cluster_threshold_pixels )
        
        returnarray = []
        for cluster in clusters.values():
            returnpoints = []
            for point in cluster.points:
                returnpoints.append(point.reference)
            returnarray.append([returnpoints, [x_to_lng((cluster.centroid.coords[0])), y_to_lat((cluster.centroid.coords[1]))]])
#            returnarray.append([returnpoints, [x_to_lng(cluster.centroid.coords[0]), y_to_lat(cluster.centroid.coords[1])]])
        return returnarray

originShift = 2 * math.pi * 6378137 / 2.0   # 20037508.342789244
tileSize=256
initialResolution = 2 * math.pi * 6378137 / tileSize
        # 156543.03392804062 for tileSize 256 pixels

def LatLonToMeters(lat, lon ):
    "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"

    mx = lon * originShift / 180.0
    my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)

    my = my * originShift / 180.0
    return mx, my

def MetersToLatLon(mx, my ):
    "Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"

    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0

    lat = 180 / math.pi * (2 * math.atan( math.exp( lat * math.pi / 180.0)) - math.pi / 2.0)
    return lat, lon

def PixelsToMeters(px, py, zoom):
    "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"

    res = self.Resolution( zoom )
    mx = px * res - self.originShift
    my = py * res - self.originShift
    return mx, my
    
def MetersToPixels(mx, my, zoom):
    "Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"
            
    res = self.Resolution( zoom )
    px = (mx + self.originShift) / res
    py = (my + self.originShift) / res
    return px, py

