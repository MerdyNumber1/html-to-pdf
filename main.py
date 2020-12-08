import pdfkit
from aiohttp import web

from services import format_html_for_pdf, change_img_sources_to_base64


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*',
    'Access-Control-Allow-Headers': '*'
}


async def handle_pdf_request(request):
    """converter from html-layout to pdf-blob"""

    req = await request.json()

    # reformat to valid html for converter
    pdf_html = format_html_for_pdf(req['html'])

    # change src in img to base64 - can raise ConnectionError if put raw link to converter
    pdf_html = await change_img_sources_to_base64(pdf_html, 10)

    # convert html to pdf
    pdf_blob = await pdfkit.from_string(pdf_html, False, options={'quiet': ''})

    return web.Response(body=pdf_blob, headers=headers)


def handle_pdf_options_request(request):
    return web.Response(headers=headers)


app = web.Application()
app.add_routes([web.post('/', handle_pdf_request), web.options('/', handle_pdf_options_request)])

if __name__ == '__main__':
    web.run_app(app, port=80)
