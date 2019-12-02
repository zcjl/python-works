# coding:utf-8

from PIL import Image
import time
import os
import shutil
import getopt
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def get_datetime(exifinfo):
    if 36867 in exifinfo:  # 36867:DateTimeOriginal
        dateinfo = exifinfo[36867]
    elif 36868 in exifinfo:  # 36868:DateTimeDigitized
        dateinfo = exifinfo[36868]
    elif 306 in exifinfo:  # 306:DateTime
        dateinfo = exifinfo[306]

    if dateinfo.isdigit():
        t_array = time.localtime(int(dateinfo)/1000)
    else:
        t_array = time.strptime(dateinfo, "%Y:%m:%d %H:%M:%S")

    date = time.strftime("%Y_%m_%d", t_array)
    timestamp = time.strftime("%Y%m%d_%H%M%S", t_array)

    return date, timestamp


def get_maker(exifinfo):
    if 271 in exifinfo:  # 271:Make
        maker = trim(exifinfo[271])

    if 272 in exifinfo:  # 272:Model
        model = trim(exifinfo[272])

    return maker, model


def trim(a):
    return re.sub("[^a-zA-Z0-9_]", "", a.strip().replace(' ', '_').replace('/', '_').replace(',', '_'))


def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    exifdata = {}
    try:
        img = Image.open(fname)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo:
                date, timestamp = get_datetime(exifinfo)
                maker, model = get_maker(exifinfo)
                exifdata["date"] = date
                exifdata["time"] = timestamp
                exifdata["maker"] = maker
                exifdata["model"] = model
    except:
        exifdata = exifdata
    return exifdata


def search_photos():
    succ = []
    fail = []
    todo = {}
    for dir_path, dir_names, file_names in os.walk(SRC):
        for file_name in file_names:
            oldpath = os.path.join(dir_path, file_name)
            exifdata = get_exif_data(oldpath)
            if exifdata:
                succ.append(oldpath)
                exifdata['oldpath'] = oldpath
                items = todo.get(exifdata['time'])
                if not items:
                    items = []
                    todo[exifdata['time']] = items
                items.append(exifdata)
            else:
                fail.append(oldpath)
    return succ, fail, todo


def copy_photos(todo):
    log = []
    for key, items in todo.items():
        for index, exifdata in enumerate(items):
            maker = exifdata['maker']
            model = exifdata['model']
            date = exifdata['date']
            timestamp = exifdata['time']
            oldpath = exifdata['oldpath']
            if index > 0:
                timestamp = timestamp + "_" + str(index)
            newpath = '%s/%s/%s_%s_IMG_%s%s' % (DEST, date, maker, model, timestamp, get_file_ext(oldpath))
            log.append('%s %s' % (oldpath, newpath))
            # do_copy(oldpath, newpath)
            # print(oldpath, newpath)
    return log


def get_file_ext(filename):
    filepath, fullname = os.path.split(filename)
    fname, fext = os.path.splitext(fullname)
    return fext


def do_copy(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


def write_log_file(succ, fail, log):
    print(succ, fail, log)
    succ_file = open('succ.txt', 'w')
    fail_file = open('fail.txt', 'w')
    log_file = open('todo_list.txt', 'w')

    succ_file.write('\n'.join(succ))
    fail_file.write('\n'.join(fail))
    log_file.write('\n'.join(log))


def main():
    succ, fail, todo = search_photos()
    log = copy_photos(todo)
    write_log_file(succ, fail, log)


def init(argv):
    global SRC, DEST

    SRC = '/volume1/photo/iPhone8p'
    DEST = '/volume1/photo/new_ip8p'

    try:
        opts, args = getopt.getopt(argv, "hs:d:", ["help", "src=", "dest="])
    except getopt.GetoptError:
        print("Error: %s -s <src> -d <dest>" % sys.argv[0])
        print("   or: %s --src=<src> --dest=<dest>" % sys.argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("%s -s <src> -u <dest>" % sys.argv[0])
            print("or: %s --src=<src> --dest=<dest>" % sys.argv[0])
            sys.exit()
        elif opt in ("-s", "--src"):
            SRC = arg
        elif opt in ("-d", "--dest"):
            DEST = arg

    print(SRC, DEST)


if __name__ == "__main__":
    init(sys.argv[1:])
    main()
