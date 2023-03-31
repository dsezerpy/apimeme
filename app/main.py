from fastapi import FastAPI, Response,Request,status
from fastapi.responses import PlainTextResponse,StreamingResponse
from json import load,loads
import random,asyncio

app = FastAPI()
database = load(open("database.json", "r"))


@app.post("/codetocrash")
async def codetocrash(req:Request):
    """returns code that crashes a process depending on the coding language submitted via xml
    idea from: https://github.com/somerandomcloud
    format:
    <?xml version="1.0" encoding="UTF-8" ?>
        <root>
            <lang>language goes here</lang>
        </root>
    example request body: just send the plain xml to the api"""
    data = (await req.body()).decode("utf-8").split("<lang>")[1].split("</lang>")[0].replace("\t","").replace("\n","")\
            .replace("\r","").lower()
    if data in database.keys():
        return PlainTextResponse(database[data])
    else:
        return PlainTextResponse("We currently cant crash this language, if you know how please submit a PR @ https://github.com/dsezerpy/apimeme")


@app.get("/mystery")
async def mystery(response:Response):
    """returns random amount of bytes, content type application/octet-stream sends single byte each second
    idea from: https://github.com/Aaron2550"""
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Transfer-Encoding"] = "chunked"

    async def generate_bytes():
        num_bytes = random.randint(1, 100)
        print("generating ", num_bytes, " bytes to send")
        bytes_data = bytes([random.randint(0, 255) for _ in range(num_bytes)])
        for byte in bytes_data:
            yield bytes([byte])
            await asyncio.sleep(1)

    return StreamingResponse(generate_bytes())
