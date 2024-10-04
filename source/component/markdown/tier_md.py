from able import Stack, Level
from source.component.tier import Tier
from source.component.markdown.max import Max
from source.component.markdown.min import Min

class TierMD(Tier):
    def __init__(self, md_text, echo=False):
        # completely replace the parent class's __init__ method
        # skip spaces
        # skip *
        # stack = Stack()
        ostack = Stack()

        table = False
        tbl_cols = []
        # last_key = ''
        # last_obj = {}
        i = 0
        # a = 0
        resource_key = ''
        parent_key=''
        level = 0

        lntyp = 5
        line_len = 15
        stk_len = 52
        for ln in str(md_text).split('\n'):

            # calc tree level
            level = Level(ln)
            ln = ln.split('...')  # remove the ... comment , '# project: ... a comment'
            ln = str(ln[0])  # point to '# project:'
            ln = ln.replace('|', ' | ')  # fix |aud|iss|sub| --> | aud | iss | sub |

            # split up
            ln = ln.replace(':', '').strip()  # fix dangling colons eg "claim:" -> "claim"
            ln = ln.split(' ')

            if not ln[0].startswith('|'):
                table = False

            if ln[0].startswith('#'):
                # remove stack items when stack size > line size

                if ln != ['']: ostack.pop(count=ostack.size() - level)
                if ostack.size() == level:
                    if ostack.size() > 1: ostack.pop(1)  # when size is 1 then at tree trunck ... will add branch later

                # stack should always have 1 item a position 0
                if len(ln) > 2:
                    raise Exception('Bad Line {}'.format(ln))

                level = Level(ln[0])

                if level == 1:
                    '''
                                lv  sz  pop     action                                         stack                        D
                    l0 l1               sz-lv
                     # a:       1   0   -1      pop(-1)                                         []                          {}
                                                lv==1 and l1 not in D: D[L1]={a}                []                          {a:{<a>}}
                                                push(D[L1])                                     [{<a>}]                     {a:{<a>}}
                    '''
                    if ln[1].lower() not in self:
                        parent_key= ln[1]
                        self[ln[1].lower()] = {}  # initialize the tree trunk
                        ostack.push(self[ln[1].lower()])  # push value
                        if echo:
                            print('L0'.ljust(2), 'L1l'.ljust(line_len, ' '), 'lv'.rjust(3, ' '), 'sz'.rjust(3, ' '),
                                  'pop'.rjust(3), 'stack'.ljust(stk_len))
                            print('--'.ljust(2), '--'.ljust(line_len, '-'), '--'.ljust(3, '-'), '--'.ljust(3, '-'),
                                  '--'.ljust(3, '-'), '--'.ljust(stk_len, '-'))
                            print(ln[0].ljust(lntyp), ln[1].ljust(line_len), str(level).rjust(3),
                                  str(ostack.size()).rjust(3), str(ostack.size() - level).rjust(3),
                                  str(ostack).ljust(stk_len), '-->', self)

                elif level > 1:
                    '''
                                lv  sz  pop     action                                         stack                        D
                    l0 l1               sz-lv                    
                    ## <a1>:    2   1   -1      pop(-1)                                         [{<a>}]                     {a:{<a>}}
                                                lv>1 and len(D) == 0: Exception('Bad Tree')     
                                                lv>1 and L1 in peek(): Exception('Duplicate')   
                                                lv>1 and L1 not in peek(): peek()[L1]={<a1>}    [{1'a1':{<a1>}}]            {a:{1'a1':{<a1>}}}
                                                lv>1 and sz == 0: Exception('Line out of order')
                                                lv>1 and sz != 0: push(peek()[L1])              [{1'a1':{<a1>}},{<a1>}]     {a:{1'a1':{<a1>}}}
                                                otherwise: Exception('Unknown Command')                    
                    '''
                    parent_key = ln[1]
                    if level==4:
                        #print('resource', ln[1].lower())
                        resource_key=ln[1].lower()
                    if ln[1].lower() not in ostack.peek():
                        ostack.peek()[ln[1].lower()] = {}
                        ostack.push(ostack.peek()[ln[1].lower()])
                    if echo:
                        print(ln[0].ljust(lntyp), ln[1].ljust(line_len), str(level).rjust(3),
                              str(ostack.size()).rjust(3),
                              str(ostack.size() - level).rjust(3), str(ostack).ljust(stk_len), '-->', self)

            elif ln[0] == '1.':

                # splits should be ['#','project'] or ['1.','cat','val']
                if len(ln) > 3:
                    raise Exception('Bad Line {}'.format(ln))
                #print('ln',ln)
                ostack.peek()[ln[1].lower()] = ln[2]
                # no push here
                if echo:
                    print(ln[0].ljust(lntyp), ln[1].ljust(line_len), str(level).rjust(3), str(ostack.size()).rjust(3),
                          str(ostack.size() - level).rjust(3), str(ostack).ljust(stk_len), '-->', self)

            elif ln[0] == '|':

                if not table:  # create list of column names
                    table = True
                    tbl_cols = [c for c in ln if c not in ['|', '']]

                elif ln[0].startswith('|') and ln[1].startswith('-'):  # table line break
                    pass
                else:  # parse row
                    #print('ln', ln)
                    tbl_att_row = [c for c in ln if c not in ['|', '']]
                    tbl_att_row = [c.strip() for c in tbl_att_row if c != '']  # ['','abc','', 'xyz',''] --> ['abc', 'xyz']
                    tbl_att_row = {tbl_cols[i]: tbl_att_row[i] for i in range(len(tbl_att_row))}
                    # break down the size (3-330) into size_min: 30, size_max: 330
                    if 'size' in tbl_att_row:
                        tbl_att_row['size_min']=Min(tbl_att_row)
                        tbl_att_row['size_max']=Max(tbl_att_row)
                        tbl_att_row['resource']=resource_key.lower()
                        tbl_att_row['pattern']='^.{{}}$'.replace('{}','{},{}'.format(Min(tbl_att_row),Max(tbl_att_row)))

                    #print('tbl_row', tbl_att_row)

                    ostack.peek()[tbl_att_row[tbl_cols[0]]] = tbl_att_row
            elif ln == ['']:
                if echo:
                    print('     blank line')
            else:
                pass
                # raise Exception('Unknown line error "{}"'.format(ln))

            i += 1

def tierMD_test():
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    # filename_md = 'project_test_prj.md'
    # folderfilename_md = '{}/{}'.format(os.getcwd(), filename_md)
    # print('folderfilename_md', folderfilename_md)
    # resource_string = getProjectMDString(Tier(getProjectString())) # StringReader(folderfilename_md)
    # print('resource_string',resource_string)
    # project_dict = Tier(getProjectString())

    #print(ProjectStringDefault())
    actual = TierMD(ProjectStringDefault())
    pprint(actual)
    #pprint(actual)
    #print('model',actual.find('model'))
    #pprint(actual.find('model'))
    assert('project' in actual)
    assert('data' in actual.find('account'))
    assert('model' in actual.find('account'))
    claims = Tier(actual.find('claim'))
    print('claims', claims)

    assert('parent' in claims)
    assert ('claim' == claims['parent'])
    assert('type' in claims)
    assert('api_admin' in claims)
    assert('api_guest' in claims)
    assert('api_user' in claims)

    resources = Tier(actual.find('resources'))
    #print('resources', resources)
    assert ('parent' in resources)
    assert ('resources' == resources['parent'])
    assert ('account' in resources)
    resource = Tier(actual.find('account'))
    #print('resource', resource)
    assert ('schema' in resource)
    assert ('version' in resource)
    assert ('active' in resource)
    assert ('model' in resource)
    assert ('data' in resource)

def main():
    tierMD_test()


if __name__ == "__main__":
    # execute as docker
    main()