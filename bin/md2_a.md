
## Environment
* last github organization
* last workspace
* last project
* last trunk
* last branch
* last repo
* last user
* last message
* last token
* MD2DM_INPUT_FOLDER defines where to get input
* MD2DM_OUTPUT_FOLDER defines where to send output
* MD2DM_OUTPUT_FILENAME defines the name of the output file

__Terms__
* __NF__ means Not Found
* __\<root>__ refers to the current repo's root folder
* __\<repo>__ refers to a target or new repository
* __configure__ refers to the setting of values which alter the outcome of a process
* __initiate__ means to start/execute a process
* __initialize__ refers to the creation of something when nothing was there previously
* __template__ refers to a file of content, complete with template-keys and/or default values

### Initialize md2

 Make the md2.env file
* __Create__ '\<root>/bin/md2.env' __From__ template __When__ file NF
### Configure Environment Values

 Interactively configure values
1. Project Values

    * __Configure__ WS_ORGANIZATION
    * __Configure__ WS_WORKSPACE
    * __Configure__ WS_PROJECT

2. GitHub Values
    * __Configure__ GH_TRUNK
    * __Configure__ GH_PROJECT
    * __Configure__ GH_BRANCH
    * __Configure__ GH_REPO
    * __Configure__ GH_USER
    * __Configure__ GH_MESSAGE
    * __Configure__ GH_TOKEN

### Clone GitHub Repository
 Create and Configure a Project Repository
* __Create__ Branch Folder __When__ folder is NF
* __Clone__ '\<repo>' __When__ repo is NF

### Initialize GitHub Repository

* Fix the .gitignore file
  * __Create__ '\<repo>/.gitignore' file __When__ file is NF
  * __Upsert__ '\<repo>/.gitignore' __Set__ line = '\*.env'
  * __Upsert__ '\<repo>/.gitignore' __Set__ line = '.idea/'

* Update .env with github variables

 TBD...
  * __Create__ '\<repo>/.env' file __When__ file is NF
* Create github code
  * __Create__ '\<repo>/scripts/' folder __When__ folder is NF
  * __Create__ '\<repo>/scripts/git.rebase.sh.c-u-.tmpl' file __When__ file is NF
  * Create source folder
* __Create__ '\<repo>/source/' folder __When__ folder is NF
* __Create__ '\<repo>/bin/' folder __When__ folder is NF
* __Create__ '\<repo>/bin/md2.env' __When__ file NF
* __Upsert__ '\<repo>/bin/md2.env' __Set__ line = GH_*
* __Upsert__ '\<repo>/bin/md2.env' __Set__ line = WS_*
* Convert Templates to Code

### Commit Environment


## MD2 Process

 Make what is not there
1. [__Initialize__ md2](#initialize~md2)
1. [__Configure__ Environment Values](#configure~environment~values)
1. [__Clone__ GitHub Repository](#clone~process)
1. [__Initialize__ GitHub Repository](#initialize~clone)
1. __Commit__ Environment Values __To__ '\<root>/bin/md2.env'

## The RecursionList

__RecursionList__

 List of files, folders and subfolders

* Ignore specific files and/or folders (eg ['.DS_Store', '.git', '.gitignore', '.idea']) on evaluation
* List of folders, subfolder and files in a given folder on request