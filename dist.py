
import marshal
import json
import base64

data = {}
plhash = {}
with open('rel.dat', 'rb') as f:
    data = marshal.load(f)

for i in data:
    plhash[i] = base64.b64encode(hex(hash(i)))

def buildpli(pl):
    info = {
        "name": pl,
        "size": len(data[pl]['influenced']) if pl in data else 5,
        "href": plhash[pl] if pl in plhash else "",
        }
    return info

for i in data:
    parents  = map(buildpli, data[i]['influenced-by'])
    children = map(buildpli, data[i]['influenced'])
    if i == 'C++':
        with open('data/graph.json', 'w') as f:
            json.dump({"name":i, "children": parents + children}, f);
    with open('data/%s.json'%(plhash[i]), 'w') as f:
        json.dump({"name":i, "children": parents + children}, f);
