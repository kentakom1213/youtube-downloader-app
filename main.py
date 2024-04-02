import PySimpleGUI as sg

from downloader import download

# レイアウト
layout = [
    [sg.Text("YouTubeダウンローダー")],
    [sg.Text("↓ ダウンロードしたい動画のURL")],
    [sg.InputText(key="target_url")],
    [
        sg.Radio("音声のみ", "AUDIO/VIDEO", default=True, key="is_audio"),
        sg.Radio("動画", "AUDIO/VIDEO", key="is_video")
    ],
    [sg.FolderBrowse("保存先フォルダ", key="ddir"), sg.Text(key="ddir")],
    [sg.Button("ダウンロード"), sg.Button("Cancel")],
    [sg.Text("\n↓ ダウンロード状況")],
    [sg.ProgressBar(100, key="PROGRESS_BAR"),]
]

# ウィンドウの生成
window = sg.Window("YouTubeダウンローダー", layout)

# イベントループ
while True:
    event, values = window.read()

    if event == "ダウンロード":
        print("ダウンロード開始")
        print(values)

        # プログレスバー描画用の関数
        def progress_bar_update(d: dict):
            if d["downloaded_bytes"] == d["total_bytes"] and d["status"] == "finished":
                sg.popup_ok("ダウンロードが完了しました", title="完了")
                window["PROGRESS_BAR"].update(0)
                return

            percent = round(d["downloaded_bytes"] / d["total_bytes"] * 100)
            window["PROGRESS_BAR"].update(percent)

        try:
            download(values, progress_bar_update)
        except Exception as e:
            print(type(e))
            sg.popup_error(str(e), title="エラー")

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

window.close()
