import face_recognition
from wx.lib import statbmp
import os
import traceback
import cv2
import wx
import numpy as np
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

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


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (' ' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        print(plain_text)
        strip_text = plain_text.rstrip()
        str_text = strip_text.decode()
        return str_text

class RootDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)
        panel = wx.Panel(self, -1)

        self.flag_ok = 0
        self.pc = prpcrypt('keys1234keys1234')

        sizer = wx.BoxSizer(wx.VERTICAL)
        RootStaticText = wx.StaticText(panel, -1, 'RootPassword:')
        self.RootText = wx.TextCtrl(panel, value='', size=(230, 30))
        openButton = wx.Button(panel, label='root', pos=(120, 100), size=(110, 30))
        self.StatusText = wx.StaticText(panel, -1, 'Administrator login')
        sizer.Add(RootStaticText, 0)
        sizer.Add(self.RootText, 0)

        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(openButton, 0)
        sizer.Add(self.StatusText, 0)

        # sizer.Add(resignButton, 0)
        # sizer.Add(openButton, 0)
        panel.SetSizer(sizer)
        sizer.SetSizeHints(self)
        panel.Layout()
        panel.SetFocus()

        openButton.Bind(wx.EVT_BUTTON, self.onClickOpen)

    def onClickOpen(self, event):
        try:
            pw0 = open("./Users/Root.txt", 'r').read()
            pw1 = pw0.encode(encoding='utf-8')
            rootPassword = self.pc.decrypt(pw1)
            print(rootPassword)
        except IOError:
            print('The datafile is missing!')
        readpassword = self.RootText.GetValue()
        if readpassword == rootPassword:
            self.flag_ok = 1
            self.StatusText.SetLabel('Accomplished!')
            # RootDialog.Disable()

        else:
            self.StatusText.SetLabel('Wrong password!')
        print('root')

class UserDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.users = []
        self.passwords = []
        self.pc = prpcrypt('keys1234keys1234')

        try:
            data = open("./Users/Users.txt", 'r')
            for each_line in data:
                Line = each_line.replace('\n','')
                line = Line.encode(encoding='utf-8')
                try:
                    decode_line = self.pc.decrypt(line)
                    (user, pw) = decode_line.split(':', 1)
                    self.users.append(user)
                    self.passwords.append(pw)
                    print(user+pw)
                except ValueError:
                    pass
            data.close()
        except IOError:
            print('decode error!')

        userStaticText = wx.StaticText(panel, -1, 'Username:')
        self.UserText = wx.TextCtrl(panel, value='', size=(230, 30))
        pwStaticText = wx.StaticText(panel, -1, 'Password:')
        self.pwText = wx.TextCtrl(panel, value='', size=(230, 30))
        resignButton = wx.Button(panel, label='registered', pos=(0, 115), size=(110, 30))
        openButton = wx.Button(panel, label='sign in', pos=(120, 115), size=(110,30))
        self.StatusText = wx.StaticText(panel, -1, '')
        sizer.Add(userStaticText, 0)
        sizer.Add(self.UserText, 0)
        sizer.Add(pwStaticText, 0)
        sizer.Add(self.pwText, 0)
        sizer.Add(self.StatusText, 0)

        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        boxsizer.Add(resignButton,0)
        boxsizer.Add(openButton, 0)
        panel.SetSizer(boxsizer)
        # sizer.Add(resignButton, 0)
        # sizer.Add(openButton, 0)
        panel.SetSizer(sizer)
        self.SetSize((230,150))
        self.Username = self.UserText.GetValue()
        self.password = self.pwText.GetValue()

        resignButton.Bind(wx.EVT_BUTTON, self.onClickResign)
        openButton.Bind(wx.EVT_BUTTON, self.onClickOpen)

    def onClickResign(self, event):
        self.Username = self.UserText.GetValue()
        self.password = self.pwText.GetValue()
        modal = RootDialog(self)
        modal.ShowModal()
        flag = modal.flag_ok
        modal.Destroy()
        if flag:
            # for User_n in self.users:
            #     if self.Username == User_n:
            #         self.StatusText.SetLabel('User is existed!')
            #         pass

            data = open("./Users/Users.txt", 'a')
            try:
                str = self.Username + ':' + self.password
                bit_data = self.pc.encrypt(str)
                write_data = '\n' + bit_data.decode()
                data.write(write_data)
                data.close()
            except:
                print('write error')
            self.users.append(self.Username)
            self.passwords.append(self.password)
        else:
            print('root error')

        print('resign')

    def onClickOpen(self, event):
        self.Username = self.UserText.GetValue()
        self.password = self.pwText.GetValue()
        try:
            idn = self.users.index(self.Username)
            if self.password == self.passwords[idn]:
                self.StatusText.SetLabel('opened!')
            else:
                self.StatusText.SetLabel('Wrong password!')
        except:
            self.StatusText.SetLabel('User is not exist!')


class ShowCapture(wx.Frame):
    def __init__(self, capture, fps=10):
        wx.Frame.__init__(self, None)
        panel = wx.Panel(self, -1)

        # create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(5, 5)
        self.flag = 0

        self.capture = capture
        ret, frame = self.capture.read()

        self.height, self.width = frame.shape[:2]
        self.orig_height = self.height
        self.orig_width = self.width

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(self.width, self.height, frame)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("initiating...")

        image_names = os.listdir('./known')
        self.known_encodings = []
        self.names = []
        if len(image_names)!=0:
            for image_name in image_names:
                image = face_recognition.load_image_file(os.path.join("./known", image_name))
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_encodings.append(face_encoding)
                self.names.append(os.path.splitext(image_name)[0])
                print(image_name)
        print('Done!')

        # create image display widgets
        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        collectButton = wx.Button(panel, label='collect', pos=(20, 20), size=(125,40))
        recognitionButton = wx.Button(panel, label='open', pos=(100, 80), size=(125,40))
        deleteButton = wx.Button(panel, label='delete', pos=(100, 140), size=(125,40))

        self.nameTest = wx.TextCtrl(panel, value='',pos=(100,200), size=(270,40))#, validator=wx.TE_CENTER)

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
        self.i = 0

        #bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.NextFrame)

        collectButton.Bind(wx.EVT_BUTTON, self.onClickCollect)
        recognitionButton.Bind(wx.EVT_BUTTON, self.onClickRecognite)
        deleteButton.Bind(wx.EVT_BUTTON, self.onClickDelete)

    def onClickCollect(self, event):
        self.str = self.nameTest.GetValue()
        self.flag = 1
        print("collect", self.str)

    def onClickRecognite(self, event):

        modal = UserDialog(self)
        self.timer.Stop()
        modal.ShowModal()
        modal.Destroy()
        self.timer.Start(1000. / self.fps)
        print("recognite")

    def onClickDelete(self, event):
        self.str = self.nameTest.GetValue()
        os.remove('./known/'+ self.str + '.jpg')
        idn = self.names.index(self.str)
        del self.names[idn]
        del self.known_encodings[idn]
        print("delete", self.str)

    def NextFrame(self, event):
        try:
            ret, self.orig_frame = self.capture.read()
            if ret:
                # small_frame = cv2.resize(self.orig_frame, (0, 0), fx=0.25, fy=0.25)
                # face_location = face_recognition.face_locations(small_frame)
                #
                # if len(face_location) > 1:
                #     self.statusbar.SetStatusText('please ensure there is only one person in the picture!')
                # elif len(face_location) == 1:
                #     self.frame = self.orig_frame
                #     if self.flag == 0:
                #         pass
                #         # if len(self.known_encodings)!=0:
                #         #     face_encoding = face_recognition.face_encodings(small_frame, face_location)[0]
                #         #     distance = face_recognition.face_distance(self.known_encodings, face_encoding)
                #         #     idx = np.argmin(distance)
                #         #     if distance[idx] < 0.6:
                #         #         prediction = self.names[idx]+ ' opened'
                #         #     else:
                #         #         prediction = 'Unknown locked'
                #         #
                #         #     for (top, right, bottom, left) in face_location:
                #         #         top *= 4
                #         #         right *= 4
                #         #         bottom *= 4
                #         #         left *= 4
                #         #
                #         #         cv2.rectangle(self.orig_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                #         #     self.statusbar.SetStatusText(prediction)
                #     else:
                #         cv2.imwrite('./known/' + self.str + '.jpg', self.orig_frame)
                #         face_encoding = face_recognition.face_encodings(self.orig_frame)[0]
                #         self.known_encodings.append(face_encoding)
                #         self.names.append(os.path.splitext(self.str)[0])
                #         self.flag = 0
                # else:
                #     self.statusbar.SetStatusText('no face detected!')

                frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2RGB)
                self.bmp = wx.Bitmap.FromBuffer(self.width, self.height, frame)
                self.ImgControl.SetBitmap(self.bmp)

            else:
                print("camera error")
        except:
            traceback.print_exc()
            print("error")


capture = cv2.VideoCapture(0)

app = wx.App()
frame = ShowCapture(capture)
frame.Show()
app.MainLoop()