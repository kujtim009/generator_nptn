import requests
import concurrent.futures
import re
# [rest of code]

mainUrl = "https://www.neptun-ks.com/"
deepLinksList = []
useProxy = True


def proxies():
    return {
        "http://": "192.187.111.82:17086",
        "https://": "192.187.111.82:17086"
    }


def getCategories(mainUrl):
    req = (requests.get(
        mainUrl, proxies=proxies()) if useProxy else requests.get(mainUrl))

    reg = re.findall(
        r"<li id=\"\"><a href=\"/pocetna/categories(.*?)\" target=\"_self\">", req.text)
    return list("{}pocetna/categories{}".format(mainUrl, n) for n in reg)


def appendToFile(content):
    strContent = " "
    print("Content Saving...")
    with open("data.txt", "a") as f:
        f.write(strContent.join(content))
        print("Content Saved")


def getPages(link):
    for pageNum in range(1, 100):
        global deepLinksList
        myList = getDipLinks("{}?page={}".format(link, pageNum))
        print(len(deepLinksList), "{}?page={}".format(link, pageNum))
        deepLinksList.extend(myList)
        if len(myList) <= 99:
            appendToFile(myList)
            myList.clear()
            break


def getDipLinks(link):
    req = requests.get("{}&items=100".format(
        link), proxies=proxies) if useProxy else requests.get("{}&items=100".format(link))
    print("Deep Links scraped")
    reg = re.findall(
        r'Url\\"\:\\"(.*?)\".*?Url\\"\:\\"(.*?)\"', req.text, flags=re.I | re.DOTALL)
    return list("{}pocetna/categories/{}{}".format(mainUrl, n[0].replace("\\", "/"), n[1].replace("\\", "")) for n in reg)


if __name__ == "__main__":
    print("starting")
    categorit = getCategories(mainUrl)
    print(len(categorit))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(getPages, [link for link in categorit])
