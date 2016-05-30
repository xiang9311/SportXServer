__author__ = '祥祥'

citys = ['beijing']


class ClubInMeituan():
    def __init__(self, name='', area='', location='', cover='', phone='', latitude=0.0, longitude=0.0, meituan_category='', club_intro='', images=[], price=0, discount=0.0):
        self.name = name
        self.area = area
        self.location = location
        self.cover = cover
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude
        self.meituan_category = meituan_category
        self.club_intro = club_intro
        self.images = images
        self.price = price
        self.discount = discount

    def same_as(self, club):
        return self.location == club.location\
               and self.name == club.name\
               and self.area == club.area\
               and self.phone == club.phone\
               and self.latitude == club.latitude\
               and self.longitude == club.longitude

    def to_string(self):
        result = []
        result.append(self.name)
        result.append(self.area)
        result.append(self.location)
        result.append(self.cover)
        result.append(self.phone)
        result.append(self.latitude)
        result.append(self.longitude)
        result.append(self.meituan_category)
        result.append(self.club_intro)
        return result


"""
读取文件 获取酒吧列表  目前默认只使用北京的
"""
def read_club_from_file():
    clubs = []
    # for city in citys:
    # file_name = city + '_detail/clubdetail.txt'
    file_name = r'D:\clubdetail.txt'
    file = open(file_name, 'r', 1, 'utf-8')
    lines = file.readlines()
    r_size = range(1, len(lines))
    for index in r_size:
        club_string = lines[index]
        club = get_club_from_string(club_string)
        clubs.append(club)
    file.close()
    return clubs



def get_club_from_string(clubitem):
    club = ClubInMeituan()
    club_split = eval(clubitem)
    club.name = club_split[0]
    club.area = club_split[1]
    club.location = club_split[2]
    club.cover = club_split[3]
    club.images = club_split[4]
    club.phone = club_split[5]
    club.latitude = club_split[6]
    club.longitude = club_split[7]
    club.meituan_category = club_split[8]
    club.club_intro = club_split[9]
    club.price = int(club_split[10][1:])
    club.discount = float(club_split[11][:-1])
    return club