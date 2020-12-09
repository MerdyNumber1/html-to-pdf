from src.services import convert_html_to_pdf
from loguru import logger
from time import time
from aiohttp import web

logger.add('logs/out.log')

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*',
    'Access-Control-Allow-Headers': '*'
}


async def handle_pdf_request(request):
    """converter from html-layout to pdf-blob"""

    req = await request.json()

    if req and len(req['html']):

        logger.info('-------- REQUEST --------')
        start_time = time()

        pdf_blob = await convert_html_to_pdf(req['html'])

        logger.info(f'{round(time() - start_time, 2)} sec. - {len(req["html"])} page(s)')
        logger.info('---- END OF REQUEST -----')

        return web.Response(body=pdf_blob, headers=headers)

    return web.Response(text='{success: false}', headers=headers)


def handle_pdf_options_request(request):
    return web.Response(headers=headers)
