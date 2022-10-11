from flask import Flask, request, Response
import sys
import json 
import base64
import requests
# import yaml

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def create_cluster_selector_yaml(filename, selectors):

    labels = ""
    for label in selectors:
        print(label)
        print(selectors[label])



    yaml = {
        "kind": "ClusterSelector",
        "apiVersion": "configmanagement.gke.io/v1",
        "metadata": {
            "name": "hello",
            "spec": {
                "selector": {
                    "matchLabels": selectors
                } 
            }
        }
    }

    print(yaml)

    # Format into YAML string
    formatted_yaml = json.dumps(yaml, indent=2)
    formatted_yaml = formatted_yaml.replace('{', '')
    formatted_yaml = formatted_yaml.replace('}', '')
    formatted_yaml = formatted_yaml.replace('"', '')
    formatted_yaml = formatted_yaml.replace(',', '')
    formatted_yaml = formatted_yaml.split("\n", 1)[1]
    print(type(formatted_yaml))
    print(formatted_yaml)
                
    return formatted_yaml

# Params:
# n selectors in the form of key:value
# which policy to apply to 
@app.route("/selector/create/", methods=['POST'])
def create_selector():
    # Get selectors from query
    params = request.get_json()
    print(params)
    print(params['selectors'])
    selectors = params['selectors']
    yaml = create_cluster_selector_yaml("selector2", selectors)

    # Create a yaml file with the desired selectors
    selector_name = params['selector_name']

    # Encode to base64
    yaml_bytes = yaml.encode("ascii")
    yaml_bytes = base64.b64encode(yaml_bytes)
    yaml_b64 = yaml_bytes.decode("ascii")
    print(yaml_b64)
    print(type(yaml_b64))

    # Push to github
    user = "janinebar"
    repo = "sample"
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{selector_name}.yaml"
    r = requests.put(
        url, 
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        },
        data = json.dumps({
            "message": f"new selector: {selector_name}",
            "content": yaml_b64
        })
    )
    

    return Response(r, status=200)


