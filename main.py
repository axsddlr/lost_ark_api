from fastapi import FastAPI
import uvicorn
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
