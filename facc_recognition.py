import face_recognition
from wx.lib import statbmp
import os
import traceback
import cv2
import wx
import numpy as np
import time

# #open camera
# video_capture = cv2.VideoCapture(0)
#
# #load image which is alreading known and encoding
# load_image1 = face_recognition.load_image_file("./known_people/yn.jpg")
# image_encoding1 = face_recognition.face_encodings(load_image1)[0]
# load_image2 = face_recognition.load_image_file("./known_people/qy.jpg")
# image_encoding2 = face_recognition.face_encodings(load_image2)[1]
#
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True
#
# while True:
# #get frame
#     ret, frame = video_capture.read()

class ShowCapture(wx.Frame):
    def __init__(self, capture, fps=15):
        wx.Frame.__init__(self, None)
        panel = wx.Panel(self, -1)

        # create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(5, 5)
        self.flag = 0

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        self.orig_height = height
        self.orig_width = width

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        #creat statictest display

        # create image display widgets
        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        collectButton = wx.Button(panel, label='collect', pos=(20, 20), size=(125,40))
        recognitionButton = wx.Button(panel, label='recognite', pos=(100, 80), size=(125,40))
        deleteButton = wx.Button(panel, label='delete', pos=(100, 140), size=(125,40))

        self.nameTest = wx.TextCtrl(panel, value='',pos=(100,200), size=(200,40))#, validator=wx.TE_CENTER)

        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(collectButton, 0)
        box_sizer.Add(recognitionButton, 0)
        box_sizer.Add(deleteButton, 0)
        box_sizer.Add(self.nameTest,0)
        sizer.Add(box_sizer, (0, 0), wx.DefaultSpan, wx.ALIGN_RIGHT)

        sizer.Add(self.ImgControl, (1, 0), (0, 0), wx.EXPAND | wx.CENTER | wx.LEFT | wx.BOTTOM, 5)

        # set the sizer and tell the Frame about the best size
        panel.SetSizer(sizer)
        sizer.SetSizeHints(self)
        panel.Layout()
        panel.SetFocus()

        # start a timer that's handler grabs a new frame and updates the image widgets
        self.timer = wx.Timer(self)
        self.fps = fps
        self.timer.Start(1000. / self.fps)

        #bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.NextFrame)

        collectButton.Bind(wx.EVT_BUTTON, self.onClickCollect)
        recognitionButton.Bind(wx.EVT_BUTTON, self.onClickRecognite)
        deleteButton.Bind(wx.EVT_BUTTON, self.onClickDelete)

    def onClickCollect(self, event):
        str = self.nameTest.GetValue()
        self.flag = 1
        print("collect", str)

    def onClickRecognite(self, event):
        self.flag = 0
        print("recognite")

    def onClickDelete(self, event):
        print("delete")

    def NextFrame(self, event):
        try:
            time.sleep(0.03)
            ret, self.orig_frame = self.capture.read()
            if ret:
                # if self.flag:
                #     small_frame = cv2.resize(self.orig_frame, (0, 0), fx=0.25, fy=0.25)
                #     face_location = face_recognition.face_locations(small_frame)
                #
                #     if len(face_location) > 1:
                #         cv2.putText(frame, 'please ensure there is only one person in the picture!', (0, 20),
                #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
                #     elif len(face_location) == 1:
                #         ok = True
                #         cv2.putText(frame, 'please type "c" to take the picture!', (0, 20),
                #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
                #     else:
                #         cv2.putText(frame, 'no face detected!', (0, 20),
                #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
                #     cv2.imshow('', frame)
                #     k = cv2.waitKey(1)
                #     if k & 0xFF == ord('q'):
                #         print('quit!')
                #         break
                #     elif k & 0xFF == ord('c'):
                #         print('collect ' + name + "'s data successfully!")
                #         cv2.imwrite('./known/' + name + '.jpg', frame)
                #         break



                frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2RGB)

                self.bmp.CopyFromBuffer(frame)
                self.ImgControl.SetBitmap(self.bmp)

            else:
                print("camera error")
        except:
            traceback.print_exc()
            print("error")










#         self.timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.update, self.timer)
#
#         collectButton = wx.ToggleButton(panel, label='collect', pos=(750, 20))
#         recognitionButton = wx.ToggleButton(panel, label='recognite', pos=(750, 60))
#         deleteButton = wx.ToggleButton(panel, label='delete', pos=(750, 100))
#
#         # self.cpnl = wx.Panel(pnl, pos=(150, 20), size=(110, 110))
#         # self.cpnl.SetBackgroundColour(self.col)
#
#         collect.Bind(wx.EVT_TOGGLEBUTTON, self.ClickCollect)
#         recognition.Bind(wx.EVT_TOGGLEBUTTON, self.ClickRecognite)
#         delete.Bind(wx.EVT_TOGGLEBUTTON, self.ClickDelete)
#
#         self.cap = cv2.VideoCapture(0)
#         ret, source = self.cap.read()
#         img = cv2.cvtColor(np.uint8(source), cv2.COLOR_BGR2RGB)
#         self.h, self.w = img.shape[0:2]
#         # wxbmp = wx.BitmapFromBuffer(self.w, self.h, img)
#         # wx.image = wx.StaticBitmap(parent=self, bitmap=wxbmp)
#         self.timer.Start(50)
#
#         self.SetSize((1000, 450))
#         self.SetTitle('face_recognition')
#         self.Centre()
#         self.Show(True)
#
#     def ClickCollect(self,e):
#         print("cllection")
#
#     def ClickRecognite(self,e):
#         print("recognition")
#
#     def ClickDelete(self,e):
#         print("delete")
#
#     def update(self,e):
#         ret, source = self.cap.read()
#         img = cv2.cvtColor(np.uint8(source), cv2.COLOR_BGR2RGB)
#         wxbmp = wx.Bitmap.FromBuffer(self.w, self.h, img)
#         wx.StaticBitmap(parent=self, bitmap=wxbmp)
#
# def main():
#     app = wx.App()
#     MyFrame(None)
#     app.MainLoop()
#
# if __name__ == "__main__":
#     main()

    # SetStatusText()
    # 在状态栏上显示的文字
capture = cv2.VideoCapture(0)

app = wx.App()
frame = ShowCapture(capture)
frame.Show()
app.MainLoop()