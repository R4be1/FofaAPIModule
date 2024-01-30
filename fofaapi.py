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
        print("\033[38;2;24;254;27m[ {} ]\033[0m Fofa API Search {} Results.".format(query, len(results)))

    except Exception as error :
        print(error)
        return list()

    hosts = list()
    file_name = "{}.csv".format(query.replace(" ","_"))
    urls_file = open("urlresults.txt","w")

    with open(file_name,"a") as results_file:
        results_file.write(fields+"\n")

        for result in results:
            url = result[0].strip() + '://' +  result[1].strip() if '://' not in result[1] else result[1].strip()
            print(",".join(result))
            hosts.append( url )
            urls_file.write( url+'\n' )
            results_file.write( ",".join(result)+'\n' )

        urls_file.close()

    return hosts

if __name__=="__main__":
    FofaAPICall(
            query = sys.argv[1],
            email='',
            api_key=''
            )
