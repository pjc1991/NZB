import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# app.processEvents()
# import sys

def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)

# sys.excepthook = trap_exc_during_debug


def wolf(raw):
    werewolf = re.search("id=werewolf", raw)
    number = re.search("&no=\d+", raw)
    night = re.search("&viewDay=\d+", raw)
    thirty = re.search("werewolf6.cafe24.com", raw)
    if number is None or werewolf is None:
        return None
    if night is None:
        night = ""
    else:
        night = night.group()
    number = number.group()
    if thirty:
        address = ("http://werewolf6.cafe24.com/bbs/view.php?id=werewolf%s%s" % (number, night))
    else:
        address = ("http://werewolf.co.kr/bbs/view.php?id=werewolf%s%s" % (number, night))
    return address


def textextract(text):
    cleanlist = [i.text() for i in text]
    return cleanlist


def getsoup(address):
    print("Web Driver Loading...")
    driver = webdriver.PhantomJS()
    print("Get Page...")
    print(driver)
    driver.get(address)
    driver.find_element_by_id("buttonOpenCommentPagesAll").click()
    print("Wait until loading...")
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    return soup


def working(soup):

    name_soup = re.compile("c_name", re.IGNORECASE)

    # 왜 c_name 도 있고 c_Name도 있는걸까요?
    # 저는 정말 화가 납니다... 왜 대소문자는 구분하는걸까요...

    name = [i_n.text for i_n in soup.find_all("span", class_=name_soup)]
    print(name)
    tmln = [i_t.text for i_t in soup.select("span.reg_date")]
    print(tmln)
    mess = [i_m.text for i_m in soup.select("div.message")]
    print(mess)

    data = list(zip(name, tmln, mess))
    print(data)
    return data


def nzb(stars, dat, max_s):   # 이름 시간 추천으로 이뤄진 리스트(line)를 리턴한다

    line = []
    stat_dict = {}

    for i in dat:
        dname = str(i[0])
        dtime = str(i[1])
        dstar = str(i[2])

        if stars.findall(dstar) and len(stars.findall(dstar)) <= max_s:

            if dname in stat_dict:
                for k, i_line in enumerate(line):
                    m = re.search(dname, i_line)
                    if m is None:
                        continue
                    elif m.start() == 0 and re.search('[★☆]', i_line):
                        line[k] = re.sub('[★☆]', "", i_line)   # 별을 삭제한다.
                        # print("별 삭제 완료.")    # test

            dfind = " ".join(stars.findall(dstar))
            dfind = re.sub('(?P<star>[★☆]) ', "\g<star>", dfind)   # 공백 제거
            stat_dict[dname] = [dfind]  # 추천 여부를 딕셔너리에 등록한다.
            # print("딕셔너리를 확인해보세요! \n%s" % stat_dict)
            line.append("%s %s %s" % (dname, dtime, dfind + "\n"))
        # 문자열을 리스트에 등록한다.
    return line


def superduper_nzb(raw_address, mode, max_s):   # 단독구동시 사용
    global wstars
    global bstars
    global maxstar
    maxstar = max_s
    if mode:
        wstars = re.compile("[☆]\s?.+\W")
        bstars = re.compile("[★]\s?.+\W")
    else:
        wstars = re.compile("[☆]\s?\w+")
        bstars = re.compile("[★]\s?\w+")
    if wolf(raw_address) is None:
        return "올바른 주소를 입력해주세요."
    else:
        print("바른 주소는...%s" % wolf(raw_address))
        data = working(getsoup(wolf(raw_address)))
        print("데이터를 확인합니다. \n %s" % data)
        zt = "".join(nzb(bstars, data))
        tc = "".join(nzb(wstars, data))
        print(zt)
        print(tc)
        output = "\n---------------점 추천---------------\n\n%s\n---------------투표 추천---------------\n\n%s" % (zt, tc)
    return output


if __name__ == "__main__":
    pass
