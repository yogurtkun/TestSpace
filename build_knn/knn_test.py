from sklearn.neighbors import NearestNeighbors
import numpy as np
import scipy.spatial.distance as dis

X = np.array([[-1,-1],[2,4],[1,-3],[4,2],[3,5],[2,-4]])

nbrs = NearestNeighbors(n_neighbors=3).fit(X)

(a,b) = nbrs.kneighbors([[1,1]]);

print(b)

len_t = dis.euclidean([1,2],[2,3]);

print(len_t)