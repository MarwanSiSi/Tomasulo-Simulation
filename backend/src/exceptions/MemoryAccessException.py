class MemoryAccessException(Exception):
    def __init__(self, address):
        self.address = address
        self.message = "Memory access exception at address " + hex(address)
        super().__init__(self.message)
