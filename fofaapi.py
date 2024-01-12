import requests
import base64
import sys

def FofaAPICall(query, email, api_key):
    fields = 'host,ip,port,protocol,country_name,title,icp,country'
    qbase64 = base64.b64encode(query.encode()).decode()
    api = f'https://fofa.info/api/v1/search/all?email={email}&key={api_key}&qbase64={qbase64}&size=10000&fields={fields}'

    response = requests.get(api)
    if response.json().get('error'):
        print(response.json().get('errmsg'))
        return list()

    try:
        results = response.json().get("results",list())
        #print(results)
        print("\033[38;2;24;254;27m[ {} ]\033[0m Fofa API Search {} Results.".format(query, len(results)))

    except Exception as error :
        print(error)
        return list()

    hosts = list()
    file_name = "{}.csv".format(query.replace(" ","_"))

    with open(file_name,"a") as results_file:
        results_file.write(fields+"\n")

        for result in results:
            hosts.append(
                    result[0].strip()
                    )
            results_file.write(
                    ",".join(result)+'\n'
                    )
    return hosts

if __name__=="__main__":
    FofaAPICall(
            query = sys.argv[1],
            email=None,
            api_key=None
            )
