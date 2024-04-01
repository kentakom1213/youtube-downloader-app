import PySimpleGUI as sg

from downloader import download

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
]

# Create the Window
window = sg.Window("YouTubeダウンローダー", layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == "ダウンロード":
        print("ダウンロード開始")
        print(values)

        try:
            download(values)
        except Exception as e:
            print(type(e))
            sg.popup_error(str(e), title="エラー")

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

window.close()
