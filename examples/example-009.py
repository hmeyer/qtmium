

def count_zeroes(lst):
	return sum(1 for x in lst if x == 0)


def partial_menger_void(k, iter=2):
  core = Box(k/3,k/3,100,center=True) 
  if iter>1:
    for x in [-1,0,1]:
      for y in [-1,0,1]:
          if count_zeroes([x,y]) <= 1:
            core += partial_menger_void(k/3, iter-1).translate(x*k/3, y*k/3, 0)
  return core

def menger_void(k, iter=2):
	pv = partial_menger_void(k, iter)
	pv += partial_menger_void(k, iter).rotate(X_axis,90)
	pv += partial_menger_void(k, iter).rotate(Y_axis,90)
	return pv
  
print 'This will take a while...'
result = Box(27,27,27,center=True) - menger_void(27)
