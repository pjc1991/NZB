from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("http://werewolf.co.kr")
html = driver.page_source
print(html)

x = 1

print("hello, world!")

def test():
    global x
    x += 1
    print(x)

for t in range(100):
    test()

