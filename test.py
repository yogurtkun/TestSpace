import numpy as np
import scipy.sparse
from scipy.sparse import csr_matrix

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    '''
    :param filename: str
    :return: scipy.sparse.csr.csr_matrix
    '''
    filename += '.npz'
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),shape = loader['shape'])



a = [[1,2,3],[4,5,6]]
a = csr_matrix(a)
print(a.__dict__)
save_sparse_csr('log',a)

b = load_sparse_csr('log')
print(b.todense())