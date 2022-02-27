import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.scrape import LostA
from api.scrape_server import LostA_servers
from ratelimit import limits

app = FastAPI(
    title="Unofficial Lost Ark API",
    description="An Unofficial REST API for [Lost Ark](https://www.playlostark.com/en-us/news), Made by [Andre "
                "Saddler]( "
                "https://github.com/axsddlr)",
    version="1.0.0",
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

# init classes
lost_ark = LostA()
la_servers = LostA_servers()

TWO_MINUTES = 150


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news/{tag}", tags=["News"])
def lost_ark_news(tag):
    """[categories]\n\n

    updates \n
    events\n
    """
    return lost_ark.news(tag)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/v1/forums", tags=["News"])
def lost_ark_forums():
    """
    News and Updates via official news section of forums
    """
    return lost_ark.la_forums_v1()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/v2/forums/{category}", tags=["News"])
def lost_ark_forums(category):
    """
    [categories]\n
    Maintenance\n
    Downtime
    """
    return lost_ark.la_forums_v2(category)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/server/all", tags=["Server Status"])
def lost_ark_all_server_status():
    return la_servers.get_server_list_status()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/server/{monitored_servers}", tags=["Server Status"])
def lost_ark_server_status(monitored_servers):
    """
    Enter Server Name (Case sensitive)\n
    i.e: http://lostarkapi.herokuapp.com/server/Una\n
    result: {"status": 200,"data": {"Una": "✔️ Ok"}}
    """
    return la_servers.get_server_status(monitored_servers)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
