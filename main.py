from random import randint
from time import sleep
from bs4 import BeautifulSoup
import requests
import json
import re
import config

client = requests.Session()

# LInkedIn URL's and other variables
HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
MY_NETWORK = 'https://www.linkedin.com/mynetwork/'
INVITES = 'https://www.linkedin.com/voyager/api/relationships/peopleYouMayKnow?count=10&includeInsights=true&start=3&usageContext=d_flagship3_people'
INVITE_POST = 'https://www.linkedin.com/voyager/api/growth/normInvitations'
JOBS_URL = 'https://www.linkedin.com/jobs/'
MAIN_NETWORK = 'https://www.linkedin.com/feed/'
FOLLOW_NETWORK = 'https://www.linkedin.com/feed/follow/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36','accept-encoding': 'gzip, deflate br','x-li-lang': 'en_US','accept-language': 'en-US,en;q=0.8',
'pragma':'no-cache'}


#Sweet logo is sweet.
def zeerg():
    print("""
    
 /$$$$$$$$                                        
|_____ $$                                         
     /$$/   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
    /$$/   /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
   /$$/   | $$$$$$$$| $$$$$$$$| $$  \__/| $$  \ $$
  /$$/    | $$_____/| $$_____/| $$      | $$  | $$
 /$$$$$$$$|  $$$$$$$|  $$$$$$$| $$      |  $$$$$$$
|________/ \_______/ \_______/|__/       \____  $$
                                         /$$  \ $$
                                        |  $$$$$$/
                                         \______/ 

    
    https://github.com/Zeerg
    A LinkedIn Invite bot for the lazy.
    Add your credentials to config.py and go.
    """)

#Sleep function
def rando_sleep(sleep_min, sleep_max):
    sleep(randint(sleep_min, sleep_max))

#Connect with requests and pull csrf token.
def connect(username, password):
    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, "html.parser")
    global csrf
    csrf = soup.find(id="loginCsrfParam-login")['value']
    login_information = {
        'session_key': username,
        'session_password': password,
        'loginCsrfParam': csrf,
    }
    client.post(LOGIN_URL, headers=headers, data=login_information)


def open_main():
    # Load the MyNetwork Page for Fun or something.
    print("Opening Main Page")
    linkedin_main = client.get(MAIN_NETWORK, headers=headers)


def open_my_network():
    # Load the MyNetwork Page for Fun or something.
    print("Opening My Network Page")
    linkedin_network = client.get(MY_NETWORK, headers=headers)


def open_jobs_feed():
    # Load the Jobs Page for Fun or something.
    print("Opening Jobs Page")
    linkedin_jobs = client.get(JOBS_URL, headers=headers)


def increase_network():
    success = 0
    failed = 0
    # Load the MyNetwork Page for Fun or something.
    print("Expanding My Network")
    linkedin_network = client.get(MY_NETWORK, headers=headers)

    # Pull out the JSESSIONID from the cookie header and set it as the CSRF Token.prob move this
    jsessionid = str(linkedin_network.request.headers['cookie']).split(';')[4:-4]
    jsessionid_join = str("".join(jsessionid))
    pattern = r'"([^"]*)"'
    a_join = re.findall(pattern, jsessionid_join)
    csrf_token = str("".join(a_join))
    apicsrf = {
        'csrf-token': csrf_token
    }
    # Get the fs_miniProfile from the Linkedin User API. We'll use this to invite them.
    linkedin_invites = client.get(INVITES, headers=apicsrf)
    invites = json.loads(linkedin_invites.text)
    # Invite Peeeeeeeople
    for item in invites['elements']:
        id = str(item['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['entityUrn']).split(":")[3]
        # Build the data
        data = '{"trackingId":"yvzykVorToqcOuvtxjSFMg==","invitations":[],"excludeInvitations":[],"invitee":{"com.linkedin.voyager.growth.invitation.InviteeProfile":{"profileId":' + '"' + id + '"' + '}}}'
        rando_sleep(1,3)
        post_invites = client.post(INVITE_POST, headers=apicsrf, data=data)
        if post_invites.status_code == 201:
            success = success + 1
        elif post_invites.status_code == 406:
            failed = failed + 1
    return success


def random_user_actions():
    print("Do Random Things")
    the_thing = randint(1,4)
    if the_thing == 1:
        open_main()
    if the_thing == 2:
        open_my_network()
    if the_thing == 3:
        open_jobs_feed()
    if the_thing == 4:
        rando_sleep(1, 300)


if __name__ == '__main__':
    # Connect to Linkedin Account whatever
    connect(config.username,config.password)
    zeerg() # print that sweet logo
    # Invite People to My Network
    # Add some randomness to invites Opening pages...etc.
    invites_sent = 0
    while invites_sent < config.invites_to_send:
        random_user_actions()
        invites_sent = invites_sent + increase_network()
        print("Successful Invites Sent: " + str(invites_sent))
        rando_sleep(1,300)
        random_user_actions()
