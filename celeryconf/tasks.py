import asyncio

from celery import Celery

from prag_ap import SearchFlats

app = Celery("celery_config.tasks", broker="redis://localhost:6379")
# app = Celery("celeryconf.tasks", broker="redis://redis:6379")
app.config_from_object("celeryconf.celeryconfig")


@app.task
def flats_func():
    asyncio.run(SearchFlats.send_me_new_flats())
