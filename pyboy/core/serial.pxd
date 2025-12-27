from libc.stdint cimport uint8_t

# Definimos estas constantes por si otros módulos las importan, 
# aunque tu lógica actual de Serial ya no las usa para el timing.
cdef int SERIAL_FREQ
cdef int CPU_FREQ

cdef class Serial:
    cdef object mb
    cdef int SC
    cdef int SB
    
    # Objetos de Python para la comunicación
    cdef object link_send
    cdef object recv_queue
    cdef unsigned long long _cycles_to_interrupt
    
    # Flags de estado
    cdef bint sent
    cdef bint stopped
    
    # NOTA: He eliminado cycles_count, cycles_target y _cycles_to_interrupt
    # porque tu __init__ en Python ya no los define.

    # Métodos
    # Usamos 'int' en value para permitir que Python pase cualquier entero
    # y tu código haga el masking (& 0xFF) internamente sin errores de overflow previo.
    cpdef void set_SB(self, int value) noexcept
    cpdef void set_SC(self, int value) noexcept
    
    cpdef bint tick(self, int cycles) noexcept
    cpdef void stop(self) noexcept