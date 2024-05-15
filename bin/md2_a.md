
# MD2 Script

__Terms__
* __NF__ means Not Found
* __\<root>__ refers to the current repo's root folder
* __\<repo>__ refers to a target or new repository
* __configure__ refers to the setting of values which alter the outcome of a process
* __initiate__ means to start/execute a process
* __initialize__ refers to the creation of something when nothing was there previously
* __template__ refers to a file of content, complete with template-keys and/or default values

## MD2 Process

 Make what is not there
1. [__Initialize__ md2](#initialize~md2)
1. [__Configure__ Environment Values](#configure~environment~values)
1. [__Initialize__ Repository](#clone~process)
1. __Commit__ Environment Values

### Initialize md2

 Make the md2.env file
* __Create__ '\<root>/bin/md2.env' __From__ template __When__ file NF

### Configure Environment Values
1. Project Values
    * __Configure__ WS_ORGANIZATION
    * __Configure__ WS_WORKSPACE
    * __Configure__ WS_PROJECT
    * __Configure__ WS_REPO

2. GitHub Values
    * __Configure__ GH_TRUNK
    * __Configure__ GH_PROJECT
    * __Configure__ GH_BRANCH
    * __Configure__ GH_REPO
    * __Configure__ GH_USER
    * __Configure__ GH_MESSAGE
    * __Configure__ GH_TOKEN

### Initialize Repository
 Create and Configure a Project Repository.
* __Create__ Branch Folder __When__ folder is NF
* __Clone__ '\<repo>' __When__ repo is NF
* __Patch__ .gitignore

* Fix the .gitignore file

### Commit Environment Values

 Save user's environment changes.
1. __Commit__ Environment Values __To__ '\<root>/bin/md2.env'
## Classes

### Process Package

* __set__
* __get__
* __assign__
* __show__

### Process Project

 Base class for project methods
* optional recorder
* template_folder_key, eg 'github'

* __get_env_var__
* __set_env_var__, eg
* __get_template_key_list__, list of template formated env vars, eg. [{\<\<GH_A>>:'abc'}, ...]
* __get_template_folder_key__, eg 'github'
* __get_template_folder__, location of templates
* __get_branch_folder__, location of git branch
* __get_repo_folder__, location of github repo
* __configure_environment__, manually set or confirm env vars
* __makedirs__, make folders from a folder file name
* __templatize__ convert templates to code