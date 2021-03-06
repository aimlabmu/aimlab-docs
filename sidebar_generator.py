import utils

docs_path_dict = utils.getDocsTreePath()

def addTopLevelDocs():
  text = '''# This is your sidebar TOC. The sidebar code loops through sections here and provides the appropriate formatting.

entries:
- title: sidebar
  product: AIMLAB DOCUMENTATION
  version: 
  folders:
  '''
  # print(text)
  return(text)

def addFirstLevelDocs(title, folderitems=''):
  text = '''
  - title: {0}
    output: web, pdf
    folderitems: {1}
    '''.format(title, folderitems)
  # print(text)
  return(text)

def addSecondLevelDocs(title, url='/index.html'):
  text = '''
    - title: {0}
      url: {1}
      output: web, pdf
      '''.format(title, url)
  # print(text)
  return(text) 

def createYMLfile(content_dict):
  with open('docs/_data/sidebars/aimlab_sidebar.yml', 'w') as f:
    f.write(addTopLevelDocs())

    # sort key for alphabetically sorted sidebar
    for key in sorted(content_dict):
      f.write(addFirstLevelDocs(key))

      for val in content_dict[key]:
        f.write(addSecondLevelDocs(val, url='/'+utils.getJekyllDocsPath(content_dict[key][val])))
      
    f.close()

createYMLfile(docs_path_dict)

# with open('test.yml', 'w') as f: 
#   f.write(addTopLevelDocs())
#   f.write(addFirstLevelDocs('Python'))
#   f.write(addSecondLevelDocs('Environment Setup'))
#   f.write(addSecondLevelDocs('OpenCV'))
# 
  # f.close()
