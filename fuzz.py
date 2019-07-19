import requests
from bs4 import BeautifulSoup
from termcolor import colored
from time import time

def how_many_forms(url):
    print("Fetching Forms List Please Wait..")
    links = links_to_page(url)
    number_of_forms = {}
    for i in links:
        r = requests.get(i)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find_all("form")
        number_of_forms.update({i: len(form)})
    return number_of_forms

def links_to_page(url):
    set_for_links = set()
    try:
            if ("https://" not in url and "http://" not in url):
                r = requests.get("http://{}".format(url))
                first_url = "http://{}".format(url)
            else:
                first_url = url
                r = requests.get(url)
    except Exception as e:
        print(e)
        pass
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a")

    if ("https://" in url or "http://" in url):
        url = url.split("//")[1]
        if ("www." in url):
            url = url.split("www.")[1]
        if ("/" in url):
            url = url.split("/")[0]

    for i in links:
        actual_url = i.get("href")
        url_in_tag = str(i.get("href"))
        if ("https://" in url_in_tag or "http://" in url_in_tag):
            url_in_tag = url_in_tag.split("//")[1]
        if ("www." in url_in_tag):
            url_in_tag = url_in_tag.split("www.")[1]
        if ("/" in url_in_tag):
            url_in_tag = url_in_tag.split("/")[0]
        if (url in url_in_tag):
            set_for_links.add(actual_url)

        try:
            if (url_in_tag[0] == "."):
                actual_url = first_url + url_in_tag[1:]
                set_for_links.add(actual_url)
            elif(url_in_tag[0] != "/" and url[-1] != "/"):
                actual_url = first_url + "/" + url_in_tag
                set_for_links.add(actual_url)
            elif(url_in_tag[0] == "/" and url[-1] == "/"):
                actual_url = first_url + url_in_tag[1:]
                set_for_links.add(actual_url)
            else:
                actual_url = first_url + url_in_tag
                set_for_links.add(actual_url)
        except:
            pass

    return set_for_links

def get_inputs(url):

    try:
            if ("https://" not in url and "http://" not in url):
                r = requests.get("http://{}".format(url))
            else:
                r = requests.get(url)
    except Exception as e:
        print(e)
        pass

    soup = BeautifulSoup(r.content, "html.parser")
    list_of_inputs = []
    for i in soup.find_all("input"):
        list_of_inputs.append(i)

    return list_of_inputs
def find_xss(url):
    xss_flag = False
    try:
        if ("https://" not in url and "http://" not in url):
            url = "http://{}".format(url)
    except Exception as e:
        print(e)
        pass

    print(colored("Request Sent to Site {}".format(url), "green"))

    inputs = get_inputs(url) #Get input boxes
    if(len(inputs) == 0):
        return -1
    print(colored("Finding input box in the page..", "green"))
    start = time()
    for pyld in payload:
        try:
            for i in inputs:
                name = str(i.get("name"))
                r = requests.get(url + "?" + name + "=" + pyld)
                if(pyld in str(r.content,"utf-8")):
                    xss_flag = True

                    print()
                    print(colored("#FOUND -> Payload:{}".format(pyld),"green"))
                    end = time()
                    ctime = end - start
                    print(colored("Vulnerable URL -> {}".format(url),"red"))
                    print(colored("Vulnerable Input Box-> {}".format(i),"red"))
                    if(xss_flag):
                        print()
                        print(colored("Time:{} Seconds".format(ctime), "white"))
                        return 1
                else:
                    print(colored("#NOT FOUND -> Payload:{}".format(pyld),"red"))
        except Exception as e:
            print(e)
            pass


def payloads(file):
    with open(file,"rb") as f:
        payloads = f.read().splitlines()
    return payloads


if __name__ == '__main__':
    intro = '''
        #################################################################
        #                                                               #
        #                       XSS Scraper                             #
        #               Developed by Chaitanya Dande                    #
        #                                                               #
        #################################################################
    '''
    print(colored(intro, "green"))
    print()

    choices = '''
    1)XSS URL Scan
    2)Total Scan
    3)Fetch all Links
    4)Fetch Form Count
    5)Fetch Input Box
    '''
    try:
        print(choices)
        choice = input("Make a Choice -->")

        if (choice == "1"):
            url = input("Please input the url -> ")
            file = input("Please input Payloads file name -> ")
            payload = payloads(file)
            result = find_xss(url)
            if (result == -1):
                print("No input box found to attack.")
            else:
                print(colored(40 * "-", "red"))
        elif (choice == "2"):
            url = input("Please input the url -> ")
            file = input("Payloads' file name -> ")
            payload = payloads(file)
            links = links_to_page(url)
            for link in links:
                try:
                    result = find_xss(link)
                    if(result == -1):
                        print("No input box found to attack.")
                        if (test == "0"):
                            exit(0)
                        print(colored(40 * "-", "red"))
                    elif(result == 1):
                        test = input("Do you want to test other links in the page:(1->Continue or 0->Stop) (Default:1)") or "1"
                        if(test == "0"):
                            exit(0)
                        print(colored(40 * "-", "red"))
                    else:
                        print(colored(40 * "-", "red"))
                except Exception as e:
                    print(e)
                    pass
        elif (choice == "3"):
            url = input("URL Please -> ")
            links = links_to_page(url)
            for i in links: 
                print(i)
        elif (choice == "4"):
            url = input("URL Please -> ")
            forms = how_many_forms(url)
            for i, j in forms.items():
                print(i, "->", j, "form(s)")
        elif (choice == "5"):
            url = input("URL Please -> ")
            inputs = get_inputs(url)
            for i in inputs:
                print(i)
        else:
            print("Bad Choice,Try Your Luck Next time")
            exit(1)
    except KeyboardInterrupt:
        print("Bye Bye..Exiting")
