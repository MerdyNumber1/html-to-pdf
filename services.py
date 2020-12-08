import base64
from aiohttp import ClientSession, ClientError
from bs4 import BeautifulSoup


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
            for i in range(retries):
                try:
                    img_content, image_type = await get_img_content(session, img)
                except ClientError:
                    continue
                else:
                    img['src'] = f'data:{image_type};base64,{base64.b64encode(img_content).decode("utf-8")}'
                    break

    return str(html)