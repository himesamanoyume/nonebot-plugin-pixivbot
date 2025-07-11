from io import BytesIO
from typing import Optional

from pydantic import BaseModel
from tzlocal import get_localzone

from .. import Illust
from ...config import Config
from ...data.pixiv_repo import PixivRepo
from ...enums import BlockAction
from ...global_context import context

conf = context.require(Config)


async def download_image(illust: Illust, page: int):
    with BytesIO() as bio:
        repo = context.require(PixivRepo)
        async for x in repo.image(illust, page):
            bio.write(x)
            break
        return bio.getvalue()


class IllustMessageModel(BaseModel):
    id: int
    title: str = ""
    author: str = ""
    create_time: str = ""
    link: str = ""
    image: bytes = bytes(0)
    tags: list = []
    is_bookmarked: bool = False
    total_view: int = 0
    total_bookmarks: int = 0
    width: int = 0
    height: int = 0

    header: Optional[str]
    number: Optional[int]

    page: int
    total: int

    block_action: Optional[BlockAction] = None
    block_message: str = ""

    @staticmethod
    async def from_illust(illust: Illust, *,
                          header: Optional[str] = None,
                          number: Optional[int] = None,
                          page: int = 0,
                          block_r18: bool = False,
                          block_r18g: bool = False) -> Optional["IllustMessageModel"]:
        model = IllustMessageModel(id=illust.id, header=header, number=number, page=page, total=illust.page_count)

        block_tags = [*conf.pixiv_block_tags]
        if block_r18:
            block_tags.append("R-18")
        if block_r18g:
            block_tags.append("R-18G")

        if illust.has_tags(block_tags):
            model.block_action = conf.pixiv_block_action
            if conf.pixiv_block_action == BlockAction.no_image:
                model.block_message = "该画像因含有不可描述的tag而被自主规制"
            elif conf.pixiv_block_action == BlockAction.completely_block:
                model.block_message = "该画像因含有不可描述的tag而被自主规制"
                return model
            elif conf.pixiv_block_action == BlockAction.no_reply:
                return None
        else:
            model.image = await download_image(illust, page)
        model.title = illust.title
        model.author = f"{illust.user.name} ({illust.user.id})"
        model.create_time = illust.create_date.astimezone(get_localzone()).strftime('%Y-%m-%d %H:%M:%S')
        model.link = f"https:\n//www.pixiv\n.net/artworks/{illust.id}"
        model.tags = illust.tags
        model.total_view = illust.total_view
        model.total_bookmarks = illust.total_bookmarks
        model.is_bookmarked = illust.is_bookmarked
        model.width = illust.width
        model.height = illust.height

        return model
