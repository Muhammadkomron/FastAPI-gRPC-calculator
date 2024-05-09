import logging

import grpc

import calculator_pb2
import calculator_pb2_grpc


class CalculatorServicer(calculator_pb2_grpc.CalculatorServiceServicer):
    async def PerformCalculation(self, request, context):
        try:
            if request.operation == calculator_pb2.ADD:
                result = request.x + request.y
            elif request.operation == calculator_pb2.SUBTRACT:
                result = request.x - request.y
            elif request.operation == calculator_pb2.MULTIPLY:
                result = request.x * request.y
            elif request.operation == calculator_pb2.DIVIDE:
                if request.y == 0:
                    raise ValueError("Cannot divide by zero")
                result = request.x / request.y
            else:
                raise ValueError("Invalid operation")

            response = calculator_pb2.CalculationResponse(result=result)
            logging.info("Calculation finished [%s]", result)
            return response

        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            raise


async def serve(address: str) -> None:
    server = grpc.aio.server()
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port(address)
    await server.start()
    logging.info("Server serving at %s", address)
    await server.wait_for_termination()


if __name__ == '__main__':
    import asyncio

    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve("[::]:50051"))
