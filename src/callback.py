from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()
router = APIRouter(prefix='/videotool')

app.include_router(router)

@router.post("/get_callback")
async def get_callback(request: Request):
    try:
        json_data = await request.json()
        challenge = json_data.get("challenge")
        if challenge is not None:
          # is a verification request, just return the challenge
          return {"challenge": challenge}
        else:
            # is a callback request, do your own logic here
            # {
            #     "task_id": "115334141465231360",
            #     "status": "Success",
            #     "file_id": "205258526306433",
            #     "base_resp": {
            #         "status_code": 0,
            #         "status_msg": "success"
            #     }
            # }
            return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, # 必选
        host="0.0.0.0", # 必选
        port=8000, # 必选，端口可设置
        # ssl_keyfile='yourname.yourDomainName.com.key', # 可选，看是否开启ssl
        # ssl_certfile='yourname.yourDomainName.com.key', # 可选，看是否开启ssl
    )