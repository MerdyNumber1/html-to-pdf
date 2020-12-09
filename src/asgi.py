from aiohttp import web
from src.handlers import handle_pdf_request, handle_pdf_options_request


async def setup_app():
    app = web.Application()
    app.add_routes([web.post('/', handle_pdf_request), web.options('/', handle_pdf_options_request)])

    return app
