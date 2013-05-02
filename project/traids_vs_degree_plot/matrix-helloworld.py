import scipy
import numpy
from scipy.sparse import csc_matrix

a = scipy.array([[1, 2, 3], [4, 5, 6], [4, 5, 6]])
b = scipy.asmatrix(a)
print "b"
print b
print "b.tolist()[1][1]"
print b.tolist()[1][1]


print "numpy.dot(b, b)"
print numpy.dot(b, b)
squared_matrix = csc_matrix(b) * csc_matrix(b)
squared_matrix1 = csc_matrix(b).getrow(1).getcol(1)
#print squared_matrix
print "squared_matrix.tobsr()"
print squared_matrix.tobsr()
print "abc"
print "squared_matrix.todense()"
print squared_matrix.todense()
print "squared_matrix.todense().tolist()[1][1]"
print squared_matrix.todense().tolist()[1][1]