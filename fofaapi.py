from urllib.parse import urlparse
import requests
import base64
import sys

def FofaAPICall(query, email, api_key):
    fields = ['protocol','host','ip','port','country_name','title','icp','country']
    fields = ",".join(fields)
    qbase64 = base64.b64encode(query.encode()).decode()
    api = f'https://fofa.info/api/v1/search/all?email={email}&key={api_key}&qbase64={qbase64}&size=10000&fields={fields}'

    response = requests.get(api)
    if response.json().get('error'):
        print(response.json().get('errmsg'))
        return list()

    try:
        results = response.json().get("results",list())

    except Exception as error :
        print(error)
        return list()

    hosts = list()
    file_name = "FofaResults.csv"
    urls_file = open("urlresults.txt","w")

    with open(file_name,"a") as results_file:
        print(f"Output File: {file_name}")
        results_file.write(fields+"\n")

        for result in results:
            url = result[0].strip() + '://' +  result[1].strip() if '://' not in result[1] else result[1].strip()
            print(",".join(result))
            hosts.append( url )
            results_file.write( ",".join(result)+'\n' )

        print("\033[38;2;24;254;27m[ {} ]\033[0m Fofa API Search {} Results.".format(query, len(results)))

        hosts = ResultsFilter(hosts)
        for url in hosts:
            urls_file.write( url+'\n' )
        urls_file.close()

        print("Filter {} Results.".format(len(hosts)))

    return hosts

def ResultsFilter(results):
    Temp = list()
    results = list(set(results))
    print("Unique data {} Results.".format(len(results)))
    return results

if __name__=="__main__":
    FofaAPICall(
            query = sys.argv[1],
            email='',
            api_key=''
            )
