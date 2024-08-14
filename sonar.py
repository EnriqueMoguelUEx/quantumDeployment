# import pyyaml module
import yaml
from yaml.loader import SafeLoader
import requests

def generate():
    # Open the file and load the file
    with open('openapi.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
    urls={}
    names={}
    for i in data['paths']:
        for j in data['paths'][i]:
            if 'x-quantumCode' in data['paths'][i][j]:
                urls[data['paths'][i][j]['x-quantumCode']]=data['paths'][i][j]['x-quantumProvider']
            if 'operationId' in data['paths'][i][j] and 'x-quantumCode' in data['paths'][i][j]:
                names[data['paths'][i][j]['x-quantumCode']]=data['paths'][i][j]['operationId']
    x=None
    for i in urls.keys():
        f = open('./sonarQuantumAnalysis/'+names[i]+'.py', "w")
        if i.endswith('.py'):
            x = requests.get(i).text
            f.write(x)
        else:
            header_value=i
            header_value_utf8 = header_value.encode('utf-8')
            if urls[i]=='aws':
                x = requests.get('http://quantumservicesdeployment.spilab.es:8081/code/aws', headers={"x-url":header_value_utf8}).json()['code']
            else:
                x = requests.get('http://quantumservicesdeployment.spilab.es:8081/code/ibm', headers={"x-url":header_value_utf8}).json()['code']
            for line in x:
                f.write(line+'\n')
        f.close()

if __name__ == '__main__':
    generate()