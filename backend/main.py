import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.classes.Simulator import Simulator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

simulator = Simulator()


class Config(BaseModel):
    filePath: str

    floatAddSubLatency: int
    floatMulDivLatency: int
    intAddSubLatency: int

    cacheHitLatency: int
    cacheMissLatency: int

    floatAddSubStationSize: int
    floatMulDivStationSize: int
    intAddSubStationSize: int

    loadBufferSize: int
    storeBufferSize: int

    cacheSize: int
    blockSize: int


class ReservationStation(BaseModel):
    busy: bool
    op: str | None
    vj: int | float
    vk: int | float
    qj: str | None
    qk: str | None
    a: int


class Register(BaseModel):
    value: int | float
    busy: bool
    station: str | None


class Cycle(BaseModel):
    cycle: int
    stations: dict[str, dict[str, ReservationStation]]
    registers: dict[str, Register]
    instruction_queue: list[str]
    cache: dict[str, str]


@app.post("/config")
async def set_config(config: Config):
    simulator.load_program(config.filePath)
    simulator.reservation_stations[0].set_size(config.intAddSubStationSize)
    simulator.reservation_stations[1].set_size(config.floatAddSubStationSize)
    simulator.reservation_stations[2].set_size(config.floatMulDivStationSize)

    simulator.reservation_stations[0].latency = config.intAddSubLatency
    simulator.reservation_stations[1].latency = config.floatAddSubLatency
    simulator.reservation_stations[2].latency = config.floatMulDivLatency

    simulator.reservation_stations[3].size = config.loadBufferSize
    simulator.reservation_stations[4].size = config.storeBufferSize

    simulator.memory_manager.block_size = config.blockSize
    simulator.memory_manager.latency = config.cacheHitLatency
    simulator.memory_manager.penalty = config.cacheMissLatency


@app.get("/cycle")
async def get_cycle() -> Cycle:
    simulator.update()
    return Cycle(
        cycle=simulator.cycle,
        stations=await get_stations(),
        registers=await get_register_file(),
        instruction_queue=await get_instruction_queue(),
        cache=await get_cache(),
    )


@app.post("/reset")
async def reset() -> None:
    simulator.reset()


@app.get("/stations")
async def get_stations() -> dict[str, dict[str, ReservationStation]]:
    ret = {}
    for station in simulator.reservation_stations:
        ret[station.name] = {}
        for entry in station.entries:
            ret[station.name][entry.tag] = ReservationStation(
                busy=entry.busy,
                op=entry.op.value if entry.op is not None else None,
                vj=entry.vj,
                vk=entry.vk,
                qj=entry.qj,
                qk=entry.qk,
                a=entry.a,
            )

    return ret


@app.get("/register_file")
async def get_register_file() -> dict[str, Register]:
    ret = {}
    for name, register in simulator.register_file.registers.items():
        ret[name] = Register(
            value=register.value,
            busy=register.Q is not None,
            station=register.Q,
        )

    return ret


@app.get("/instruction_queue")
async def get_instruction_queue() -> list[str]:
    return [str(instruction) for instruction in simulator.instruction_queue]


@app.get("/cache")
async def get_cache() -> dict[str, str]:
    ret = {}
    for address, value in simulator.memory_manager.cache.cache.items():
        ret[str(address)] = str(value)

    return ret


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
