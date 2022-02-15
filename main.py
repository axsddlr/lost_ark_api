import uvicorn
from fastapi import FastAPI

from api.scrape import LostA
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

# init classes
lost_ark = LostA()

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
@app.get("/server/all", tags=["Server Status"])
def lost_ark_all_server_status():
    return lost_ark.get_server_list_status()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/server/{monitored_servers}", tags=["Server Status"])
def lost_ark_server_status(monitored_servers):
    """
    Enter Server Name\n
    i.e: http://lostarkapi.herokuapp.com/server/Una\n
    result: {'Una': '✅'}
    """
    return lost_ark.get_server_status(monitored_servers)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
