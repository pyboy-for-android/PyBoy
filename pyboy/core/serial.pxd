# serial.pxd

cdef int INTR_VBLANK, INTR_LCDC, INTR_TIMER, INTR_SERIAL, INTR_HIGHTOLOW
cdef int SERIAL_FREQ, CPU_FREQ
cdef object async_recv

cdef class Serial:
    cdef object mb
    cdef int SC
    cdef int SB
    cdef object connection
    cdef object recv
    cdef object recv_t
    cdef bint quitting
    cdef int trans_bits
    cdef int cycles_count
    cdef int cycles_target
    cdef int serial_interrupt_based
    cdef bint waiting_for_byte
    cdef int byte_retry_count
    cdef object binding_connection
    cdef int is_master
    cdef bint transfer_enabled
    cdef unsigned long long _cycles_to_interrupt

    cpdef send_bit(self)
    cpdef bint tick(self, int cycles) noexcept 
    cpdef void set_SB(self, uint8_t) noexcept 
    cpdef void set_SC(self, uint8_t) noexcept 
    cpdef int cycles_to_transmit(self) noexcept 
    cpdef stop(self)
