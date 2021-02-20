# Necro(ネクロ)
# sidmishra94540@gmail.com

import os, requests, sys, time, PIL.Image
from tkinter import *
import webbrowser
def reset(MANGA_PATH):
    log.insert(END, 'TASK STARTED\n')
    log.see(END)
    root.update()
    for manga in os.listdir(MANGA_PATH):
        if manga[0]=='!' or manga=='$RECYCLE.BIN':
            continue
        try:
            log.insert(END, ' >Scanning folder ' + manga + '...\n')
            log.see(END)
            root.update()
            try:
                os.remove(MANGA_PATH + manga + '/!ndex.txt')
                log.insert(END, '  -Removed !ndex.txt from: ' + manga + '\n')
                log.see(END)
                root.update()
            except:
                pass
            try:
                os.remove(MANGA_PATH + manga + '/!con.ico')
                log.insert(END, '  -Removed icon from: ' + manga + '\n')
                log.see(END)
                root.update()
            except:
                pass
            try:
                os.remove(MANGA_PATH + manga +  '/desktop.ini')
                log.insert(END, '  -Removed configuration file from: ' + manga + '\n')
                log.see(END)
                root.update()
            except:
                pass
            for part in os.listdir(MANGA_PATH + manga):
                log.insert(END, ' >Scanning sub-folder ' + part + '...\n')
                log.see(END)
                root.update()
                try:
                    os.remove(MANGA_PATH + manga + '/' + part + '/!ndex.txt')
                    log.insert(END, '  -Removed !ndex.txt from: ' + part + '\n')
                    log.see(END)
                    root.update()
                except:
                    pass
                try:
                    os.remove(MANGA_PATH + manga + '/' + part + '/!con.ico')
                    log.insert(END, '  -Removed icon from: ' + part + '\n')
                    log.see(END)
                    root.update()
                except:
                    pass
                try:
                    os.remove(MANGA_PATH + manga + '/' + part + '/desktop.ini')
                    log.insert(END, '  -Removed configuration file from: ' + part + '\n')
                    log.see(END)
                    root.update()
                except:
                    pass
        except:
            continue
    log.insert(END, 'TASK ENDED\n')
    log.see(END)
    root.update()
def generate(MANGA_PATH):
    log.insert(END, 'TASK STARTED\n')
    log.see(END)
    root.update()
    for manga in os.listdir(MANGA_PATH):
        if manga[0]=='!' or manga=='$RECYCLE.BIN':
            continue
        try:
            log.insert(END, ' >Scanning folder ' + manga + '...\n')
            log.see(END)
            root.update()
            if os.path.exists(MANGA_PATH + manga + '/!ndex.txt') and open(MANGA_PATH + manga + '/!ndex.txt', 'r').read():
                log.insert(END, '  -Manga ID present for ' + manga + '\n')
                log.see(END)
                root.update()
            else:
                log.insert(END, '  -Enter Manga ID for ' + manga + ': ')
                log.see(END)
                root.update()
                index = open(MANGA_PATH + manga + '/!ndex.txt', 'w')
                var = IntVar()
                log.bind('<Return>', lambda e: var.set(1))
                root.wait_variable(var)
                index.write(log.get('1.0',END).split(':')[-1].strip())
                index.close()
            for part in os.listdir(MANGA_PATH + manga):
                if part == '!ndex.txt' or part == 'desktop.ini' or part == '!con.ico':
                    continue
                log.insert(END, ' >Scanning sub-folder ' + part + '...\n')
                log.see(END)
                root.update()
                if os.path.exists(MANGA_PATH + manga + '/' + part + '/!ndex.txt') and open(MANGA_PATH + manga + '/' + part + '/!ndex.txt', 'r').read():
                    log.insert(END, '  -Manga ID present for ' + part + '\n')
                    log.see(END)
                    root.update()
                    continue
                log.insert(END, '  -Enter Manga ID for ' + part + ': ')
                log.see(END)
                root.update()
                index = open(MANGA_PATH + manga + '/' + part + '/!ndex.txt', 'w')
                var = IntVar()
                log.bind('<Return>', lambda e: var.set(1))
                root.wait_variable(var)
                index.write(log.get('1.0',END).split(':')[-1].strip())
                index.close()
        except:
            continue
    log.insert(END, 'TASK ENDED\n')
    log.see(END)
    root.update()
def setIcon(MANGA_PATH):
    log.insert(END, 'TASK STARTED\n')
    log.see(END)
    root.update()
    for manga in os.listdir(MANGA_PATH):
        if manga[0]=='!' or manga=='$RECYCLE.BIN':
            continue
        try:
            log.insert(END, ' >Scanning folder ' + manga + '...\n')
            log.see(END)
            root.update()
            flag = 1
            if os.path.exists(MANGA_PATH + manga + '/desktop.ini'):
                log.insert(END, '  -Folder icon already set' + '\n')
                log.see(END)
                root.update()
                flag = 0
            index = open(MANGA_PATH + manga + '/!ndex.txt', 'r')
            data = index.read()
            if(not data):
                log.insert(END, '  -!ndex.txt is empty' + '\n')
                log.see(END)
                root.update()
                flag = 0
            if flag:
                variables = {
                'id': data
                }
                index.close()
                query = '''
                query ($id: Int) {
                    Media (id: $id, type: MANGA) {
                        id
                        title {
                            english
                            romaji
                        }
                        coverImage{
                            extraLarge
                        }
                    }
                }
                '''
                log.insert(END, '  -Connecting to server' + '\n')
                log.see(END)
                root.update()
                response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']
                title_base = response['title']['english'] if response['title']['english'] else response['title']['romaji']
                title_base = title_base.replace('&', 'and').replace('/', '~').replace(':', '~').replace('*', '~').replace('?', '~').replace('"', '~').replace('<', '~').replace('>', '~').replace('|', '~')
                cover = response['coverImage']['extraLarge']
                image = MANGA_PATH + manga + '/!con' + os.path.splitext(cover)[1]
                log.insert(END, '  -Downloading icon' + '\n')
                log.see(END)
                root.update()
                open(image, 'wb').write(requests.get(cover).content)
                log.insert(END, '  -Optimizing icon' + '\n')
                log.see(END)
                root.update()
                icon = PIL.Image.open(image)
                width, height = icon.size
                crop = width if width <= height else height
                icon = icon.crop(((width - crop) // 2, (height - crop) // 2, (width + crop) // 2, (height + crop) // 2)).resize((256,256))
                icon.save(os.path.splitext(image)[0] + '.ico', format = 'ICO', sizes=[(256,256)], quality=95)
                os.remove(image)
                log.insert(END, '  -Applying changes' + '\n')
                log.see(END)
                root.update()
                os.system(MANGA_PATH[0] + ': & cd ' + MANGA_PATH + ' & attrib +s "' + manga + '" & cd ' + manga + ' & echo [.ShellClassInfo] > desktop.ini & echo IconResource=!con.ico,0 >> desktop.ini & attrib +s +h desktop.ini & attrib +h !con.ico & attrib +h !ndex.txt')
                log.insert(END, '  -Icon set' + '\n')
                log.see(END)
                root.update()
                time.sleep(1)
            for part in os.listdir(MANGA_PATH + manga):
                if part == '!ndex.txt' or part == 'desktop.ini' or part == '!con.ico':
                    continue
                log.insert(END, ' >Scanning sub-folder ' + part + '...\n')
                log.see(END)
                root.update()
                flagIn = 1
                if os.path.exists(MANGA_PATH + manga + '/' + part + '/desktop.ini'):
                    log.insert(END, '  -Sub-folder icon already set' + '\n')
                    log.see(END)
                    root.update()
                    flagIn = 0
                index = open(MANGA_PATH + manga + '/' + part + '/!ndex.txt', 'r')
                data = index.read()
                if(not data):
                    log.insert(END, '  -!ndex.txt is empty' + '\n')
                    log.see(END)
                    root.update()
                    flagIn = 0
                if flagIn:
                    variables = {
                    'id': data
                    }
                    index.close()
                    query = '''
                    query ($id: Int) {
                        Media (id: $id, type: MANGA) {
                            id
                            title {
                                english
                                romaji
                            }
                            coverImage{
                                extraLarge
                            }
                        }
                    }
                    '''
                    log.insert(END, '  -Connecting to server' + '\n')
                    log.see(END)
                    root.update()
                    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']
                    title = response['title']['english'] if response['title']['english'] else response['title']['romaji']
                    title = title.replace('&', 'and').replace('/', '~').replace(':', '~').replace('*', '~').replace('?', '~').replace('"', '~').replace('<', '~').replace('>', '~').replace('|', '~')
                    cover = response['coverImage']['extraLarge']
                    image = MANGA_PATH + manga + '/' + part + '/!con' + os.path.splitext(cover)[1]
                    log.insert(END, '  -Downloading icon' + '\n')
                    log.see(END)
                    root.update()
                    open(image, 'wb').write(requests.get(cover).content)
                    log.insert(END, '  -Optimizing icon' + '\n')
                    log.see(END)
                    root.update()
                    icon = PIL.Image.open(image)
                    width, height = icon.size
                    crop = width if width <= height else height
                    icon = icon.crop(((width - crop) // 2, (height - crop) // 2, (width + crop) // 2, (height + crop) // 2)).resize((256,256))
                    icon.save(os.path.splitext(image)[0] + '.ico', format = 'ICO', sizes=[(256,256)], quality=95)
                    os.remove(image)
                    log.insert(END, '  -Applying changes' + '\n')
                    log.see(END)
                    root.update()
                    os.system(MANGA_PATH[0] + ': & cd ' + MANGA_PATH + manga + ' & attrib +s "' + part + '" & cd ' + part + ' & echo [.ShellClassInfo] > desktop.ini & echo IconResource=!con.ico,0 >> desktop.ini & attrib +s +h desktop.ini & attrib +h !con.ico & attrib +h !ndex.txt')
                    log.insert(END, '  -Renaming sub-folder' + '\n')
                    log.see(END)
                    root.update()
                    os.rename(MANGA_PATH + manga + '/' + part, MANGA_PATH + manga + '/' + title)
                    log.insert(END, '  -Icon set' + '\n')
                    log.see(END)
                    root.update()
                    time.sleep(1)
            log.insert(END, '  -Renaming folder' + '\n')
            log.see(END)
            root.update()
            os.rename(MANGA_PATH + manga, MANGA_PATH + title_base)
        except:
            continue
    log.insert(END, 'TASK ENDED\n')
    log.see(END)
    root.update()
def missing(MANGA_PATH):
    log.insert(END, 'TASK STARTED\n')
    log.see(END)
    root.update()
    for manga in os.listdir(MANGA_PATH):
        if manga[0]=='!' or manga=='$RECYCLE.BIN':
            continue
        try:
            for part in os.listdir(MANGA_PATH + manga):
                if part == '!ndex.txt' or part == 'desktop.ini' or part == '!con.ico':
                    continue
                log.insert(END, '  >Scanning: ' + part + '\n')
                log.see(END)
                root.update()
                files = os.listdir(MANGA_PATH + manga + '/' + part)
                content = len(files)
                if 'desktop.ini' in files:
                    content -= 1
                if '!ndex.txt' in files:
                    content -= 1
                if '!con.ico' in files:
                    content -= 1
                index = open(MANGA_PATH + manga + '/' + part + '/!ndex.txt', 'r')
                data = index.read()
                if(not data):
                    log.insert(END, '  -!ndex.txt is empty' + '\n')
                    log.see(END)
                    root.update()
                    continue
                variables = {
                'id': data
                }
                index.close()
                query = '''
                query ($id: Int) {
                    Media (id: $id, type: MANGA) {
                        id
                        chapters
                    }
                }
                '''
                log.insert(END, '  -Connecting to server' + '\n')
                log.see(END)
                root.update()
                response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']
                chapters = 0 if not(response['chapters']) else int(response['chapters'])
                if content < chapters:
                    log.insert(END, '  -' + str(chapters - content) + ' chapters MISSING in ' + part + '\n')
                    log.see(END)
                    root.update()
                elif content > chapters:
                    log.insert(END, '  -' + str(content - chapters) + ' chapters EXTRA in ' + part + '\n')
                    log.see(END)
                    root.update()
                else:
                    log.insert(END, '  -All chapters present' + '\n')
                    log.see(END)
                    root.update()
                time.sleep(1)
        except:
            continue
    log.insert(END, 'TASK ENDED\n')
    log.see(END)
    root.update()
bg = '#ffffff'
fg = '#000000'
root = Tk()
root.title('AniFold Samurai')
root.state('zoomed')
root.configure(bg=bg)
parent = Frame(root)
parent.configure(bg=bg)
link = Label(parent, text='How to use?', fg='#0066ff', bg=bg, anchor='e', cursor="hand2")
link.pack(fill="x", pady=(50,0))
link.bind("<Button-1>", lambda e: webbrowser.open_new('https://github.com/Necro-Mancer-94540/AniFold-Samurai'))
Label(parent, text='Path to Manga collection:', font='5', anchor='w', bg=bg, fg=fg).pack(fill="x")
path = Entry(parent, width=100, font='5', bg=bg, fg=fg)
path.pack(fill="x", pady=(0,50))
Button(parent, text='Reset Folders', bg=bg, fg=fg, width=50, font='5', command=lambda:reset(path.get())).pack(pady='1')
Button(parent, text='Generate !ndex.txt', bg=bg, fg=fg, width=50, font='5', command=lambda:generate(path.get())).pack(pady='1')
Button(parent, text='Set Icons', bg=bg, fg=fg, width=50, font='5', command=lambda:setIcon(path.get())).pack(pady='1')
Button(parent, text='Find Missing chapters', bg=bg, fg=fg, width=50, font='5', command=lambda:missing(path.get())).pack(pady='1')
Label(parent, text='Output:', font='5', anchor='w', bg=bg, fg=fg).pack(fill="x", pady=(50,0))
log = Text(parent, width=100, padx=5, pady=5, bg=bg, fg=fg)
log.insert(END, 'Waiting for command...\n')
log.see(END)
root.update()
log.pack(fill="x")
parent.pack()
root.mainloop()
