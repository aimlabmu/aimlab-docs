import utils
import os
import shutil

# get dict of docs path
docp = utils.getDocsTreePath()

# path of where contents will be stored
content_store = os.path.join(os.curdir, 'docs', 'pages', 'aimlabdocs')

# function to add frontmatter section
def addFrontMatter(title, permalink):
  fm = '''---
title: {0}
keywords: 
sidebar: aimlab_sidebar
permalink: {1}
folder: aimlabdocs
---

'''.format(title, permalink)
  # print(fm)
  return fm

# function to parse content and return title and new content separately
def getTitleAndContent(old_content):
  # get splited of contents to manipulate title
  splited_content = old_content.split('\n')
  # get title from first line of document and strip '# ' out
  title = splited_content[0].split('# ')[-1]
  # reconstruct old contents from the line after first \n
  # check first if there is a blank line before starting new content
  if splited_content[1:][0] == '':
    new_content = '\n'.join(splited_content[2:])
  else:
    new_content = '\n'.join(splited_content[1:])

  # print('this is title: ' + title)
  # print('this is chopped content: ' + new_content)
  return (title, new_content)

# check if content store path exist, if not create one
if not os.path.exists(content_store):
  os.makedirs(content_store)

# loop through key of available content titles e.g. Python, Linux, etc.
for key in docp:
  # loop through each content (subtitles) of each key
  for val in docp[key]:
    # get value of subtitle dict which is a path to the file (val is a key of 
    # content of each dict which contains content name as key and url as value)
    old_file_path = docp[key][val]
    # rename file as non-space and subtitle name instead of 'readme.md'
    new_file_name = utils.getJekyllDocsPath(old_file_path, format='md')
    # set path where this content will be placed
    new_file_path = os.path.join(content_store, new_file_name)
    # move file to new path
    shutil.copy(old_file_path, new_file_path)
    print(new_file_path)
    # read moved file to get content
    with open(new_file_path, 'r') as f:
      old_content = f.read()
      f.close()
    # open as write mode to add frontmatter 
    # i.e. move # to title tag
    with open(new_file_path, 'w') as f:
      # get title and new content
      title, new_content = getTitleAndContent(old_content)
      for i in new_content.split('\n'):
        if '![' in i:
          tmp = i.split('img')
          tmp2 = tmp[0]+"pages/aimlabdocs/img"+tmp[1]
          new_content = new_content.replace(i, tmp2)
          print(i, 'is replaced by', tmp2)
      # write front matter to the file
      # permalink need to be html format instead of none or md
      f.write(addFrontMatter(title, utils.getJekyllDocsPath(old_file_path, format='html')))
      # write new content
      f.write(new_content)
      f.close()
