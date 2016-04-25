from scipy import sparse
import numpy as np

a = np.array([1,2,0,0,0,4])
b = sparse.csr_matrix(a)
c = b.tocoo()
d = b.__dict__

print(d)
print(d['indices'].tolist())
