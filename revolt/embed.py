from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict, Union

from typing_extensions import NotRequired, Unpack

from .asset import Asset
from .enums import EmbedType

if TYPE_CHECKING:
    from .state import State
    from .types import Embed as EmbedPayload
    from .types import ImageEmbed as ImageEmbedPayload
    from .types import SendableEmbed as SendableEmbedPayload
    from .types import TextEmbed as TextEmbedPayload
    from .types import WebsiteEmbed as WebsiteEmbedPayload

__all__ = ("Embed", "WebsiteEmbed", "ImageEmbed", "TextEmbed", "NoneEmbed", "to_embed", "SendableEmbed")

class WebsiteEmbed:
    type = EmbedType.website

    def __init__(self, embed: WebsiteEmbedPayload):
        self.url = embed.get("url")
        self.special = embed.get("special")
        self.title = embed.get("title")
        self.description = embed.get("description")
        self.image = embed.get("image")
        self.video = embed.get("video")
        self.site_name = embed.get("site_name")
        self.icon_url = embed.get("icon_url")
        self.colour = embed.get("colour")

class ImageEmbed:
    type = EmbedType.image

    def __init__(self, image: ImageEmbedPayload):
        self.url = image.get("url")
        self.width = image.get("width")
        self.height = image.get("height")
        self.size = image.get("size")

class TextEmbed:
    type = EmbedType.text

    def __init__(self, embed: TextEmbedPayload, state: State):
        self.icon_url = embed.get("icon_url")
        self.url = embed.get("url")
        self.title = embed.get("title")
        self.description = embed.get("description")

        if media := embed.get("media"):
            self.media = Asset(media, state)
        else:
            self.media = None

        self.colour = embed.get("colour")

class NoneEmbed:
    type = EmbedType.none

Embed = Union[WebsiteEmbed, ImageEmbed, TextEmbed, NoneEmbed]

def to_embed(payload: EmbedPayload, state: State) -> Embed:
    if payload["type"] == "Website":
        return WebsiteEmbed(payload)
    elif payload["type"] == "Image":
        return ImageEmbed(payload)
    elif payload["type"] == "Text":
        return TextEmbed(payload, state)
    else:
        return NoneEmbed()

class EmbedParameters(TypedDict):
    title: NotRequired[str]
    description: NotRequired[str]
    media: NotRequired[str]
    icon_url: NotRequired[str]
    colour: NotRequired[str]
    url: NotRequired[str]

class SendableEmbed:
    """
    Represents an embed that can be sent in a message, you will never receive this, you will receive :class:`Embed`.

    Attributes
    -----------
    title: Optional[:class:`str`]
        The title of the embed

    description: Optional[:class:`str`]
        The description of the embed

    media: Optional[:class:`str`]
        The file inside the embed, this is the ID of the file, you can use :meth:`Client.upload_file` to get an ID.

    icon_url: Optional[:class:`str`]
        The url of the icon url

    colour: Optional[:class:`str`]
        The embed's accent colour, this is any valid `CSS color <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>`_

    url: Optional[:class:`str`]
        URL for hyperlinking the embed's title
    """
    def __init__(self, **attrs: Unpack[EmbedParameters]):
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.media: Optional[str] = None
        self.icon_url: Optional[str] = None
        self.colour: Optional[str] = None
        self.url: Optional[str] = None

        for key, value in attrs.items():
            setattr(self, key, value)

    def to_dict(self) -> SendableEmbedPayload:
        """Converts the embed to a dictionary which Revolt accepts

        Returns
        --------
        :class:`dict[str, Any]`
            The embed
        """
        output: SendableEmbedPayload = {"type": "Text"}

        if title := self.title:
            output["title"] = title

        if description := self.description:
            output["description"] = description

        if media := self.media:
            output["media"] = media

        if icon_url := self.icon_url:
            output["icon_url"] = icon_url

        if colour := self.colour:
            output["colour"] = colour

        if url := self.url:
            output["url"] = url

        return output
