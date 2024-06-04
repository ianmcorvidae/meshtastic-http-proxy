from fastapi import FastAPI, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from meshtastic.tcp_interface import TCPInterface
from meshtastic.ble_interface import BLEInterface
from meshtastic.mesh_pb2 import FromRadio, ToRadio
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Union
from typing_extensions import Annotated
from contextlib import asynccontextmanager
import bleak
import logging
import os

if os.getenv('DEBUG'):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

bufs: List[bytes] = []

class WrappedTCPInterface(TCPInterface):

    def __init__(self, *args, **kwargs):
        TCPInterface.__init__(self, *args, **kwargs)

    def _handleFromRadio(self, fromRadioBytes: bytes):
        bufs.append(fromRadioBytes)
        return TCPInterface._handleFromRadio(self, fromRadioBytes)

class WrappedBLEInterface(BLEInterface):

    def __init__(self, *args, **kwargs):
        BLEInterface.__init__(self, *args, **kwargs)

    def _handleFromRadio(self, fromRadioBytes: bytes):
        bufs.append(fromRadioBytes)
        return BLEInterface._handleFromRadio(self, fromRadioBytes)

client: Optional[Union[WrappedBLEInterface, WrappedTCPInterface]] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    host = os.getenv("MESHTASTIC_TCP_HOST") or "localhost"
    ble_host = os.getenv("MESHTASTIC_BLE_MAC")
    if ble_host is None or ble_host == "":
        client = WrappedTCPInterface(host)
    else:
        try:
            client = WrappedBLEInterface(ble_host)
        except bleak.exc.BleakDBusError:
            print("Trying a second connect attempt")
            try:
                client = WrappedBLEInterface(ble_host)
            except bleak.exc.BleakDBusError:
                print("Trying a third connect attempt")
                client = WrappedBLEInterface(ble_host)
    yield
    client.close()
    client = None

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class TFStr(Enum):
    TRUE = "true"
    FALSE = "false"

@app.put("/api/v1/toradio")
async def toradio(buf: Annotated[bytes, Body()]):
    global client
    to = ToRadio()
    to.ParseFromString(buf)
    if client is not None:
        client._sendToRadio(to)
    else:
        return HTMLResponse('<html><body>no client, fix this</body></html>')

@app.get("/api/v1/fromradio")
async def fromradio(all: TFStr="false"):
    global bufs
    content: bytes = b""
    if all == TFStr.TRUE:
        content = b"".join(bufs)
    elif len(bufs) > 0:
        content = bufs.pop(0)
    return Response(content=content, media_type="application/x-protobuf")
