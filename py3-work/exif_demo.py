from PIL import Image
from PIL.ExifTags import TAGS
import time


def get_date(exifinfo):
    if 36867 in exifinfo:  # 36867:DateTimeOriginal
        exifdate = exifinfo[36867]
    elif 36868 in exifinfo:  # 36868:DateTimeDigitized
        exifdate = exifinfo[36868]
    elif 306 in exifinfo:  # 306:DateTime
        exifdate = exifinfo[306]

    print(exifdate)

    # 转为日期格式
    if exifdate.isdigit():
        t_array = time.localtime(int(exifdate)/1000)
    else:
        t_array = time.strptime(exifdate, "%Y:%m:%d %H:%M:%S")

    date = time.strftime("%Y_%m_%d", t_array)
    timestamp = time.strftime("%Y%m%d_%H%M%S", t_array)

    print(date, timestamp)
    return date, timestamp


def get_maker(exifinfo):
    if 271 in exifinfo:  # 271:Make
        maker = exifinfo[271].replace(' ', '_')

    if 272 in exifinfo:  # 272:Model
        model = exifinfo[272].replace(' ', '_')

    print(maker, model)
    return maker, model


def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo != None:
                date, timestamp = get_date(exifinfo)
                maker, model = get_maker(exifinfo)
                ret["date"] = date
                ret["time"] = timestamp
                ret["maker"] = maker
                ret["model"] = model

                for tag, value in exifinfo.items():
                    key = TAGS.get(tag, tag)
                    ret[key] = value
                    print(tag, value)
    except IOError:
        print('IOERROR ' + fname)
    return ret


if __name__ == '__main__':
    filename = '/Users/zcjl/IMG_1192.JPG'
    exif = get_exif_data(filename)
    print(exif)
