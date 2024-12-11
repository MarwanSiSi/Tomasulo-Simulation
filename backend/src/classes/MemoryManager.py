from .Cache import Cache


class MemoryManager:
    def __init__(self, latency: int = 1, penalty: int = 5, block_size: int = 1024):
        self.latency = latency
        self.penalty = penalty
        self.block_size = block_size
        self.cache = Cache()
        self.data_memory: dict[int, int | float] = {}
        self.instruction_memory: dict[int, int | float] = {}
        self.requests: dict[str, tuple[int, int]] = {}

    def update(self):
        for tag, (stime, ctime) in self.requests.items():
            self.requests[tag] = (stime, ctime + 1)

    def requestUpdate(self, tag: str, address: int, ctime: int):
        self.requests[tag] = (0, 0)
