from aiohttp import web
from src.handlers import handle_pdf_request


async def setup_app():
    app = web.Application()
    app.add_routes([web.post('/', handle_pdf_request)])

    return app
