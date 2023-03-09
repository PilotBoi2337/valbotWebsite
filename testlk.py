from flask import Flask, render_template, request, redirect, url_for
import asyncio
import sys
import nest_asyncio
import riot_auth
import requests
nest_asyncio.apply()
app = Flask(__name__)
skins_list = []
url_list = []
cost = []
mylist = []
mylist1 = []
mylist2 = []
@app.route('/')
def index():
    return render_template('index.html')
async def check(username, password):
                CREDS = username, password

                auth = riot_auth.RiotAuth()
                asyncio.run(auth.authorize(*CREDS))


                authtoken = (auth.access_token)
                entitled = (auth.entitlements_token)
                userid = (auth.user_id)
                asyncio.run(auth.reauthorize())
                url = (f"https://pd.na.a.pvp.net/store/v2/storefront/{userid}")


                payload = ""
                headers = {
                        "X-Riot-Entitlements-JWT": (entitled),
                        "Authorization": (f"Bearer {authtoken}")
                    }


                response = requests.request("GET", url, data=payload, headers=headers)




                li = list(response.text.split('"'))

                    
                loc = (li.index("SkinsPanelLayout"))

                item1 = loc + 4
                item2 = item1 + 2
                item3 = item2 + 2
                item4 = item3 + 2

                priceitem1 = item1 + 23
                priceitem2 = priceitem1 + 26
                priceitem3 = priceitem2 + 26
                priceitem4 = priceitem3 + 26
                li = list(response.text.split('"'))

                first = (li[item1])
                second = (li[item2])
                third = (li[item3])
                fourth = (li[item4])







                url = "https://valorant-api.com/v1/weapons/skins"

                payload = ""
                response = requests.request("GET", url, data=payload)

                uuidsort = list(response.text.split('"'))
   
                for val in uuidsort:
                        if val == first:
                            loc2 = uuidsort.index(val)
                            title=(uuidsort[loc2+4])
                            url=(uuidsort[loc2+10])
                       
                            value=(li[priceitem1])
                            
                        elif val == second:
                            loc2 = uuidsort.index(val)
                            url1=(uuidsort[loc2+10])
                            title1=(uuidsort[loc2+4])
                           
                            value1=(li[priceitem2])
                           

                        elif val == third:
                            loc2 = uuidsort.index(val)
                            url2=(uuidsort[loc2+10])
                            title2=(uuidsort[loc2+4])   
                            value2=(li[priceitem3])
                           
 
                        elif val == fourth:
                            loc2 = uuidsort.index(val)
                            title3=(uuidsort[loc2+4])
                            url3=(uuidsort[loc2+10])
                            
                            value3=(li[priceitem4])


                return title, title1, title2, title3, url, url1, url2, url3, value, value1, value2, value3

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    asyncheck = check(username, password)
    data = (asyncio.run(asyncheck))
    print(data)
    skins_list.append(data[0:4])
    url_list.append(data[4:8])
    cost.append(data[8:12])
    print(skins_list)
    print(cost[0])
    print(url_list)

    return redirect(url_for('dashboard'))
    
@app.route('/dashboard')
def dashboard():
    mylist = ' '.join(cost[0]).replace('}','').split()
    mylist1 = ' '.join(mylist).replace(':','').split()
    mylist2 = ' '.join(mylist1).replace(',','').split()

    print(mylist2)
    rendered_template = render_template('dashboard.html', skin0=skins_list[0][0], skin1=skins_list[0][1], skin2=skins_list[0][2], skin3=skins_list[0][3], url0=url_list[0][0], url1=url_list[0][1], url2=url_list[0][2], url3=url_list[0][3], cost0=mylist2[0], cost1=mylist2[1], cost2=mylist2[2], cost3=mylist2[3])
    skins_list.clear()
    url_list.clear()
    mylist.clear()
    mylist1.clear()
    mylist2.clear()
    return rendered_template

    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=3000)
