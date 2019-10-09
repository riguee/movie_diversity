import requests as req
import json
import pandas as pd
import urllib.request
import urllib


def test_ethnicity_lookup():
    all_ethnicities_and_actors = []
    for year in all_actors_by_year.keys():
        for actor in all_actors_by_year[year]:
            print(actor)
            try:
                data = session.get('https://ethnicelebs.com/'+actor.replace(' ', '-'))
                soup = BeautifulSoup(data.content, 'html.parser', from_encoding="utf-8")
                test_value = (soup.findAll(text=re.compile("Ethnicity:")))
                ethnicity = test_value[0].split(':')[1].strip()
            except:
                ethnicity = ''
            print('ethnicity is '+ethnicity)
            all_ethnicities_and_actors.append({'year':year, 'actor':actor,'ethnicity': ethnicity})
    print(all_ethnicities_and_actors)

def nndb_ethnicity_lookup(actor_name):
    search_url = 'http://search.nndb.com/search/nndb.cgi?nndb=1&omenu=unspecified&query=%s'
    people_url_prefix = 'http://www.nndb.com/people/'
    print('-- Searching ethnicity on NNDB for %s' % actor_name)
    tmp = urllib.request.urlopen(search_url % urllib.parse.quote_plus(actor_name))
    result = tmp.read()
    soup = BeautifulSoup(result,features="html.parser")
    all_results = soup.find_all('a')
    potential_results = []
    for link in all_results:
        if (link.get('href').startswith(people_url_prefix) and link.contents[0] == actor_name.strip()):
            potential_results.append(link.get('href'))
    if len(potential_results) > 1:
        print("-- -- Multiple results for %s. Aborting." % actor_name)
        return
    if len(potential_results) <= 0:
        print("-- -- No result for %s. Aborting." % actor_name)
        return
    tmp = urllib.request.urlopen(potential_results[0])
    result = tmp.read()
    soup = BeautifulSoup(result,features="html.parser")
    ethnicity_occ = soup.findAll(text=re.compile("Ethnicity"))
    if (len(ethnicity_occ) > 0):
        return ethnicity_occ[0].next_element.strip()
    return 'Unknown'

def add_ethnicities(actors_by_year):
    actors_to_search = []
    all_actor_ethnicities = []
    existing_actors =  pd.read_csv('all_actors_2.csv', encoding='utf_8')
    actors_to_find = 0
    actors_found = 0
    # actors_to_search = pd.DataFrame(columns=['actor'])
    # all_actor_ethnicities = pd.DataFrame(columns=['actor', 'ethnicity'])
    all_actors = []
    for year in actors_by_year.keys():
        all_actors+=actors_by_year[year]
    all_actors = list(dict.fromkeys(all_actors))
    for actor in all_actors:
        try:
            actor = actor.strip()
            ethn = existing_actors['ethnicity'].loc[existing_actors['actor'] == actor].iloc[0]
            print('actor '+ actor.strip() +' in the database already')
        except:
        # if actor.strip() in existing_actors['actor']:
        #     print(actor +' exists in the database already')
            # all_actor_ethnicities.append([actor.strip(), ""])
            try:
                ethnicity = nndb_ethnicity_lookup(actor)
                if ethnicity == 'Unknown' or ethnicity == '' or ethnicity == None:
                    print(actor+" wasn't found in the nndb database")
                    actors_to_search.append(actor.strip())
                    actors_to_find+=1
                else:
                    all_actor_ethnicities.append([actor.strip(), ethnicity])
                    actors_found+=1
            except:
                print('An error happened while looking up the ethnicity of '+actor)
    print(all_actor_ethnicities)
    print(actors_to_search)
    all_actor_ethnicities = pd.DataFrame(all_actor_ethnicities)
    print(all_actor_ethnicities)
    # all_actor_ethnicities.to_csv("test_actors.csv")
    actors_to_search =  pd.DataFrame(actors_to_search)
    with open('all_actors.csv', 'a', encoding="utf-8") as f:
        all_actor_ethnicities.to_csv(f, header=False)
    with open('unknown_actors.csv', 'a', encoding="utf-8") as f:
        actors_to_search.to_csv(f, header=False)
#len_df['category_sub_1'].loc[len_df['sku'] == prod_ref].iloc[0]
