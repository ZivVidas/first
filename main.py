from fastapi import FastAPI

import routers.tasks as rtasks
import routers.auth as auth


app = FastAPI()


app.include_router(rtasks.router)
app.include_router(auth.router)