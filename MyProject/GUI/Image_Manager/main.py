from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import subprocess
import zipfile


def resize(img, size=550):
    origin = Image.open(img)  # 이미지 열기
    width = origin.size[0]  # 이미지 너비
    height = origin.size[1]  # 이미지 높이
    if height >= width:  # 이미지가 가로/세로 여부에 따라 다른 계산식을 적용
        h_resize = size  # 수정할 이미지 높이
        resized = origin.resize((int(width*(h_resize/height)), h_resize), Image.ANTIALIAS)
    else:
        w_resize = size  # 수정할 이미지 너비
        resized = origin.resize((w_resize, (int(height*(w_resize/width)))), Image.ANTIALIAS)
    # 이미지 크기 조정. 안티앨리어스 적용
    return resized


def extract(file, address):
    filezip = zipfile.ZipFile(file)  # 패키지 함수를 통해 해당 압축파일을 객체화
    filezip_name = filezip.namelist()  # 편의를 위해 압축파일 내 이름 리스트를 객체화
    index = 0
    # 가끔씩 압축파일 내부에 디렉토리가 나누어져 있거나(이 경우 맨 처음에 디렉토리가 오게 됨), 다른 확장자 파일이 존재하는 경우가 있음
    # 이를 거르고 맨 처음 이미지 파일만 뽑아내기 위해 인덱스 객체를 생성하고 다음과 같은 for문을 작성
    for zips in range(len(filezip_name)):
        if os.path.splitext(filezip_name[zips])[1] in ['.jpg', '.png', '.bmp', '.gif']:
            break
        else:
            index += 1
    name = filezip_name[index]  # 인덱스를 이용해 압축파일 안의 첫 번째 이미지 파일의 이름을 객체화
    filezip.extract(name, address)  # 해당 파일의 이름을 이용해 그 파일만 이미지 파일을 읽어올 경로로 압축해제
    filezip.close()  # 객체 삭제
    return name  # 추후 리사이즈 경로 설정을 위해 압축해제한 파일명을 리턴


def refresh_listbox(f_list):
    global file_list  # 파일 전체 리스트를 전역변수로 선언
    global img_list  # 이미지 파일 리스트를 전역변수로 선언. 하지 않으면 새로 수정된 이미지 파일 리스트를 사용할 수 없음
    global name_list  # 이름 리스트를 전역변수로 선언. 하지 않으면 새로 수정된 이름 리스트를 사용할 수 없어 인덱스 에러 발생
    file_list = f_list  # 설정한 경로를 토대로 해당 디렉토리의 파일 리스트 생성
    img_list = []  # 이미지 파일 리스트를 초기화
    for file in file_list:  # 파일 리스트를 기반으로 조건에 맞는 파일만 이미지 파일 리스트에 추가
        if os.path.splitext(file)[1] in ['.zip', '.jpg', '.png', '.bmp', '.gif']:
            img_list.append(file)
    listbox.delete(0, len(name_list) - 1)  # 기존 파일 이름 리스트박스 목록을 전부 제거
    name_list = [os.path.splitext(img)[0] for img in img_list]  # 이미지 파일 리스트에서 확장자를 제거한 이름 리스트 생성
    for name in range(len(name_list)):  # for문을 이용, 이름 리스트를 파일 이름 리스트박스에 추가
        listbox.insert(name, name_list[name])
# 리스트박스를 새로고침하는 함수


def read_setting():
    setting = open('./setting.txt', 'r')  # 같은 경로에 존재하는 세팅 텍스트 파일을 읽어옴
    setting_lines = setting.readlines()  # 텍스트 파일 안에 존재하는 모든 문자열을 라인을 기준으로 나눈 리스트 형식으로 불러옴
    setting_viewer = setting_lines[0].replace('\n', '')  # 첫 번째 열은 파일을 어떤 외부 뷰어로 볼 것인지. 줄바꿈 문자를 제거
    viewer = setting_viewer.split('=')[1]  # 그 후 경로만 따로 추출함
    setting_dir = setting_lines[1].replace('\n', '')  # 두 번째 열은 새 경로를 열 때 시작 위치를 설정. 줄바꿈 문자를 제거
    open_dir = setting_dir.split('=')[1]  # 그 후 경로만 따로 추출함
    return viewer, open_dir  # 이후 경로만 따로 추출한 두 객체를 리턴


def cur_sel_canv(evt):
    try:
        value = int((listbox.index(listbox.curselection())))  # 커서가 선택한 부분의 인덱스를 반환
        img = window.dirname+'/'+img_list[value]  # 이미지 파일 이름 리스트를 이용해 이미지 경로 지정
        extention = os.path.splitext(img_list[value])[1]  # 파일의 확장자에 따라 다른 프로세스를 밟도록 함
        if extention == '.zip':                     # 만약 압축파일일 경우
            extimg = window.dirname + '/' + extract(img, window.dirname)
            # 압축파일의 첫 번째 이미지 파일의 압축을 풀고, 그 파일의 이름에 디렉토리명을 더해 경로를 특정할 수 있도록 함
            resized = resize(extimg)  # 그 경로 객체를 가지고 해당 이미지를 리사이즈
            os.remove(extimg)  # 과정이 끝났으면 압축해제한 이미지를 삭제
        if extention in ['.jpg', '.png', '.bmp', '.gif']:  # 만약 이미지파일일 경우
            resized = resize(img)  # 그냥 바로 리사이즈 함수를 통해 해당 경로 이미지를 열고 리사이즈
        image = ImageTk.PhotoImage(resized)  # ImageTK를 통해 리사이즈한 이미지 객체 생성
        display.delete('IMG')  # 기존에 캔버스에 있던 이미지 삭제
        display.create_image(302, 298, image=image, anchor=CENTER, tag='IMG')  # 캔버스에 새 이미지 부착
        display.image = image  # 캔버스에 부착한 이미지 업데이트. 이렇게 해주지 않으면 제대로 업데이트가 되지 않음
    except:  # 예외처리. 만약 해주지 않을 경우 디렉토리 리스트박스를 클릭할 때 반응해 exception error를 일으킴
        pass
# 리스트박스 항목을 클릭하면 그 항목의 그림을 띄우는 함수. 리스트박스의 바인드문에 사용되어 행동과 연계
# 캔버스를 이용해 이미지 부착


def menu_open():
    global dir_list  # 디렉토리 리스트를 전역변수로 선언
    global file_list  # 파일 전체 리스트를 전역변수로 선언. 혹시 몰라서.
    window.dirnamenew = filedialog.askdirectory(initialdir=open_directory)  # 파일 경로 설정
    if window.dirnamenew:  # 새 경로가 존재할 때만 그 경로가 기존 경로를 대체하도록 함
        window.dirname = window.dirnamenew  # 그러지 않으면 새 경로를 설정하지 않고 창을 닫을 경우 경로가 지정되지 않아 에러 발생
    file_list = os.listdir(window.dirname)
    refresh_listbox(file_list)  # 파일 이름 리스트박스 새로고침 함수 사용
    # print(window.dirname)
    directory_label.config(text=window.dirname)  # 디렉토리 라벨 업데이트
    listbox_dir.delete(1, len(dir_list))  # 디렉토리 리스트박스 내용물 지우기
    dir_list = ['/'+dirs for dirs in file_list if os.path.isdir(window.dirname+'/'+dirs)]
    # 파일 리스트를 기반으로 하위 디렉토리만 디렉토리 리스트에 추가
    for dirs in range(len(dir_list)):
        listbox_dir.insert(dirs+1, dir_list[dirs])  # for문을 이용, 새 디렉토리 리스트를 디렉토리 리스트박스에 추가
# 상단 메뉴의 Open버튼에 사용할 함수


def open_view(*evt):
    # file = 'D:/Honeyview/Honeyview.exe'  # 꿀뷰가 있는 경로를 설정
    if listbox.curselection():  # 커서가 무언가를 선택한 경우에만 작동하도록 함
        value = int((listbox.index(listbox.curselection())))  # 커서가 선택한 부분의 인덱스를 반환
        img = window.dirname+'/'+img_list[value]  # 그 인덱스로 파일의 이름을 얻어내고, 그것으로 해당 파일의 경로를 설정
        # os.system(file+" "+img)  # cmd 커맨드를 이용해 해당 파일을 이미지 뷰어로 열게 함
        subprocess.Popen(file_viewer+" "+img)
    else:
        pass  # 커서가 아무 것도 선택하지 않은 경우에는 아무 것도 띄우지 않도록 함
# 내부의 Open 버튼에 사용할 함수
# 외부 프로그램을 이용해서 이미지를 열도록 함


def change_dir(evt):
    global dir_list  # 디렉토리 리스트를 전역변수로 선언
    global name_list  # 이름 리스트를 전역변수로 선언. 하지 않으면 새로 수정된 이름 리스트를 사용할 수 없어 인덱스 에러 발생
    global img_list  # 이미지 파일 리스트를 전역변수로 선언. 하지 않으면 새로 수정된 이미지 파일 리스트를 사용할 수 없음
    value = int((listbox_dir.index(listbox_dir.curselection())))  # 커서가 선택한 부분의 인덱스를 반환
    if value == 0:  # 만약 인덱스가 0인 경우, 뒤로가기 기능을 구현해야 하므로 현재 경로에서 현재 디렉토리 명을 빼야 함
        folder = window.dirname.split('/')[-1]  # 현재 경로를 '/'를 기준으로 분리해 리스트화. 그 후 맨 마지막의 현재 디렉토리 명을 선택
        window.dirnamenew = window.dirname.replace('/'+folder, '')  # 현재 경로에서 현재 디렉토리 명을 뺀 것을 새 경로로 설정
    else:  # 만약 인덱스가 0이 아닌 경우에는 하위 디렉토리로 들어갈 수 있도록 현재 경로에서 선택한 디렉토리 명을 더해야 함
        folder = dir_list[value-1]  # 디렉토리 리스트에서 선택한 하위 디렉토리의 인덱스와 대응되는 디렉토리 명을 가져옴
        # 뒤로가기 기능이 인덱스 0번이기 때문에 다른 리스트의 인덱스와 맞춰주기 위해 하나씩 당겨줌
        window.dirnamenew = window.dirname + folder  # 현재 경로에 해당 디렉토리 명을 더해 새 경로 설정
    try:
        file_list = os.listdir(window.dirnamenew)  # 설정한 경로를 토대로 해당 디렉토리의 파일 리스트 생성
        window.dirname = window.dirnamenew  # 새 경로를 기존 경로로 설정(뒤의 예외처리를 위해 구분함)
    except FileNotFoundError:  # 만약 유효하지 않은 경로로 들어갈 경우에는 기존 경로에서 움직이지 않도록 예외처리
        file_list = os.listdir(window.dirname)
    refresh_listbox(file_list)  # 파일 이름 리스트박스 새로고침 함수 사용
    # print(window.dirname)
    directory_label.config(text=window.dirname)  # 디렉토리 라벨 업데이트
    listbox_dir.delete(1, len(dir_list))  # 디렉토리 리스트박스 내용물 지우기
    dir_list = ['/'+file for file in file_list if os.path.isdir(window.dirname+'/'+file)]
    # 파일 리스트를 기반으로 하위 디렉토리만 디렉토리 리스트에 추가
    for dirs in range(len(dir_list)):
        listbox_dir.insert(dirs+1, dir_list[dirs])  # for문을 이용, 새 디렉토리 리스트를 디렉토리 리스트박스에 추가
# 디렉토리 리스트박스를 이용해 경로를 변경할 수 있도록 하는 함수


def rename_caution():
    rc_window = Toplevel()
    rc_window.title('Caution')
    rc_window.geometry('220x100+650+350')
    frame_caution = Frame(rc_window)
    frame_caution.pack(ipady=20, expand=1)
    caution_label = Label(frame_caution, text='이미 존재하는 이름입니다!')  # 경고문 라벨
    caution_label.pack(ipady=0, expand=1)
    button_close = Button(frame_caution, text='Close', relief=GROOVE, command=rc_window.withdraw)  # 경고창을 끄는 버튼
    button_close.pack(expand=1)
    rc_window.mainloop()
# 이름 바꾸기 중 이미 존재하는 이름으로 바꾸려 할 때 뜨는 경고창 함수


def rename_save():
    value = int((listbox.index(listbox.curselection())))  # 커서가 선택한 부분의 인덱스를 반환
    origin_name = window.dirname + '/' + img_list[value]  # 이름 변경 전 원래 이름을 전체 디렉토리를 포함해 객체화
    img_ext = os.path.splitext(img_list[value])[1]  # 해당 이미지의 확장자를 따로 객체화
    new_name = window.dirname + '/' + str(entry.get()) + img_ext  # 현 디렉토리와 엔트리에서 입력한 값, 확장자를 합쳐 새 이름 객체 생성
    try:
        os.rename(origin_name, new_name)  # 원래 이름과 새 이름 객체를 이용해 해당 파일의 이름을 변경
        file_list = os.listdir(window.dirname)  # 파일 이름 리스트박스의 새로고침을 위해 해당 디렉토리 내의 파일 리스트를 불러옴
        refresh_listbox(file_list)  # 파일 이름 리스트박스 새로고침 함수 사용
        r_window.withdraw()  # 이름바꾸기 창 닫음
    except FileExistsError:  # 이미 같은 이름이 존재해 에러가 일어났을 때 경고창 함수 호출
        rename_caution()


def rename_window():
    global r_window  # rename_save함수와 함께 사용하기 위해 창의 객체를 전역변수로 선언
    global entry  # 같은 이유로 전역변수 선언
    global name_label  # 같은 이유로 전역변수 선언
    r_window = Toplevel()  # 종속창 객체 생성
    r_window.geometry('600x80+450+350')
    r_window.title('Rename')
    r_window.resizable(0, 0)
    name_frame1 = Frame(r_window, bd=1)  # 원래 이름을 띄울 프레임
    name_frame1.pack(side=TOP, fill=BOTH, expand=1)
    name_frame2 = Frame(r_window, bd=1)  # 새 이름 입력칸을 띄울 프레임
    name_frame2.pack(padx=107, fill=BOTH, expand=1)
    name_frame3 = Frame(r_window, bd=1)  # 버튼을 띄울 프레임
    name_frame3.pack(side=BOTTOM, fill=BOTH, expand=0)
    value = int((listbox.index(listbox.curselection())))  # 커서가 선택한 부분의 인덱스를 반환
    img_name = img_list[value]  # 해당 인덱스의 이미지 파일 이름을 객체화
    extention = os.path.splitext(img_name)[1]  # 해당 인덱스에서 확장자만 따로 추출
    name_label = Label(name_frame1, text=img_name)  # 원래 이름을 띄울 라벨
    name_label.pack(expand=1)
    entry = Entry(name_frame2, width=50)  # 새 이름을 입력할 입력칸(엔트리)
    entry.pack(side=LEFT, expand=1)
    ext_label = Label(name_frame2, text=extention)  # 입력칸 옆에 붙일 확장자 라벨
    ext_label.pack(side=RIGHT, expand=1)
    button_ok = Button(name_frame3, text='Save', relief=GROOVE, command=rename_save)  # 입력한 새 이름으로 이름을 바꾸고 저장하는 버튼
    button_ok.pack(side=LEFT, fill=X, expand=1)
    button_cancel = Button(name_frame3, text='Cancel', relief=GROOVE, command=r_window.withdraw)  # 취소하고 창을 종료하는 버튼
    button_cancel.pack(side=RIGHT, fill=X, expand=1)
    r_window.mainloop()


window = Tk()
window.title('Image Manager')  # 창 제목 설정
window.geometry('1000x600+250+100')  # 창 크기와 위치. 너비x높이+x축+y축
window.resizable(True, False)  # 크기 조절 여부. 가로, 세로

menubar = Menu(window)  # 메뉴바 추가
menu1 = Menu(menubar, tearoff=0)  # 메뉴바에 추가할 메인 메뉴 객체 생성
menu1.add_command(label='Open_Dir', command=menu_open)  # 메인 메뉴에 디렉토리를 여는 버튼 추가
# menu1.add_command(label='Open_Cloud', command=menu_open2)  # 메인 메뉴에 디렉토리를 여는 버튼 추가
menu1.add_separator()  # 메인 메뉴에 구분선 추가
menu1.add_command(label='Exit', command=window.quit)  # 메인 메뉴에 창을 닫는 버튼 추가
menubar.add_cascade(label="Directory", menu=menu1)  # 메인 메뉴를 메뉴바에 부착

frame1 = Frame(window, relief=SOLID, bd=0, background='black')  # 이미지를 띄울 프레임1 생성
frame1.pack(ipadx=0, side=LEFT, fill=BOTH, expand=0)  # 프레임1 부착

frame2 = Frame(window, relief=SOLID, bd=0, background='blue')  # 리스트박스 등을 띄울 프레임2 생성
frame2.pack(ipadx=0, side=RIGHT, fill=BOTH, expand=1)  # 프레임2 부착

frame4 = Frame(frame2, bd=1, background='black')  # 프레임2 안에 디렉토리 리스트박스와 디렉토리 라벨을 띄울 프레임4 생성
frame4.pack(ipady=10, side=TOP, fill=X, expand=0)

frame3 = Frame(frame2, bd=0, background='black')  # 프레임2 안에 파일 이름 리스트박스와 스크롤바를 띄울 프레임3 생성
frame3.pack(side=TOP, fill=BOTH, expand=1)  # 프레임3 부착


file_viewer, open_directory = read_setting()  # 세팅 텍스트 파일을 통해 외부 뷰어 경로 및 새 경로를 열 때 시작지점을 설정


# 1. 최초 디렉토리 및 이미지 파일 목록 작성
# window.dirname = filedialog.askdirectory(initialdir = './')  # 파일 경로 설정
window.dirname = '.'
file_list = os.listdir(window.dirname)  # 설정한 경로를 토대로 해당 디렉토리의 파일 리스트 생성
img_list = []  # 조건에 맞는 파일만 리스트화
for i in file_list:
    if os.path.splitext(i)[1] in ['.zip', '.jpg', '.png', '.bmp', '.gif']:
        img_list.append(i)
# img_list = os.listdir('./image')  # 하위 디렉토리의 이미지 파일 이름을 리스트화
# name_list = [i.split('.')[0] for i in img_list]  # 이미지 파일 이름에서 확장자를 제거
name_list = [os.path.splitext(i)[0] for i in img_list]
dir_list = ['/'+i for i in file_list if os.path.isdir(window.dirname + '/' + i)]

# 2. 메인 이미지 띄우기
# resized = Resize(main_img)  # 리사이즈 함수를 통해 이미지를 열고 리사이즈
# image = ImageTk.PhotoImage(resized)  # 이미지 객체 생성
display = Canvas(frame1, width=600, height=600, background='black', bd=0)  # 프레임2에 부착하는 캔버스 객체 생성
# display.create_image(302, 298, image=image, anchor=CENTER, tag='IMG')  # 캔버스에 이미지 부착
display.pack(expand=1)  # 캔버스 부착

# 3. 파일 이름 스크롤바
scrollbar_x = Scrollbar(frame3, orient=HORIZONTAL)  # 가로축 스크롤바 생성
scrollbar_x.pack(side=BOTTOM, fill=X)  # 가로축 스크롤바 부착. 리스트박스와 연동됨(xscrollcommand)
scrollbar_y = Scrollbar(frame3)  # 세로축 스크롤바 생성
scrollbar_y.pack(side=RIGHT, fill=Y)  # 세로축 스크롤바 부착. 리스트박스와 연동됨(yscrollcommand)

# 4. 파일 이름 리스트박스
listbox = Listbox(frame3,
                  selectmode=BROWSE, activestyle=NONE,
                  xscrollcommand=scrollbar_x.set,
                  yscrollcommand=scrollbar_y.set)  # 리스트박스 생성
scrollbar_x.config(command=listbox.xview)  # 가로축 스크롤바에 드래그 기능 추가
scrollbar_y.config(command=listbox.yview)  # 세로축 스크롤바에 드래그 기능 추가

for i in range(len(name_list)):
    listbox.insert(i, name_list[i])
# 리스트박스에 항목을 추가하는 for문. 확장자를 제거한 이름 리스트를 사용

listbox.bind('<<ListboxSelect>>', cur_sel_canv)  # 리스트박스에 함수 적용
listbox.bind('<Double-Button-1>', open_view)
listbox.pack(side=TOP, fill=BOTH, expand=1)  # 리스트박스 부착

# 5. 파일 선택 버튼
button_rename = Button(frame2, text='Rename', relief=GROOVE, command=rename_window)  # 선택한 파일의 이름을 바꾸는 버튼
button_rename.pack(side=BOTTOM, fill=X)
button_open = Button(frame2, text='Open', relief=GROOVE, command=open_view)  # 선택한 파일을 외부 뷰어로 여는 버튼
button_open.pack(side=BOTTOM, fill=X)

# 6. 디렉토리 라벨
directory_label = Label(frame4, text=window.dirname)  # 현 디렉토리를 보여주는 텍스트 라벨을 생성
directory_label.pack(side=TOP, fill=BOTH, expand=1)  # 라벨 부착

# 7. 디렉토리 스크롤바
scrollbar_x_dir = Scrollbar(frame4, orient=HORIZONTAL)  # 가로축 스크롤바 생성
scrollbar_x_dir.pack(side=BOTTOM, fill=X)  # 가로축 스크롤바 부착. 리스트박스와 연동됨(xscrollcommand)
scrollbar_y_dir = Scrollbar(frame4)  # 세로축 스크롤바 생성
scrollbar_y_dir.pack(side=RIGHT, fill=Y)  # 세로축 스크롤바 부착. 리스트박스와 연동됨(yscrollcommand)

# 7 디렉토리 리스트박스
listbox_dir = Listbox(frame4, height=5,
                      selectmode=BROWSE, activestyle=NONE,
                      xscrollcommand=scrollbar_x_dir.set,
                      yscrollcommand=scrollbar_y_dir.set
                      )
scrollbar_x_dir.config(command=listbox_dir.xview)  # 가로축 스크롤바에 드래그 기능 추가
scrollbar_y_dir.config(command=listbox_dir.yview)  # 세로축 스크롤바에 드래그 기능 추가

listbox_dir.insert(0, '..')  # 뒤로가기 용으로 쓸 첫번째 칸
for i in range(len(dir_list)):  # 디렉토리 리스트박스에 항목 추가
    listbox_dir.insert(i+1, dir_list[i])

listbox_dir.bind('<Double-Button-1>', change_dir)  # 리스트박스에 함수 적용
listbox_dir.pack(side=BOTTOM, fill=BOTH, expand=1)  # 리스트박스 부착

# print(window.dirname)


window.config(menu=menubar)  # 창에 메뉴바 추가
window.mainloop()

