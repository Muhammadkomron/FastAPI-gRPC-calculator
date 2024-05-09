from enum import Enum, IntEnum
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic._internal._schema_generation_shared import GenerateJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema, SchemaSerializer
from pydantic_core.core_schema import ValidationInfo, CoreSchema
from starlette.middleware.cors import CORSMiddleware

import grpc

import calculator_pb2
import calculator_pb2_grpc

app = FastAPI(
    title="gRPC-calculator",
    version="0.0.1",
    description="this is a simple calculator app with minimal usage grpc in backend",
    terms_of_service="https://example.com/terms/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

channel = grpc.aio.insecure_channel('calculator_grpc:50051')
stub = calculator_pb2_grpc.CalculatorServiceStub(channel)


class OperationEnum(IntEnum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3


@app.get("/calculate/")
async def calculate(x: int, y: int, operation: OperationEnum = Query(..., description="Operation choices")):
    try:
        request = calculator_pb2.CalculationRequest(x=x, y=y, operation=operation)
        response = await stub.PerformCalculation(request)
        return {"result": response.result}
    except grpc.aio.AioRpcError as rpc_error:
        details = rpc_error.details()
        status_code = rpc_error.code()
        if status_code == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=400, detail=details)
        raise HTTPException(status_code=500, detail="Internal Server Error")
