import utils
import os
import shutil

# get dict of docs path
docp = utils.getDocsTreePath()

content_store = os.path.join('docs', 'pages', 'aimlabdocs')



if not os.path.exists(content_store):
  os.makedirs(content_store)

for key in docp:
  for val in docp[key]:
    temp = docp[key][val]
    # print(temp.split(os.sep))
    # print(content_store)
    # print(os.path.join(content_store, utils.getJekyllDocsPath(temp)))
    shutil.copy(docp[key][val], os.path.join(content_store, utils.getJekyllDocsPath(temp)))
    

# print(docs_path_dict)

