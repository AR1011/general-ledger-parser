from fastapi import FastAPI, Request
import time
import util
import classes
import uvicorn


class API:
    def __init__(self, host: str = "0.0.0.0", port: int = 20500):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self.configure_routes()
        self.configure_middleware()

    def configure_routes(self):
        @self.app.get("/foo")
        def ping():
            return {"message": "bar"}

        @self.app.post("/api/parse")
        async def parse(request: Request):
            csv_bytes = await request.body()
            csv = csv_bytes.decode("utf-8")

            job = classes.AttrDict({"id": util.genUUID()})
            job.time = time.time()

            if (len(csv) > 2**20):  # 1MB
                return {"error": "File too large"}

            parsed, err = util.parseCSV(job, csv)
            if err:
                return {"error": err}

            df = parsed[0]
            predictions = parsed[1]

            err = util.saveCSV(job, df)
            if err:
                return {"error": err}

            data, err = util.dfToJson(df)
            if err:
                data = ""

            return {"message": "success", "job": job, "reformatted_data": data, "predictions": predictions}

    def configure_middleware(self):
        @self.app.middleware("http")
        async def add_custom_headers(request: Request, call_next):
            t0 = time.time()
            response = await call_next(request)
            response_time = time.time() - t0
            response.headers["X-Response-Time"] = util.formatTime(response_time)
            response.headers["X-Served-By"] = "Levenue"
            return response

    def start(self):
        uvicorn.run(self.app, host=self.host, port=self.port)


if __name__ == "__main__":
    util.createDirs()
    api = API()
    api.start()
