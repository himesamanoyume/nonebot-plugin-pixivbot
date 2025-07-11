from typing import List, Union, Tuple, Iterable, Sequence

from nonebot import logger

from nonebot_plugin_pixivbot.config import Config
from nonebot_plugin_pixivbot.data.local_tag import LocalTagRepo
from nonebot_plugin_pixivbot.data.pixiv_repo import LazyIllust, PixivRepo
from nonebot_plugin_pixivbot.data.pixiv_repo.remote_repo import RemotePixivRepo
from nonebot_plugin_pixivbot.enums import RandomIllustMethod, RankingMode
from nonebot_plugin_pixivbot.global_context import context
from nonebot_plugin_pixivbot.model import Illust, User
from nonebot_plugin_pixivbot.service.roulette import roulette
from nonebot_plugin_pixivbot.utils.errors import BadRequestError, QueryError

conf = context.require(Config)
repo = context.require(PixivRepo)
local_tags = context.require(LocalTagRepo)
remote_pixiv = context.require(RemotePixivRepo)


@context.register_singleton()
class PixivService:

    @staticmethod
    def _handle_r18(illusts: Iterable[LazyIllust],
                    exclude_r18: bool = False,
                    exclude_r18g: bool = False) -> Iterable[LazyIllust]:
        if not exclude_r18 and not exclude_r18g:
            return illusts
        else:
            def _():
                for x in illusts:
                    if not x.loaded:
                        continue
                    if x.content.has_tag("R-18") and exclude_r18:
                        continue
                    if x.content.has_tag("R-18G") and exclude_r18g:
                        continue
                    yield x

            return _()

    async def _choice_and_load(self, illusts: Sequence[LazyIllust], random_method: RandomIllustMethod, count: int) \
            -> List[Illust]:
        if count <= 0:
            raise BadRequestError("不合法的请求数量")
        if count > conf.pixiv_max_item_per_query:
            raise BadRequestError("数量超过单次请求上限")
        if count > len(illusts):
            raise QueryError("别看了，没有的。")

        winners = roulette(illusts, random_method, count)
        logger.info(f"[pixiv_service] choice {[x.id for x in winners]}")
        return [await x.get() for x in winners]

    async def illust_ranking(self, mode: RankingMode, range: Tuple[int, int]) -> List[Illust]:
        # range 下标从1开始 闭区间
        i = 1
        li = []
        async for x in repo.illust_ranking(mode):
            if i > range[1]:
                break
            elif i >= range[0]:
                li.append(await x.get())
            i += 1
        return li

    async def illust_detail(self, illust: int) -> Illust:
        async for x in repo.illust_detail(illust):
            return x

    async def random_illust(self, word: str,
                            *, count: int = 1,
                            exclude_r18: bool = False,
                            exclude_r18g: bool = False) -> List[Illust]:
        if conf.pixiv_tag_translation_enabled:
            # 只有原word不是标签时获取翻译（例子：唐可可）
            tag = await local_tags.find_by_name(word)
            if not tag:
                tag = await local_tags.find_by_translated_name(word)
                if tag:
                    logger.info(f"[pixiv_service] found translation {word} -> {tag.name}")
                    word = tag.name

        illusts = [x async for x in repo.search_illust(word)]
        illusts = self._handle_r18(illusts, exclude_r18, exclude_r18g)
        return await self._choice_and_load(list(illusts), conf.pixiv_random_illust_method, count)

    async def get_user(self, user: Union[str, int]) -> User:
        if isinstance(user, str):
            async for x in repo.search_user(user):
                logger.info(f"[pixiv_service] select user {x.name}({x.id})")
                return x
            raise QueryError("未找到用户")
        else:
            async for x in repo.user_detail(user):
                return x

    async def random_user_illust(self, user: Union[str, int],
                                 *, count: int = 1,
                                 exclude_r18: bool = False,
                                 exclude_r18g: bool = False) -> Tuple[User, List[Illust]]:
        user = await self.get_user(user)

        illusts = [x async for x in repo.user_illusts(user.id)]
        illusts = self._handle_r18(illusts, exclude_r18, exclude_r18g)
        illust = await self._choice_and_load(list(illusts), conf.pixiv_random_user_illust_method, count)
        return user, illust

    async def random_recommended_illust(self, *, count: int = 1,
                                        exclude_r18: bool = False,
                                        exclude_r18g: bool = False) -> List[Illust]:
        illusts = [x async for x in repo.recommended_illusts()]
        return await self._choice_and_load(illusts, conf.pixiv_random_recommended_illust_method, count)

    async def random_bookmark(self, pixiv_user_id: int = 0,
                              *, count: int = 1,
                              exclude_r18: bool = False,
                              exclude_r18g: bool = False) -> List[Illust]:
        illusts = [x async for x in repo.user_bookmarks(pixiv_user_id)]
        illusts = self._handle_r18(illusts, exclude_r18, exclude_r18g)
        return await self._choice_and_load(list(illusts), conf.pixiv_random_bookmark_method, count)

    async def random_related_illust(self, illust_id: int,
                                    *, count: int = 1,
                                    exclude_r18: bool = False,
                                    exclude_r18g: bool = False) -> List[Illust]:
        if illust_id == 0:
            raise BadRequestError("你还没有发送过请求")

        illusts = [x async for x in repo.related_illusts(illust_id)]
        illusts = self._handle_r18(illusts, exclude_r18, exclude_r18g)
        return await self._choice_and_load(list(illusts), conf.pixiv_random_related_illust_method, count)
    
    async def illust_bookmark_add(self, illust_id: int):
        if illust_id == 0:
            raise BadRequestError("你还没有发送过请求")
        
        await remote_pixiv.illust_bookmark_add(illust_id)
    
    async def illust_bookmark_delete(self, illust_id: int):
        if illust_id == 0:
            raise BadRequestError("你还没有发送过请求")
        
        await remote_pixiv.illust_bookmark_delete(illust_id)


__all__ = ("PixivService",)
