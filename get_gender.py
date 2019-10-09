import requests as req
import json
import pandas as pd
from datetime import datetime

def gender(gender):
    genders = {
    0: "unknown",
    1: "female",
    2: "male"
    }
    return genders.get(gender,"unknown")

def searchGender(actor):
    output = {"response" : False}
    search_actor_url = "https://api.themoviedb.org/3/search/person?api_key=c4d48123a2a6f5d1d47be09f93ecc8db&language=en-US&query={}&page=1&include_adult=true".format(actor)
    response = req.get(search_actor_url)
    if response.status_code == 200:
        resp = response.json()
        for i in range(resp['total_results']):
            if resp['results'][i]['known_for_department']=='Acting':
                output["response"] = True
                actor_id = resp['results'][i]['id']
                print(actor_id)
                break

        if output["response"] ==False:
            output["data"] = 'No result was found for actor {}'.format(actor)
            return(output)
    else:
        output["response"] = False
        ourput["data"] = 'There was an error with the actor search'
        return(output)

    search_gender_url = "https://api.themoviedb.org/3/person/{}?api_key=c4d48123a2a6f5d1d47be09f93ecc8db&language=en-UK".format(actor_id)
    response = req.get(search_gender_url)
    if response.status_code == 200:
        resp = response.json()
        bday = resp['birthday']
        if bday!= None:
            bday = datetime.strptime(bday, '%Y-%m-%d').date()
        else:
            bday = "unknown"
        gder = gender(resp['gender'])
        output["response"] = True
        output["data"] = [gder, bday]
        print("{}'s birthday is {}".format(actor, bday))
        print("Their gender id is {}".format(gder))
        return(output)
    else:
        output["response"] = False
        output["data"] = 'There was an error with the API actor id query'
        return(output)

def getInfoOnActors(casting):
    errors = 0
    false_results = []
    good_results = []
    ok = 0
    for actor in casting[2019]:
        actor_info = searchGender(actor)
        if actor_info["response"] == False:
            errors+=1
            false_results.append([actor, actor_info["response"], actor_info["data"]])
        else:
            ok+=1
            good_results.append([actor, actor_info["response"], actor_info["data"][0], actor_info['data'][1]])
    gr_df = pd.DataFrame(good_results)
    fr_df = pd.DataFrame(false_results)
    with open('actor_info.csv', 'a', encoding="utf-8") as f:
        gr_df.to_csv(f, header=False, index=False)
    with open('actor_info_unknown.csv', 'a', encoding="utf-8") as f:
        fr_df.to_csv(f, header=False, index=False)
