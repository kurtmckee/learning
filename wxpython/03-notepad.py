import pathlib

import wx


class Notepad(wx.Frame):
    def __init__(self):
        title = 'Notepad in Python'

        super().__init__(None, title=title)

        self.title = title
        self.path = None

        self.create_window()
        self.Show()

    def create_window(self):
        self.SetIcon(wx.Icon('icon.png'))
    
        bar = wx.MenuBar()
        self.SetMenuBar(bar)

        file_menu = wx.Menu()
        open_item = file_menu.Append(-1, '&Open\tCtrl-O', 'Open a file')
        save_item = file_menu.Append(-1, '&Save\tCtrl-S', 'Save to a file')
        file_menu.AppendSeparator()
        quit_item = file_menu.Append(wx.ID_EXIT, '&Quit\tCtrl-Q', 'Quit')

        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, '&About', 'Show the about dialog')

        self.Bind(wx.EVT_MENU, self.open, open_item)
        self.Bind(wx.EVT_MENU, self.save, save_item)
        self.Bind(wx.EVT_MENU, self.quit, quit_item)
        self.Bind(wx.EVT_MENU, self.show_about, about_item)

        bar.Append(file_menu, '&File')
        bar.Append(help_menu, '&Help')

        self.text_box = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.EXPAND)
        self.Bind(wx.EVT_TEXT, self.indicate_modified, self.text_box)

        self.status_bar = self.CreateStatusBar()

    def indicate_modified(self, event):
        if self.path:
            self.SetTitle(f'* {self.path.name} - {self.title}')
        else:
            self.SetTitle(f'* {self.title}')

    def save(self, event):
        if self.path:
            with self.path.open('w') as file:
                file.write(self.text_box.GetValue())
            self.SetTitle(f'{self.path.name} - {self.title}')
            return

        with wx.FileDialog(self, "Save a text file", style=wx.FD_SAVE) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = pathlib.Path(dialog.GetPath())

        if path.exists():
            result = wx.MessageBox('This will overwrite the file!', style=wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING)
            if result == wx.CANCEL:
                return

        self.path = path
        with self.path.open('w') as file:
            file.write(self.text_box.GetValue())
        self.SetTitle(f'{self.path.name} - {self.title}')

    def open(self, event):
        with wx.FileDialog(self, "Open a text file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.path = pathlib.Path(dialog.GetPath())

        with self.path.open('r') as file:
            self.text_box.SetValue(file.read())
        self.SetTitle(f'{self.path.name} - {self.title}')

    def quit(self, event):
        self.Close()

    def show_about(self, event):
        wx.MessageBox('Notepad in Python 1.0')


app = wx.App()
Notepad()
app.MainLoop()
