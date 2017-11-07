import wx
import time

#
# class MyForm(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, wx.ID_ANY, "Timer Tutorial 1",
#                           size=(500, 500))
#
#         # Add a panel so it looks the correct on all platforms
#         panel = wx.Panel(self, wx.ID_ANY)
#
#         self.timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.update, self.timer)
#
#         self.toggleBtn = wx.Button(panel, wx.ID_ANY, "Start")
#         self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)
#
#     def onToggle(self, event):
#         btnLabel = self.toggleBtn.GetLabel()
#         if btnLabel == "Start":
#             print("starting timer...")
#             self.timer.Start(1000)
#             self.toggleBtn.SetLabel("Stop")
#         else:
#             print("timer stopped!")
#             self.timer.Stop()
#             self.toggleBtn.SetLabel("Start")
#
#     def update(self, event):
#         print("\nupdated: ",time.ctime())
#
#
#
#
# # Run the program
# if __name__ == "__main__":
#     app = wx.PySimpleApp()
#     frame = MyForm().Show()
#     app.MainLoop()


import wx

class StaticTextExampleFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, \
         "Static text example", size =(800, 600))
        panel = wx.Panel(self, -1)

        #基本静态的文本
        wx.StaticText(panel, wx.ID_ANY, "这是个基本的静态文本。", (100, 10))

        #为文本指定前景色和背景色
        text = wx.StaticText(panel, wx.ID_ANY, "指定文本前景和背景色", (100, 30))
        text.SetForegroundColour("White")
        text.SetBackgroundColour("Black")

        #指定居中对齐
        text = wx.StaticText(panel, wx.ID_ANY, "居中对齐", (100,50), (160, -1),\
                                wx.ALIGN_CENTER)
        text.SetForegroundColour("White")
        text.SetBackgroundColour("Black")

        #指定右对齐
        text =wx.StaticText(panel, wx.ID_ANY, "居右对齐", (100,70),(160, -1),\
                                wx.ALIGN_RIGHT)

        #指定字体的静态文本的font
        text = wx.StaticText(panel, wx.ID_ANY,"设置文本font", (20,100))
        font=wx.Font(18,wx.DECORATIVE,wx.ITALIC,wx.NORMAL)
        text.SetFont(font)

        #设置多行文本
        multiStr ="现在你看到\n的是多行\n文本"
        wx.StaticText(panel, wx.ID_ANY, multiStr, (20, 150))



def main():
    app = wx.PySimpleApp()
    frame = StaticTextExampleFrame()
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()