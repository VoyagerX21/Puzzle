from django.shortcuts import render
from random import shuffle
import os
import shutil
from PIL import Image

# globals
dic = {0: '', 1: r'media\myapp\main\1.png', 2: r'media\myapp\main\2.png', 3: r'media\myapp\main\3.png', 4: r'media\myapp\main\4.png', 5: r'media\myapp\main\5.png', 6: r'media\myapp\main\6.png', 7: r'media\myapp\main\7.png', 8: r'media\myapp\main\8.png', 9: r'media\myapp\main\9.png'}
global main
global mat
global count

def make():
    mn = [1,2,3,4,5,6,7,8,9]
    shuffle(mn)
    res = []
    global main
    main = mn
    for i in range(1,4):
        res.append(mn[3*(i-1):i*3])

    global mat
    mat = res

def mkcontext(flag=True):
    context = {
        'flag': True,
        'img1': dic[main[0] if main[0] != 9 else 0],
        'img2': dic[main[1] if main[1] != 9 else 0],
        'img3': dic[main[2] if main[2] != 9 else 0],
        'img4': dic[main[3] if main[3] != 9 else 0],
        'img5': dic[main[4] if main[4] != 9 else 0],
        'img6': dic[main[5] if main[5] != 9 else 0],
        'img7': dic[main[6] if main[6] != 9 else 0],
        'img8': dic[main[7] if main[7] != 9 else 0],
        'img9': dic[main[8] if main[8] != 9 else 0]
    }
    return context

def gather(box):
    global main
    res = []
    for i in range(3):
        for j in range(3):
            res.append(box[i][j])
    
    main = res

def availcell(row, column):
    if row==0 and column==0:
        return ['01','10']
    if row==0 and column==1:
        return ['00','02','11']
    if row==0 and column==2:
        return ['01','12']
    if row==1 and column==0:
        return ['00','11','20']
    if row==1 and column==1:
        return ['01','10','12','21']
    if row==1 and column==2:
        return ['02','11','22']
    if row==2 and column==0:
        return ['10','21']
    if row==2 and column==1:
        return ['11','20','22']
    if row==2 and column==2:
        return ['12','21']

def getidx(box, val):
    for i in range(3):
        for j in range(3):
            if box[i][j] == val:
                return i, j

def getInvCount(arr):
    inv_count = 0
    empty_value = 9
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def isSolvable(puzzle) :
    inv_count = getInvCount([j for sub in puzzle for j in sub])
    return (inv_count % 2 == 0)

def index(request):
    make()
    global mat
    while not isSolvable(mat):
        make()
    global count
    count = 0
    return render(request, 'myapp/index.html', mkcontext())

def first(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '00' in avail:
        mat[0][0], mat[i][j] = mat[i][j], mat[0][0]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def second(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '01' in avail:
        mat[0][1], mat[i][j] = mat[i][j], mat[0][1]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def third(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '02' in avail:
        mat[0][2], mat[i][j] = mat[i][j], mat[0][2]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def fourth(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '10' in avail:
        mat[1][0], mat[i][j] = mat[i][j], mat[1][0]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def fifth(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '11' in avail:
        mat[1][1], mat[i][j] = mat[i][j], mat[1][1]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def sixth(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '12' in avail:
        mat[1][2], mat[i][j] = mat[i][j], mat[1][2]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def seventh(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '20' in avail:
        mat[2][0], mat[i][j] = mat[i][j], mat[2][0]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def eighth(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '21' in avail:
        mat[2][1], mat[i][j] = mat[i][j], mat[2][1]
        global count
        count += 1
        gather(mat)

    return render(request, 'myapp/index.html', mkcontext())

def ninth(request):
    global mat
    i, j = getidx(mat, 9)
    avail = availcell(i, j)
    if '22' in avail:
        mat[2][2], mat[i][j] = mat[i][j], mat[2][2]
        global count
        count += 1
        gather(mat)

    c = mkcontext()
    if main == sorted(main):
        c['img9'] = r'media\myapp\images\9.png'
        c['steps'] = count
        c['flag'] = False

    return render(request, 'myapp/index.html', c)

def reset(request):
    return render()

def choices(request):
    return render(request, 'myapp/choice.html')

def clear(path: str):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        os.unlink(filepath)

def crop_image_into_9_pieces(image_path, output_folder):
    img = Image.open(image_path)

    width, height = img.size

    piece_width = width // 3
    piece_height = height // 3

    k = 1
    for i in range(3):
        for j in range(3):
            left = j * piece_width
            upper = i * piece_height
            right = (j + 1) * piece_width
            lower = (i + 1) * piece_height

            piece = img.crop((left, upper, right, lower))

            piece.save(f"{output_folder}/{k}.png")
            k += 1

path = r"media\myapp\present"
path2 = r"media\myapp\main"

def store(id: int):
    if id == 1:
        shutil.copy(r'media\myapp\images\img1.png', r'media\myapp\present\img.png')
    elif id == 2:
        shutil.copy(r'media\myapp\images\img2.png', r'media\myapp\present\img.png')
    elif id == 3:
        shutil.copy(r'media\myapp\images\img3.png', r'media\myapp\present\img.png')
    elif id == 4:
        shutil.copy(r'media\myapp\images\img4.png', r'media\myapp\present\img.png')
    elif id == 5:
        shutil.copy(r'media\myapp\images\img5.png', r'media\myapp\present\img.png')
    elif id == 6:
        shutil.copy(r'media\myapp\images\img6.png', r'media\myapp\present\img.png')
    elif id == 7:
        shutil.copy(r'media\myapp\images\img7.png', r'media\myapp\present\img.png')
    elif id == 8:
        shutil.copy(r'media\myapp\images\img8.png', r'media\myapp\present\img.png')
    elif id == 9:
        shutil.copy(r'media\myapp\images\img9.png', r'media\myapp\present\img.png')
    elif id == 10:
        shutil.copy(r'media\myapp\images\img10.png', r'media\myapp\present\img.png')
    elif id == 11:
        shutil.copy(r'media\myapp\images\img11.png', r'media\myapp\present\img.png')
    elif id == 12:
        shutil.copy(r'media\myapp\images\img12.png', r'media\myapp\present\img.png')
    elif id == 13:
        shutil.copy(r'media\myapp\images\img13.png', r'media\myapp\present\img.png')
    elif id == 14:
        shutil.copy(r'media\myapp\images\img14.png', r'media\myapp\present\img.png')
    elif id == 15:
        shutil.copy(r'media\myapp\images\img15.png', r'media\myapp\present\img.png')
    elif id == 16:
        shutil.copy(r'media\myapp\images\img16.png', r'media\myapp\present\img.png')

def taken(request):
    clear(path)
    # store the image received in the path directory and store the cropped images in the path2 folder
    store(int(request.POST.get('id')))
    crop_image_into_9_pieces(r'media\myapp\present\img.png', path2)
    # After that
    make()
    global mat
    while not isSolvable(mat):
        make()
    global count
    count = 0
    return index(request)
