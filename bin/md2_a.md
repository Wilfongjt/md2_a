
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
1. [__Clone__ GitHub Repository](#clone~process)
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

### Clone GitHub Repository
 Create and Configure a Project Repository
* __Create__ Branch Folder __When__ folder is NF
* __Clone__ '\<repo>' __When__ repo is NF

* Fix the .gitignore file

### Commit Environment Values

1. __Commit__ Environment Values __To__ '\<root>/bin/md2.env'
## Classes

### Process Project

 Base class for common methods
* optional recorder
* template_subfolder_name, eg 'github'
* get_env_var
* set_env_var
* configure_environment
* get_template_subfolder
* get_template_name_value_pairs
* get_branch_folder
* get_repo_folder
* makedirs
* templatize