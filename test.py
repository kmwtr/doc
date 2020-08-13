import logging as log
import sys
import time
import tkinter

log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')

md_txt = ''

# tkinter
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def button_callback():
    # Entryの値を取得
    global md_txt
    md_txt = EditBox.get()
    log.debug('md_txt:\n' + md_txt)
    return True

# ウィンドウ
window = tkinter.Tk()
window.title('md2html')
window.geometry('642x482')
window.configure(background='dimgray')

# ラベル
label = tkinter.Label(text='md テキストをペーストしてください。', foreground='white', background='dimgray')
label.pack(fill='x', ipadx=4, ipady=4, padx=32, pady=8)

# エントリー
EditBox = tkinter.Entry()
#EditBox.insert(tkinter.END, u'Paste here')
EditBox.pack(fill='x', ipadx=4, ipady=4, padx=32, pady=8)

# ボタン
Button = tkinter.Button(text="処理", background='lightgray', command=button_callback)
Button.pack(fill='x', ipadx=4, ipady=4, padx=32, pady=8)


# インフィニティ!!!
window.mainloop()
