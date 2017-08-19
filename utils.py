from os import walk, sep, path

def getDocsTreePath():
  # define temporary variables
  tempDict = {}
  collection = []

  # set excluded paths
  exclude = ['/docs', '/.git', '/.vscode']

  # loop through dir
  for r,d,p in walk('.'):
    # loop through only not excluded paths
    if not True in [i in r for i in exclude]:
      # split path to access each value
      temp = r.split('/')
      # cut dot (pardir) out and only use list splited from full path
      if(len(temp[1:]) == 2):
        # add path and subtitles of each title to collection list
        collection.append(temp[1:] + [path.join(r, 'readme.md')])

  # get keys which are each first val of the list
  keys = [i[0] for i in collection]

  # loop through zip of keys and collection
  for key, val in zip(keys, collection):
    # try calling dict of specific key if not exist create blank dict for that key
    try:
      tempDict[key]
    except:
      tempDict[key] = {}

    # if key and val matches, put val in that key
    if key in val:
      # print(val)
      tempDict[key][val[-2]] = val[-1]
      
  # print(tempDict)    
  return tempDict

def getJekyllDocsPath(full_original_path):
  temp = full_original_path.split(sep)
  return "{0}_{1}.html".format(temp[-3], temp[-2]).replace(' ','')