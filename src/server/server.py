from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn

# 创建模板和静态文件目录
# templates = Jinja2Templates(directory="templates")

# 处理函数
async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})

async def api_data(request):
    return JSONResponse({"data": "example", "status": "success"})

# 路由配置
routes = [
    Route("/", homepage),
    Route("/api/data", api_data),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)