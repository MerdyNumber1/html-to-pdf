import base64
import pdfkit

from aiohttp import ClientSession, ClientError
from bs4 import BeautifulSoup
from loguru import logger
from time import time


async def get_img_content(session, img):
    async with session.get(img['src']) as resp:
        return await resp.read(), resp.headers['Content-Type']


def format_html_for_pdf(html_pages):
    html = "<meta charset='utf-8' />"
    for page in html_pages:
        html += f'<div style="page-break-before: always;">{page}</div>'
    return html


async def change_img_sources_to_base64(html, retries):
    html = BeautifulSoup(html, "lxml")

    async with ClientSession() as session:
        for img in html.find_all("img"):
            start_time = time()
            for i in range(retries):
                try:
                    logger.info('ConnectionClose - retrying to get image')
                    img_content, image_type = await get_img_content(session, img)
                except ClientError:
                    continue
                else:
                    logger.info(f'{round(time() - start_time, 2)} sec. - get image content {img["src"]}')
                    img['src'] = f'data:{image_type};base64,{base64.b64encode(img_content).decode("utf-8")}'
                    break

    return str(html)


async def convert_html_to_pdf(html):
    html = format_html_for_pdf(html)

    # change src in img to base64 - can raise ConnectionError if put raw link to converter
    html = await change_img_sources_to_base64(html, 10)

    # convert html to pdf
    return await pdfkit.from_string(html, False, options={'quiet': ''})
