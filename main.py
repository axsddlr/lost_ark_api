import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

from api.scrape import LostA
from api.scrape_server import LostA_servers

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Unofficial Lost Ark API",
    description="An Unofficial REST API for [Lost Ark](https://www.playlostark.com/en-us/news), Made by [Andre "
                "Saddler]( "
                "https://github.com/axsddlr)",
    version="1.0.3",
    docs_url="/",
    redoc_url=None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# init classes
lost_ark = LostA()
la_servers = LostA_servers()


@app.get("/news/{tag}", tags=["News"])
@limiter.limit("250/minute")
def lost_ark_news(request: Request, tag):
    """[categories]\n\n

    updates \n
    events\n
    release-notes\n
    general\n
    """
    return lost_ark.news(tag)


@app.get("/forums/tips", tags=["Extras"])
@limiter.limit("250/minute")
def lost_ark_forums_tips(request: Request):
    """
    Guides and Tips via official news section of forums
    """
    return lost_ark.la_forums_tips()


@app.get("/v1/forums", tags=["News"])
@limiter.limit("250/minute")
def lost_ark_forums(request: Request):
    """
    News and Updates via official news section of forums
    """
    return lost_ark.la_forums_v1()


@app.get("/v2/forums/{category}", tags=["News"])
@limiter.limit("250/minute")
def lost_ark_forums(request: Request, category):
    """
    [categories]\n
    Maintenance\n
    Downtime
    """
    return lost_ark.la_forums_v2(category)


@app.get("/steam/playercount", tags=["Server Status"])
@limiter.limit("250/minute")
def steam_playercount(request: Request):
    return lost_ark.la_playercount()


@app.get("/server/all", tags=["Server Status"])
@limiter.limit("250/minute")
def lost_ark_all_server_status(request: Request):
    return la_servers.get_server_list_status()


@app.get("/server/{monitored_servers}", tags=["Server Status"])
@limiter.limit("250/minute")
def lost_ark_server_status(request: Request, monitored_servers):
    """
    Enter Server Name (Case sensitive)\n
    i.e: http://lostarkapi.herokuapp.com/server/Una\n
    result: {"status": 200,"data": {"Una": "✔️ Ok"}}
    """
    return la_servers.get_server_status(monitored_servers)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
