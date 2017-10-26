import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import sys
import os
import atexit

# app.processEvents()
# import sys
# def trap_exc_during_debug(*args):
# when app raises uncaught exception, print info
#    print(args)

# sys.excepthook = trap_exc_during_debug


def selenium_killer():
    driver.quit()


atexit.register(selenium_killer)

driver = None


# def res_path(rel_path):
    # if hasattr(sys, '_MEIPASS'):
        # return os.path.join(sys._MEIPASS, rel_path)
    # return os.path.join(os.path.abspath("."), rel_path)


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


def on_drv():
    global driver
    driver = webdriver.PhantomJS()


def off_drv():
    global driver
    driver.quit()


def get_vil_list(address):
    global driver
    driver.get(address)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ongoing = soup.select("table.roomPlaying a:nth-of-type(2)")
    ongoing = list(map(lambda log: (log.get_text(strip=True), address + "/bbs/" + log.get('href')), ongoing))
    # ongoing = raw.get_text(strip=True), address + "/bbs/" + raw.get('href')
    return ongoing


def getsoup(address):
    global driver
    # print("Web Driver Loading...")
    # driver = webdriver.PhantomJS()
    print("Get Page...")
    print(driver)
    driver.get(address)
    try:
        driver.find_element_by_id("buttonOpenCommentPagesAll").click()
        print("Wait until loading...")
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
    except NoSuchElementException:
        soup = "WARNING"
    return soup


def working(soup):

    name_soup = re.compile("c_name", re.IGNORECASE)

    # 왜 c_name 도 있고 c_Name 도 있는걸까요?

    name = [i_n.text.strip() for i_n in soup.find_all("span", class_=name_soup)]
    print(name)
    tmln = [i_t.text.strip() for i_t in soup.select("span.reg_date")]
    print(tmln)
    mess = [i_m.text.strip() for i_m in soup.select("div.message")]
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
            dfind = re.sub('(?P<star>[★☆]) ', "\g<star>", dfind)
            dfind = re.sub('\s+', " ", dfind)  # 공백이 두개 이상인 것은 하나로.
            stat_dict[dname] = dfind  # 추천 여부를 딕셔너리에 등록한다.
            # print("딕셔너리를 확인해보세요! \n%s" % stat_dict)
            line.append("%s %s %s" % (dname, dtime, dfind + "\n"))
        # 문자열을 리스트에 등록한다.
        stat = {}  # (이름 : [점추전 행사자들])

    print("여기가 문제입니다.")
    for i in list(stat_dict.keys()):
        print("이게 문제입니다. %s" % i)
        his_name = (stat_dict[i][1:]).strip()  # i 점추천자 his_name 대상
        if his_name not in stat:
            stat[his_name] = []
        stat[his_name].append(i)  # stat[his_name] his_name 을 점추천한 사람들의 리스트
        print(stat[his_name])
    print("요기가 문제입니다.")

    line.append("\n")
    for d in sorted(list(stat.keys()), key=lambda sus: len(stat[sus]), reverse=True):
        line.append("%s %s %d표 (%s)\n" % (d, "/" * len(stat[d]), len(stat[d]), ", ".join(stat[d])))

    return line


def vil_list():
    pass


if __name__ == "__main__":
    on_drv()
    list1 = get_vil_list("http://werewolf.co.kr")
    list3 = get_vil_list("http://werewolf6.cafe24.com")
    vil_list = list1 + list3
    print(vil_list)
    len(vil_list)
