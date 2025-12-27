# serial.pxd

cdef int SERIAL_FREQ, CPU_FREQ

cdef class Serial:
    cdef object mb
    cdef int SC
    cdef int SB
    cdef object link_send
    cdef object recv_queue
    cdef int trans_bits
    cdef int cycles_count
    cdef int cycles_target
    cdef unsigned long long _cycles_to_interrupt
    cpdef bint tick(self, int cycles) noexcept
    cpdef void set_SB(self, uint8_t) noexcept
    cpdef void set_SC(self, uint8_t) noexcept
