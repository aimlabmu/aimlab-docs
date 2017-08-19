from os import walk, sep, path

def getDocsTreePath():
  tempDict = {}
  collection = []

  exclude = ['/docs', '/.git', '/.vscode']
  for r,d,p in walk('.'):
    if not True in [i in r for i in exclude]:
      temp = r.split('/') 
      if(len(temp[1:]) == 2):
        collection.append(temp[1:] + [path.join(r, 'readme.md')])

  keys = [i[0] for i in collection]

  for key, val in zip(keys, collection):
    try:
      tempDict[key]
    except:
      tempDict[key] = []

    if key in val:
      # print(val)
      tempDict[key].append({val[-2]: val[-1]})
      
  # print(tempDict)    
  return tempDict