"""動画のダウンロードを行う
"""

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def handle_error(inner_func):
    """例外処理を行う
    """
    def wrapper(query: dict):
        url = query.get("target_url")
        ddir = query.get("ddir")

        if not url or not ddir:
            raise ValueError("URLと保存先フォルダを指定してください")

        # クエリを渡して実行
        try:
            inner_func(query)
        except Exception as e:
            if isinstance(e, DownloadError):
                raise ValueError("ダウンロードに失敗しました")
            else:
                raise ValueError("予期せぬエラーが発生しました")

    return wrapper


@handle_error
def download(query: dict):
    """動画をダウンロードする
    """
    url, is_audio, ddir = query["target_url"], query["is_audio"], query["ddir"]

    # ダウンロードオプション
    ydl_opts = {
        'format': 'm4a/bestaudio/best' if is_audio else 'best',
        'outtmpl': f'{ddir}/%(title)s.%(ext)s',
    }

    # ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    dragon = "https://www.youtube.com/watch?v=OnCFEo_pXaY"

    download(dragon, "audio")
