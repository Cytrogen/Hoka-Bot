import base64
import imagehash
import asyncio
from io import BytesIO
from typing import Tuple, Union, Literal, Optional
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageFile
from imagehash import ImageHash
from nonebot import adapters
from util.text_util import cut_text
from config.path_config import FONT_PATH


def imageToB64(image: Image.Image) -> str:
    """
    :说明: `imageToB64`
    > PIL Image转base64

    :参数:
      * `image: Image.Image`: Image对象

    :返回:
      - `str`: base64://xxxxxxxx
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    base64_str = base64.b64encode(buffer.getvalue()).decode()
    return "base64://" + base64_str


# 从Abot抄来的文字转图片
async def textToImage(text: str, cut: int = 64) -> str:
    """
    :说明: `textToImage`
    > 文字转图片

    :参数:
      * `text: str`: 要转换的文字内容

    :可选参数:
      * `cut: int = 64`: 自动换行字符数限制, 设置为零禁用自动换行

    :返回:
      - `str`: 图片Base64，base64://xxxxxxxx
    """
    font = ImageFont.truetype(f"{FONT_PATH}sarasa-mono-sc-semibold.ttf", 22)
    if cut != 0:
        cut_str = "\n".join(cut_text(text, cut))
    else:
        cut_str = text
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 50, texty + 50), (242, 242, 242))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    imageb64 = imageToB64(image)
    return imageb64


async def textToImageBuf(text: str, cut: int = 64) -> bytes:
    """
    :说明: `textToImageBuf`
    > 文字转图片，返回bytes

    :参数:
      * `text: str`: 要转换的文字内容, 设置为零禁用自动换行

    :可选参数:
      * `cut: int = 64`: 自动换行字符数限制

    :返回:
      - `bytes`: 图片bytes
    """
    font = ImageFont.truetype(f"{FONT_PATH}sarasa-mono-sc-semibold.ttf", 22)
    if cut != 0:
        cut_str = "\n".join(cut_text(text, cut))
    else:
        cut_str = text
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 50, texty + 50), (242, 242, 242))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


class ImageUtil:
    """
    :说明: `ImageUtil`
    > 图片处理工具类
    > Author: HibiKier
    """

    def __init__(
        self,
        width: int,
        height: int,
        paste_image_width: int = 0,
        paste_image_height: int = 0,
        color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = None,
        image_mode: Literal[
            "CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"
        ] = "RGBA",
        font_size: int = 10,
        background: Union[Optional[str], BytesIO, Path] = None,
        font: str = "sarasa-mono-sc-semibold.ttf",
        ratio: float = 1,
        is_alpha: bool = False,
        plain_text: Optional[str] = None,
        font_color: Optional[Tuple[int, int, int]] = None,
    ) -> None:
        """
        :说明: `__init__`
        > 创建图片处理对象

        :参数:
          * `width: int`: 图片宽度
          * `height: int`: 图片高度

        :可选参数:
          * `paste_image_width: int = 0`: 当图片做为背景图时，设置贴图的宽度，用于贴图自动换行
          * `paste_image_height: int = 0`: 当图片做为背景图时，设置贴图的高度，用于贴图自动换行
          * `color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = None`: 生成图片的颜色
          * `image_mode: Literal["CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"] = "RGBA"`: 图片类型
          * `font_size: int = 10`: 字体大小
          * `background: Union[Optional[str], BytesIO, Path] = None`: 背景图片路径
          * `font: str = "sarasa-mono-sc-semibold.ttf"`: 字体路径
          * `ratio: float = 1`: 图片缩放比例
          * `is_alpha: bool = False`: 是否使用透明度
          * `plain_text: Optional[str] = None`: 纯文本内容
          * `font_color: Optional[Tuple[int, int, int]] = None`: 字体颜色

        :错误:
          - `ValueError`: image_mode 不在范围内
        """
        self.width = width
        self.height = height
        self.paste_image_width = paste_image_width
        self.paste_image_height = paste_image_height
        self.current_width = 0
        self.current_height = 0
        self.font = ImageFont.truetype(f"{FONT_PATH}{font}", font_size)
        if image_mode not in ["CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"]:
            raise ValueError(f"image_mode: {image_mode}错误")
        if not color:
            color = (255, 255, 255)
        if not background:
            if plain_text:
                self.width = (
                    self.width
                    if self.width > self.font.getsize(plain_text)[0]
                    else self.font.getsize(plain_text)[1]
                )
                self.height = (
                    self.height
                    if self.height > self.font.getsize(plain_text)[1]
                    else self.font.getsize(plain_text)[1]
                )
            self.mark_image = Image.new(image_mode, (self.width, self.height), color)
            self.mark_image.convert(image_mode)
        else:
            if not width and not height:
                self.mark_image = Image.open(background)
                width, height = self.mark_image.size
                if ratio and ratio > 0 and ratio != 1:
                    self.width = int(ratio * width)
                    self.height = int(ratio * height)
                    self.mark_image = self.mark_image.resize(
                        (self.width, self.height), Image.ANTIALIAS
                    )
                else:
                    self.width = width
                    self.height = height
            else:
                self.mark_image = Image.open(background).resize(
                    (self.width, self.height), Image.ANTIALIAS
                )
        if is_alpha:
            array = self.mark_image.load()
            for i in range(width):
                for j in range(height):
                    pos = array[i, j]  # type: ignore
                    is_edit = sum([1 for x in pos[0:3] if x > 240]) == 3
                    if is_edit:
                        array[i, j] = (255, 255, 255, 0)  # type: ignore
        self.draw = ImageDraw.Draw(self.mark_image)
        self.size = self.width, self.height
        if plain_text:
            fill = font_color if font_color else (0, 0, 0)
            self.text((0, 0), plain_text, fill)

    def text(
        self,
        pos: Tuple[int, int],
        text: str,
        fill: Tuple[int, int, int] = (0, 0, 0),
        center_type: Literal["center", "by_height", "by_width"] = None,
    ):
        """
        :说明: `text`
        > 在图片上添加文本

        :参数:
          * `pos: Tuple[int, int]`: 文本位置
          * `text: str`: 文本内容

        :可选参数:
          * `fill: Tuple[int, int, int] = (0, 0, 0)`: 文本颜色
          * `center_type: Literal["center", "by_height", "by_width"] = None`: 文本居中方式

        :错误:
          * `ValueError`: 当 `center_type` 不为 `center`, `by_height`, `by_width` 时
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            width, height = self.width, self.height
            text_widht, text_height = self.getsize(text)
            if center_type == "center":
                width = int((width - text_widht) / 2)
                height = int((height - text_height) / 2)
            elif center_type == "by_width":
                width = int((width - text_widht) / 2)
                height = pos[1]
            elif center_type == "by_height":
                height = int((height - text_height) / 2)
                width = pos[0]
            pos = (width, height)
        self.draw.text(pos, text, fill=fill, font=self.font)

    def paste(
        self,
        img: Union["ImageUtil", Image.Image],
        pos: Tuple[int, int] = None,
        alpha: bool = False,
        center_type: Literal["center", "by_height", "by_width"] = None,
    ):
        """
        :说明: `paste`
        > 在图片上添加图片

        :参数:
          * `img: ImageUtil`: 图片对象

        :可选参数:
          * `pos: Tuple[int, int] = None`: 图片位置
          * `alpha: bool = False`: 是否使用透明度
          * `center_type: Literal["center", "by_height", "by_width"] = None`: 图片居中方式

        :错误:
          - `ValueError`: 当 `center_type` 不为 `center`, `by_height`, `by_width` 时
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            width, height = 0, 0
            if not pos:
                pos = (0, 0)
            if center_type == "center":
                width = int((self.width - img.width) / 2)
                height = int((self.height - img.height) / 2)
            elif center_type == "by_width":
                width = int((self.width - img.width) / 2)
                height = pos[1]
            elif center_type == "by_height":
                width = pos[0]
                height = int((self.height - img.height) / 2)
            pos = (width, height)
        if isinstance(img, ImageUtil):
            img = img.mark_image
        if self.current_width == self.width:
            self.current_width = 0
            self.current_height += self.paste_image_height
        if not pos:
            pos = (self.current_width, self.current_height)
        if alpha:
            try:
                self.mark_image.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.mark_image.paste(img, pos, img)
        else:
            self.mark_image.paste(img, pos)
        self.current_width += self.paste_image_width

    def getsize(self, msg: str) -> Tuple[int, int]:
        """
        :说明: `getsize`
        > 获取文本大小

        :参数:
          * `msg: str`: 文本内容

        :返回:
          - `Tuple[int, int]`: 文本大小
        """
        return self.font.getsize(msg)

    def point(self, pos: Tuple[int, int], fill: Tuple[int, int, int] = (0, 0, 0)):
        """
        :说明: `point`
        > 绘制单独的像素点

        :参数:
          * `pos: Tuple[int, int]`: 像素点位置

        :可选参数:
          * `fill: Tuple[int, int, int] = (0, 0, 0)`: 像素点颜色
        """
        self.draw.point(pos, fill=fill)

    def ellipse(
        self,
        pos: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        :说明: `ellipse`
        > 绘制描边

        :参数:
          * `pos: Tuple[int, int, int, int]`: 坐标范围[x1, y1, x2, y2]

        :可选参数:
          * `fill: Optional[Tuple[int, int, int]] = None`: 填充颜色
          * `outline: Optional[Tuple[int, int, int]] = None`: 描边颜色
          * `width: int = 1`: 描边宽度
        """
        self.draw.ellipse(pos, fill, outline, width)

    def save(self, path: Union[str, Path]):
        """
        :说明: `save`
        > 保存图片

        :参数:
          * `path: Union[str, Path]`: 保存路径
        """
        if isinstance(path, Path):
            path = path.absolute()
        self.mark_image.save(path)

    def convert(
        self,
        image_mode: Literal[
            "CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"
        ] = "RGBA",
    ):
        """
        :说明: `convert`
        > 转换图片类型

        :可选参数:
          * `image_mode:Literal["CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"] = "RGBA"`: 转换后的图片类型
        """
        self.mark_image = self.mark_image.convert(image_mode)

    def circle(self):
        """
        :说明: `circle`
        > 转换图片为圆形
        """
        self.convert("RGBA")
        r2 = min(self.width, self.height)
        if self.width != self.height:
            self.resize(width=r2, height=r2)
        r3 = int(r2 / 2)
        imb = Image.new("RGBA", (r3 * 2, r3 * 2), (255, 255, 255, 0))
        pim_a = self.mark_image.load()  # 像素的访问对象
        pim_b = imb.load()
        r = float(r2 / 2)
        for i in range(r2):
            for j in range(r2):
                lx = abs(i - r)  # 到圆心距离的横坐标
                ly = abs(j - r)  # 到圆心距离的纵坐标
                length = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径
                if length < r3:
                    pim_b[i - (r - r3), j - (r - r3)] = pim_a[i, j]  # type: ignore
        self.mark_image = imb

    def resize(self, ratio: float = 0, width: int = 0, height: int = 0):
        """
        :说明: `resize`
        > 图片缩放

        :可选参数:
          * `ratio: float = 0`: 缩放比例
          * `width: int = 0`: 缩放后的宽度
          * `height: int = 0`: 缩放后的高度

        :异常:
          - `Exception`: 缺少参数
        """
        if not width and not height and not ratio:
            raise Exception("缺少参数...")
        if not width and not height and ratio:
            width = int(self.width * ratio)
            height = int(self.height * ratio)
        self.mark_image = self.mark_image.resize((width, height), Image.ANTIALIAS)
        self.width, self.height = self.mark_image.size
        self.size = self.width, self.height
        self.draw = ImageDraw.Draw(self.mark_image)

    def toB64(self) -> str:
        """
        :说明: `toB64`
        > 返回Base64编码的图片

        :返回:
          - `str`: Base64编码的图片
        """
        buffer = BytesIO()
        self.mark_image.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode()
        return base64_str


def compare_image_with_hash(
    image_file1: str, image_file2: str, max_dif: int = 1.5
) -> bool:
    """
    说明：
        比较两张图片的hash值是否相同
    参数：
        :param image_file1: 图片文件路径
        :param image_file2: 图片文件路径
        :param max_dif: 允许最大hash差值, 越小越精确,最小为0
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = get_img_hash(image_file1)
    hash_2 = get_img_hash(image_file2)
    dif = hash_1 - hash_2
    if dif < 0:
        dif = -dif
    if dif <= max_dif:
        return True
    else:
        return False


def get_img_hash(image_file: Union[str, Path]) -> ImageHash:
    """
    说明：
        获取图片的hash值
    参数：
        :param image_file: 图片文件路径
    """
    with open(image_file, "rb") as fp:
        hash_value = imagehash.average_hash(Image.open(fp))
    return hash_value


class BuildImage:
    """
    快捷生成图片与操作图片的工具类
    """

    def __init__(
        self,
        w: int,
        h: int,
        paste_image_width: int = 0,
        paste_image_height: int = 0,
        color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = None,
        image_mode: str = "RGBA",
        font_size: int = 10,
        background: Union[Optional[str], BytesIO, Path] = None,
        font: str = "yz.ttf",
        ratio: float = 1,
        is_alpha: bool = False,
        plain_text: Optional[str] = None,
        font_color: Optional[Tuple[int, int, int]] = None,
    ):
        """
        参数：
            :param w: 自定义图片的宽度，w=0时为图片原本宽度
            :param h: 自定义图片的高度，h=0时为图片原本高度
            :param paste_image_width: 当图片做为背景图时，设置贴图的宽度，用于贴图自动换行
            :param paste_image_height: 当图片做为背景图时，设置贴图的高度，用于贴图自动换行
            :param color: 生成图片的颜色
            :param image_mode: 图片的类型
            :param font_size: 文字大小
            :param background: 打开图片的路径
            :param ttf: 字体，默认在 resource/ttf/ 路径下
            :param ratio: 倍率压缩
            :param is_alpha: 是否背景透明
            :param plain_text: 纯文字文本
        """
        self.w = int(w)
        self.h = int(h)
        self.paste_image_width = int(paste_image_width)
        self.paste_image_height = int(paste_image_height)
        self.current_w = 0
        self.current_h = 0
        self.font = ImageFont.truetype(FONT_PATH + font, int(font_size))
        if not plain_text and not color:
            color = (255, 255, 255)
        if not background:
            if plain_text:
                if not color:
                    color = (255, 255, 255, 0)
                ttf_w, ttf_h = self.getsize(plain_text)
                self.w = self.w if self.w > ttf_w else ttf_w
                self.h = self.h if self.h > ttf_h else ttf_h
            self.markImg = Image.new(image_mode, (self.w, self.h), color)
            self.markImg.convert(image_mode)
        else:
            if not w and not h:
                self.markImg = Image.open(background)
                w, h = self.markImg.size
                if ratio and ratio > 0 and ratio != 1:
                    self.w = int(ratio * w)
                    self.h = int(ratio * h)
                    self.markImg = self.markImg.resize(
                        (self.w, self.h), Image.ANTIALIAS
                    )
                else:
                    self.w = w
                    self.h = h
            else:
                self.markImg = Image.open(background).resize(
                    (self.w, self.h), Image.ANTIALIAS
                )
        if is_alpha:
            array = self.markImg.load()
            for i in range(w):
                for j in range(h):
                    pos = array[i, j]
                    is_edit = sum([1 for x in pos[0:3] if x > 240]) == 3
                    if is_edit:
                        array[i, j] = (255, 255, 255, 0)
        self.draw = ImageDraw.Draw(self.markImg)
        self.size = self.w, self.h
        if plain_text:
            fill = font_color if font_color else (0, 0, 0)
            self.text((0, 0), plain_text, fill)
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            self.loop = asyncio.get_event_loop()

    async def apaste(
        self,
        img: "BuildImage" or Image,
        pos: Tuple[int, int] = None,
        alpha: bool = False,
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            异步 贴图
        参数：
            :param img: 已打开的图片文件，可以为 BuildImage 或 Image
            :param pos: 贴图位置（左上角）
            :param alpha: 图片背景是否为透明
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        await self.loop.run_in_executor(None, self.paste, img, pos, alpha, center_type)

    def paste(
        self,
        img: "BuildImage" or Image,
        pos: Tuple[int, int] = None,
        alpha: bool = False,
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            贴图
        参数：
            :param img: 已打开的图片文件，可以为 BuildImage 或 Image
            :param pos: 贴图位置（左上角）
            :param alpha: 图片背景是否为透明
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            width, height = 0, 0
            if not pos:
                pos = (0, 0)
            if center_type == "center":
                width = int((self.w - img.w) / 2)
                height = int((self.h - img.h) / 2)
            elif center_type == "by_width":
                width = int((self.w - img.w) / 2)
                height = pos[1]
            elif center_type == "by_height":
                width = pos[0]
                height = int((self.h - img.h) / 2)
            pos = (width, height)
        if isinstance(img, BuildImage):
            img = img.markImg
        if self.current_w == self.w:
            self.current_w = 0
            self.current_h += self.paste_image_height
        if not pos:
            pos = (self.current_w, self.current_h)
        if alpha:
            try:
                self.markImg.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.markImg.paste(img, pos, img)
        else:
            self.markImg.paste(img, pos)
        self.current_w += self.paste_image_width

    def getsize(self, msg: str) -> Tuple[int, int]:
        """
        说明：
            获取文字在该图片 font_size 下所需要的空间
        参数：
            :param msg: 文字内容
        """
        return self.font.getsize(msg)

    async def apoint(
        self, pos: Tuple[int, int], fill: Optional[Tuple[int, int, int]] = None
    ):
        """
        说明：
            异步 绘制多个或单独的像素
        参数：
            :param pos: 坐标
            :param fill: 填错颜色
        """
        await self.loop.run_in_executor(None, self.point, pos, fill)

    def point(self, pos: Tuple[int, int], fill: Optional[Tuple[int, int, int]] = None):
        """
        说明：
            绘制多个或单独的像素
        参数：
            :param pos: 坐标
            :param fill: 填错颜色
        """
        self.draw.point(pos, fill=fill)

    async def aellipse(
        self,
        pos: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            异步 绘制圆
        参数：
            :param pos: 坐标范围
            :param fill: 填充颜色
            :param outline: 描线颜色
            :param width: 描线宽度
        """
        await self.loop.run_in_executor(None, self.ellipse, pos, fill, outline, width)

    def ellipse(
        self,
        pos: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            绘制圆
        参数：
            :param pos: 坐标范围
            :param fill: 填充颜色
            :param outline: 描线颜色
            :param width: 描线宽度
        """
        self.draw.ellipse(pos, fill, outline, width)

    async def atext(
        self,
        pos: Tuple[int, int],
        text: str,
        fill: Tuple[int, int, int] = (0, 0, 0),
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            异步 在图片上添加文字
        参数：
            :param pos: 文字位置
            :param text: 文字内容
            :param fill: 文字颜色
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        await self.loop.run_in_executor(None, self.text, pos, text, fill, center_type)

    def text(
        self,
        pos: Tuple[int, int],
        text: str,
        fill: Tuple[int, int, int] = (0, 0, 0),
        center_type: Optional[Literal["center", "by_height", "by_width"]] = None,
    ):
        """
        说明：
            在图片上添加文字
        参数：
            :param pos: 文字位置
            :param text: 文字内容
            :param fill: 文字颜色
            :param center_type: 居中类型，可能的值 center: 完全居中，by_width: 水平居中，by_height: 垂直居中
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            w, h = self.w, self.h
            ttf_w, ttf_h = self.getsize(text)
            if center_type == "center":
                w = int((w - ttf_w) / 2)
                h = int((h - ttf_h) / 2)
            elif center_type == "by_width":
                w = int((w - ttf_w) / 2)
                h = pos[1]
            elif center_type == "by_height":
                h = int((h - ttf_h) / 2)
                w = pos[0]
            pos = (w, h)
        self.draw.text(pos, text, fill=fill, font=self.font)

    async def asave(self, path: Union[str, Path]):
        """
        说明：
            异步 保存图片
        参数：
            :param path: 图片路径
        """
        await self.loop.run_in_executor(None, self.save, path)

    def save(self, path: Union[str, Path]):
        """
        说明：
            保存图片
        参数：
            :param path: 图片路径
        """
        if isinstance(path, Path):
            path = path.absolute()
        self.markImg.save(path)

    def show(self):
        """
        说明：
            显示图片
        """
        self.markImg.show(self.markImg)

    async def aresize(self, ratio: float = 0, w: int = 0, h: int = 0):
        """
        说明：
            异步 压缩图片
        参数：
            :param ratio: 压缩倍率
            :param w: 压缩图片宽度至 w
            :param h: 压缩图片高度至 h
        """
        await self.loop.run_in_executor(None, self.resize, ratio, w, h)

    def resize(self, ratio: float = 0, w: int = 0, h: int = 0):
        """
        说明：
            压缩图片
        参数：
            :param ratio: 压缩倍率
            :param w: 压缩图片宽度至 w
            :param h: 压缩图片高度至 h
        """
        if not w and not h and not ratio:
            raise Exception("缺少参数...")
        if not w and not h and ratio:
            w = int(self.w * ratio)
            h = int(self.h * ratio)
        self.markImg = self.markImg.resize((w, h), Image.ANTIALIAS)
        self.w, self.h = self.markImg.size
        self.size = self.w, self.h
        self.draw = ImageDraw.Draw(self.markImg)

    async def acrop(self, box: Tuple[int, int, int, int]):
        """
        说明：
            异步 裁剪图片
        参数：
            :param box: 左上角坐标，右下角坐标 (left, upper, right, lower)
        """
        await self.loop.run_in_executor(None, self.crop, box)

    def crop(self, box: Tuple[int, int, int, int]):
        """
        说明：
            裁剪图片
        参数：
            :param box: 左上角坐标，右下角坐标 (left, upper, right, lower)
        """
        self.markImg = self.markImg.crop(box)
        self.w, self.h = self.markImg.size
        self.size = self.w, self.h
        self.draw = ImageDraw.Draw(self.markImg)

    def check_font_size(self, word: str) -> bool:
        """
        说明：
            检查文本所需宽度是否大于图片宽度
        参数：
            :param word: 文本内容
        """
        return self.font.getsize(word)[0] > self.w

    async def atransparent(self, alpha_ratio: float = 1, n: int = 0):
        """
        说明：
            异步 图片透明化
        参数：
            :param alpha_ratio: 透明化程度
            :param n: 透明化大小内边距
        """
        await self.loop.run_in_executor(None, self.transparent, alpha_ratio, n)

    def transparent(self, alpha_ratio: float = 1, n: int = 0):
        """
        说明：
            图片透明化
        参数：
            :param alpha_ratio: 透明化程度
            :param n: 透明化大小内边距
        """
        self.markImg = self.markImg.convert("RGBA")
        x, y = self.markImg.size
        for i in range(n, x - n):
            for k in range(n, y - n):
                color = self.markImg.getpixel((i, k))
                color = color[:-1] + (int(100 * alpha_ratio),)
                self.markImg.putpixel((i, k), color)
        self.draw = ImageDraw.Draw(self.markImg)

    def pic2bs4(self) -> str:
        """
        说明：
            BuildImage 转 base64
        """
        buf = BytesIO()
        self.markImg.save(buf, format="PNG")
        base64_str = base64.b64encode(buf.getvalue()).decode()
        return base64_str

    def convert(self, type_: str):
        """
        说明：
            修改图片类型
        参数：
            :param type_: 类型
        """
        self.markImg = self.markImg.convert(type_)

    async def arectangle(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: str = None,
        width: int = 1,
    ):
        """
        说明：
            异步 画框
        参数：
            :param xy: 坐标
            :param fill: 填充颜色
            :param outline: 轮廓颜色
            :param width: 线宽
        """
        await self.loop.run_in_executor(None, self.rectangle, xy, fill, outline, width)

    def rectangle(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: str = None,
        width: int = 1,
    ):
        """
        说明：
            画框
        参数：
            :param xy: 坐标
            :param fill: 填充颜色
            :param outline: 轮廓颜色
            :param width: 线宽
        """
        self.draw.rectangle(xy, fill, outline, width)

    async def apolygon(
        self,
        xy: Tuple[int, int],
        fill: Tuple[int, int, int] = (0, 0, 0),
        outline: int = 1,
    ):
        """
        说明:
            异步 画多边形
        参数：
            :param xy: 坐标
            :param fill: 颜色
            :param outline: 线宽
        """
        await self.loop.run_in_executor(None, self.polygon, xy, fill, outline)

    def polygon(
        self,
        xy: Tuple[int, int],
        fill: Tuple[int, int, int] = (0, 0, 0),
        outline: int = 1,
    ):
        """
        说明:
            画多边形
        参数：
            :param xy: 坐标
            :param fill: 颜色
            :param outline: 线宽
        """
        self.draw.polygon(xy, fill, outline)

    async def aline(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            异步 画线
        参数：
            :param xy: 坐标
            :param fill: 填充
            :param width: 线宽
        """
        await self.loop.run_in_executor(None, self.line, xy, fill, width)

    def line(
        self,
        xy: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        说明：
            画线
        参数：
            :param xy: 坐标
            :param fill: 填充
            :param width: 线宽
        """
        self.draw.line(xy, fill, width)

    async def acircle(self):
        """
        说明：
            异步 将 BuildImage 图片变为圆形
        """
        await self.loop.run_in_executor(None, self.circle)

    def circle(self):
        """
        说明：
            将 BuildImage 图片变为圆形
        """
        self.convert("RGBA")
        r2 = min(self.w, self.h)
        if self.w != self.h:
            self.resize(w=r2, h=r2)
        r3 = int(r2 / 2)
        imb = Image.new("RGBA", (r3 * 2, r3 * 2), (255, 255, 255, 0))
        pim_a = self.markImg.load()  # 像素的访问对象
        pim_b = imb.load()
        r = float(r2 / 2)
        for i in range(r2):
            for j in range(r2):
                lx = abs(i - r)  # 到圆心距离的横坐标
                ly = abs(j - r)  # 到圆心距离的纵坐标
                l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径
                if l < r3:
                    pim_b[i - (r - r3), j - (r - r3)] = pim_a[i, j]
        self.markImg = imb

    async def acircle_corner(self, radii: int = 30):
        """
        说明：
            异步 矩形四角变圆
        参数：
            :param radii: 半径
        """
        await self.loop.run_in_executor(None, self.circle_corner, radii)

    def circle_corner(self, radii: int = 30):
        """
        说明：
            矩形四角变圆
        参数：
            :param radii: 半径
        """
        # 画圆（用于分离4个角）
        circle = Image.new("L", (radii * 2, radii * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)
        self.markImg = self.markImg.convert("RGBA")
        w, h = self.markImg.size
        alpha = Image.new("L", self.markImg.size, 255)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
        alpha.paste(
            circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii)
        )
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))
        self.markImg.putalpha(alpha)

    async def arotate(self, angle: int, expand: bool = False):
        """
        说明：
            异步 旋转图片
        参数：
            :param angle: 角度
            :param expand: 放大图片适应角度
        """
        await self.loop.run_in_executor(None, self.rotate, angle, expand)

    def rotate(self, angle: int, expand: bool = False):
        """
        说明：
            旋转图片
        参数：
            :param angle: 角度
            :param expand: 放大图片适应角度
        """
        self.markImg = self.markImg.rotate(angle, expand=expand)

    async def atranspose(self, angle: int):
        """
        说明：
            异步 旋转图片(包括边框)
        参数：
            :param angle: 角度
        """
        await self.loop.run_in_executor(None, self.transpose, angle)

    def transpose(self, angle: int):
        """
        说明：
            旋转图片(包括边框)
        参数：
            :param angle: 角度
        """
        self.markImg.transpose(angle)

    async def afilter(self, filter_: str, aud: int = None):
        """
        说明：
            异步 图片变化
        参数：
            :param filter_: 变化效果
            :param aud: 利率
        """
        await self.loop.run_in_executor(None, self.filter, filter_, aud)

    def filter(self, filter_: str, aud: int = None):
        """
        说明：
            图片变化
        参数：
            :param filter_: 变化效果
            :param aud: 利率
        """
        _x = None
        if filter_ == "GaussianBlur":  # 高斯模糊
            _x = ImageFilter.GaussianBlur
        elif filter_ == "EDGE_ENHANCE":  # 锐化效果
            _x = ImageFilter.EDGE_ENHANCE
        elif filter_ == "BLUR":  # 模糊效果
            _x = ImageFilter.BLUR
        elif filter_ == "CONTOUR":  # 铅笔滤镜
            _x = ImageFilter.CONTOUR
        elif filter_ == "FIND_EDGES":  # 边缘检测
            _x = ImageFilter.FIND_EDGES
        if _x:
            if aud:
                self.markImg = self.markImg.filter(_x(aud))
            else:
                self.markImg = self.markImg.filter(_x)
        self.draw = ImageDraw.Draw(self.markImg)

    #
    def getchannel(self, type_):
        self.markImg = self.markImg.getchannel(type_)


def pic2b64(pic: Image) -> str:
    """
    说明：
        PIL图片转base64
    参数：
        :param pic: 通过PIL打开的图片文件
    """
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str