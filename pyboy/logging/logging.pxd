cimport cython


cdef int CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG

cdef class Logger:
  cdef str name

  cpdef void critical(self, str, ...) noexcept 
  cpdef void error(self, str, ...) noexcept 
  cpdef void warning(self, str, ...) noexcept 
  cpdef void info(self, str, ...) noexcept 
  cpdef void debug(self, str, ...) noexcept 