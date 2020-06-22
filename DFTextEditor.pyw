from tkinter import *
from tkinter import filedialog
import json




class MenuBar:

    def __init__(self, parent):
        font_specs = ('Segoe UI', 12)

        menubar = Menu(parent.app, font=font_specs)
        parent.app.config(menu=menubar)

        file_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label='New File', command=parent.new_file, accelerator='Ctrl+N')
        file_dropdown.add_command(label='Open File', command=parent.open_file, accelerator='Ctrl+O')
        file_dropdown.add_command(label='Save', command=parent.save, accelerator='Ctrl+S')
        file_dropdown.add_command(label='Save As', command=parent.save_as, accelerator='Ctrl+Shift+S')
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit', command=parent.app.destroy)

        options_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        options_dropdown.add_command(label='Preferences', command=parent.optionsmenu.open_preferences, accelerator='Ctrl+,')

        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='Options', menu=options_dropdown)




class StatusBar:

    def __init__(self, parent):

        font_specs = ('Segoe UI', 10)

        self.root = parent
        
        self.status = StringVar()
        self.status.set('DF Text Editor')

        label = Label(parent.textarea, textvariable=self.status, fg='black', bg='lightgrey', anchor='sw', font=font_specs)
        label.pack(side=BOTTOM, fill=BOTH)
    
    def update_status(self, *args):
        if isinstance(args[0], str):
            action = args[0]
            self.status.set('Unknown status')
            if action == 'save':
                self.status.set('File saved successfully')
            if action == 'save-error':
                self.status.set('Error occured while attempting to save file')
            if action == 'open':
                self.status.set('File opened successfully')
            if action == 'open-error':
                self.status.set('Error occured while attempting to open file')
            if action == 'new_file':
                self.status.set('New file opened successfully')
        else:
            self.status.set('DF Text Editor')
        self.update_save_indicator()
    
    def when_file_update(self, *args):
        self.update_status(args)
        self.root.filesaved = False
    
    def update_save_indicator(self):
        filename = self.root.filename
        filesaved = self.root.filesaved

        set_title = ''
        if filename:
            set_title += filename
        else:
            set_title += 'Untitled'
        if not filesaved:
            set_title += '*'

        self.root.set_window_title(set_title)




class OptionsMenu:

    def __init__(self, parent):

        font_specs = ('Segoe UI', 12)
    
    def open_preferences(self, *args):
        print('hello there')




class DFTextEditor:

    def __init__(self, app):
        app.title('Untitled - DF Text Editor')
        app.geometry('1000x600')
        app.iconbitmap('DFLogo.ico')

        font_specs = ('Segoe UI', 14)

        self.app = app
        self.filename = None
        self.filesaved = True

        self.textarea = Text(app, font=font_specs)
        self.scrollbar = Scrollbar(app, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scrollbar.set)
        self.textarea.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.optionsmenu = OptionsMenu(self)
        self.menubar = MenuBar(self)
        self.statusbar = StatusBar(self)

        self.bind_shortcuts()
    
    def set_window_title(self, name=None):
        if name:
            self.app.title(name + ' - DF Text Editor')
        else:
            self.app.title('Untitled - DF Text Editor')

    def new_file(self, *args):
        self.textarea.delete(1.0, END)
        self.filename = None
        self.set_window_title()
        self.statusbar.update_status('new_file')

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(defaultextension='.dflib', filetypes=[('All Files', '*.*'), ('Text Files', '*.txt'), ('DF Code Projects', '*.dflib'), ('DF Templates', '*.dfcode')])
        if self.filename:
            self.textarea.delete(1.0, END)
            try:
                with open(self.filename, 'r') as f:
                    self.textarea.insert(1.0, f.read())
                self.statusbar.update_status('open')
            except:
                self.statusbar.update_status('open-error')
            self.set_window_title(self.filename)

    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                self.filesaved = True
                self.statusbar.update_status('save')
            except:
                self.statusbar.update_status('save-error')
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(initialfile='Untitled.dflib', defaultextension='.dflib', filetypes=[('All Files', '*.*'), ('Text Files', '*.txt'), ('DF Code Projects', '*.dflib'), ('DF Templates', '*.dfcode')])
            textarea_content = self.textarea.get(1.0, END)
            with open(new_file, 'w') as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.filesaved = True
            self.statusbar.update_status('save')
        except:
            self.statusbar.update_status('save-error')
    
    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.when_file_update)
        self.textarea.bind('<Control-,>', self.optionsmenu.open_preferences)




if __name__ == '__main__':
    app = Tk()
    df = DFTextEditor(app)
    app.mainloop()
