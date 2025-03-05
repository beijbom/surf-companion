import modal
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from sqlmodel import Session, SQLModel, create_engine

import client
import stuff
from config import sqlite_url
from datamodel import Rating, SurfSession

web_app = FastAPI()
app = modal.App(name="SurfCompanion")

volume = modal.Volume.from_name("surf-companion", create_if_missing=True)

favicon_path = "/static/favicon.ico"

modal_image = (
    modal.Image.debian_slim()
    .apt_install(["libgl1-mesa-glx", "libglib2.0-0"])
    .pip_install_from_pyproject("pyproject.toml")
    .add_local_python_source("datamodel", "config")
    .add_local_dir("static", remote_path="/static")
)


@web_app.get("/")
async def homepage(request: Request):
    return client.homepage(request)


@web_app.get("/log")
async def log():
    return client.log_form()


@web_app.post("/log_session")
async def log_session(request: Request):
    form_data = await request.form()

    # Convert form data to appropriate types
    surfer_id = int(form_data.get("surfer_id"))
    spot_id = int(form_data.get("spot_id"))
    crowd = Rating(int(form_data.get("crowd"))) if form_data.get("crowd") else None
    wind = Rating(int(form_data.get("wind"))) if form_data.get("wind") else None
    waves = Rating(int(form_data.get("waves"))) if form_data.get("waves") else None

    # Create and save the session
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        surf_session = SurfSession(surfer_id=surfer_id, spot_id=spot_id, crowd=crowd, wind=wind, waves=waves)
        session.add(surf_session)
        session.commit()

    return RedirectResponse(url="/?success=Session+added", status_code=303)


@web_app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.function(image=modal_image, container_idle_timeout=60, volumes={"/data": volume})
@modal.asgi_app()
def surf_companion():
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)
    stuff.initialize_db()

    return web_app
