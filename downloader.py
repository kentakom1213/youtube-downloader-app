"""動画のダウンロードを行う
"""

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


AUDIO_EXT = "m4a"
VIDEO_EXT = "mp4"
AUDIO_FORMAT = "m4a/bestaudio/best"
VIDEO_FORMAT = "mp4/bestaudio/360p"


def handle_error(inner_func):
    """例外処理を行う
    """
    def wrapper(query: dict, *args):
        url = query.get("target_url")
        ddir = query.get("ddir")

        if not url or not ddir:
            raise ValueError("URLと保存先フォルダを指定してください")

        # エラーログ
        logger = ErrorLogger()

        # クエリを渡して実行
        try:
            inner_func(query, *args, logger=logger)
        except Exception as e:
            if isinstance(e, DownloadError):
                raise ValueError("ダウンロードに失敗しました")
            else:
                print(logger.log)
                if logger.log:
                    raise ValueError(logger.log)
                else:
                    raise ValueError("予期せぬエラーが発生しました")

    return wrapper


class ErrorLogger:
    """エラーログを出力する
    """

    def __init__(self) -> None:
        self.log = ""

    def debug(self, msg):
        print(msg)
        if "has already been downloaded" in msg:
            self.log = "ファイルが既に存在します"

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


@handle_error
def download(query: dict, progress_bar_update=None, logger=None):
    """動画をダウンロードする
    """
    url, is_audio, ddir = query["target_url"], query["is_audio"], query["ddir"]

    # ダウンロードオプション
    ydl_opts = {
        "format": AUDIO_FORMAT if is_audio else VIDEO_FORMAT,
        "outtmpl": f"{ddir}/%(title)s.{AUDIO_EXT if is_audio else VIDEO_EXT}",
        "progress_hooks": [progress_bar_update] if progress_bar_update else [],
    }

    if logger:
        ydl_opts["logger"] = logger

    # ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
