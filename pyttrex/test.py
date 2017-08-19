def foo(bar, baz):
  print('hello {0}'.format(bar))
  return 'foo' + baz

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=4)

async_result = pool.apply_async(foo, ('world', 'foo')) # tuple of args for foo
pool.apply_async(foo, ('world', 'foo'))
pool.apply_async(foo, ('world', 'foo'))
# do some other stuff in the main process

return_val = async_result.get()  #