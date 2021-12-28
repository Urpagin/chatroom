import threading
import socket
from tkinter import Tk, Frame, Text, END, Label
from tkinter.scrolledtext import ScrolledText

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('urpagin.xyz', 45588))


def receive():
    while True:
        global window
        window.update()
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                global chat_box
                print(message)
                chat_box.insert('1.0', message)  # inserer les nouveaux messages dans "ScrolledText" de l'interface
        except:
            print("An error occurred")
            client.close()
            break


def write():
    global send_box
    message = send_box.get("1.0", END)
    try:
        client.send(message.encode('utf-8'))
    except:
        client.send('characteres illegales!!!'.encode('utf-8'))


# ============================== Interface ================================
window = Tk()
window.geometry("1200x900")
window.title("Chat")

chat_box = ScrolledText(window, font=("Calibri", 20), bg="#ecf0f1")
chat_box.pack(expand=True, fill="both")

send_box = ScrolledText(window, font=("Calibri", 20), height=1)
send_box.pack(expand=True, fill="both", side="bottom")
# ============================== Thread ================================

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

window.mainloop()
receive()
