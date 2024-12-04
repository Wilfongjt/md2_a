from able import ClassNameable
class Section(ClassNameable):

    def scalars(self, section_dict):
        # print('scalars_nv 1')
        scalar_list = []
        parent_name = self.getClassName()
        print('scalar_nv', parent_name)
        print('scalar_nv', section_dict)
        for key, value in section_dict.items():
            # print('scalars_nv 2',type(value))
            if type(value) not in [dict, list]:
                # print('scalars_nv 3', '{}_{}'.format(parent_name, key).upper() )
                scalar_list.append({'{}_{}'.format(parent_name.upper(), key.upper()): value})

        return scalar_list

def test_section(s):
    from pprint import pprint
    from source.component.markdown.project_string_default import ProjectStringDefault
    from source.component.markdown.tier_md import TierMD
    from source.component.markdown.claims import Claims
    from source.component.markdown.model import Model

    status.addTitle('section test')
    project_dict = TierMD(ProjectStringDefault())

    actual = Section()
    print('claim', Claims(project_dict, 'api_admin'))
    actual.scalars(Claims(project_dict, 'api_admin'))

    #actual.scalars(project_dict)

def main(status):
    test_section(status)

if __name__ == "__main__":
    # execute as docker
    from source.component.status import Status
    from source.component.status_report import StatusReport

    status = Status()
    # execute as docker

    main(status)
    print(StatusReport(status))