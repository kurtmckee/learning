import wx


class Converter(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer()
        panel.SetSizer(sizer)

        self.input_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.input_box.Bind(wx.EVT_TEXT_ENTER, self.calculate)
        sizer.Add(self.input_box)

        button = wx.Button(panel, label='F --> C')
        button.Bind(wx.EVT_BUTTON, self.calculate)
        sizer.Add(button)

        self.output_label = wx.StaticText(panel, -1, label='--- C')
        sizer.Add(self.output_label)

    def calculate(self, event):
        try:
            f = int(self.input_box.GetValue())
        except ValueError:
            self.output_label.SetLabel('Invalid')
            return
        
        c = (f - 32) * 5 / 9
        if c < -273.15:
            self.output_label.SetLabel('Impossibly cold!')
        else:
            self.output_label.SetLabel(f'{c:.1f} C')


app = wx.App()

frame = Converter(None, title='Temperature Converter')
frame.Show()

app.MainLoop()
