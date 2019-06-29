import xmltodict
import re
from os import listdir
from Rsrc.Pathfinder_elements import *


class Pathfinder:

    def __init__(self, xsd_path, head_xsd_name = 'fcsExport.xsd'):
        self.schema_dict = Pathfinder.__make_schema_dict(xsd_path)
        self.__change_base_types()
        head_file = open(xsd_path + head_xsd_name, 'rb')
        self.export_elems = xmltodict.parse(head_file)['xs:schema']['xs:element']\
        ['xs:complexType']['xs:sequence']['xs:choice']['xs:element']

    def ConvertValues(self, xml):
        xml_new = {}
        self._preprocessing(xml, xml_new)
        if 'export' in xml_new:
            elem = list(xml_new['export'].keys())[0]
            xsd_elem, schema, _ = self.__find_elem_in_schema(elem, self.export_elems)
            self.__go_deeper(xsd_elem, schema, xml_new['export'], elem)
        else:
            raise Exception("Not an export")
        return xml_new['export']

    def __go_deeper(self, xsd_elem, schema, xml_dict, elem_name):
        if isinstance(xml_dict, dict):
            for key in xsd_elem:
                if key in ignorable_tags:
                    pass
                elif key in simple_transition_tags:
                    self.__go_deeper(xsd_elem[key], schema, xml_dict, elem_name)
                elif key in complex_transition_tags:
                    self.__complex_transition(xsd_elem, schema, xml_dict, elem_name, key)
                else:
                    print(xsd_elem.keys(), key)
                    raise Exception
        elif isinstance(xml_dict, list):
            for xml_item in xml_dict:
                if isinstance(xml_item, dict):
                    self.__go_deeper(xsd_elem, schema, xml_item, elem_name )
                else:
                    raise Exception("{}".format(type(xml_item)))

    def __complex_transition(self, xsd_elem, schema, xml_dict, elem_name, key):
        if key == 'xs:complexType':
            self.__go_deeper(xsd_elem['xs:complexType'], schema, xml_dict[xsd_elem['@name']], xsd_elem['@name'])

        elif key == 'xs:choice':
            if isinstance(xsd_elem['xs:choice'], list):
                for xsd_item in xsd_elem['xs:choice']:
                    self.__go_deeper(xsd_item, schema, xml_dict, elem_name)
            else:
                self.__go_deeper(xsd_elem['xs:choice'], schema, xml_dict, elem_name)

        elif key == '@base':
            if 'xs:' not in xsd_elem['@base']:
                current_xsd_elem, current_schema, _ = self.__find_elem_in_schema(xsd_elem['@base'], schema)
                self.__go_deeper(current_xsd_elem, current_schema, xml_dict, elem_name)
            else:
                if isinstance(xml_dict[elem_name], list):
                    for i, xml_item in enumerate(xml_dict[elem_name]):
                        xml_dict[elem_name][i] = eval("{}(xml_item)".format(type_dict[xsd_elem['@base']]))
                else:
                    xml_dict[elem_name] = eval("{}(xml_dict[elem_name])".format(type_dict[xsd_elem['@base']]))

        elif key == '@type':
            if 'xs:' not in xsd_elem['@type']:
                current_xsd_elem, current_schema, type_ = self.__find_elem_in_schema(xsd_elem['@type'], schema)
                if type_ == 'complex':
                    self.__go_deeper(current_xsd_elem, current_schema, xml_dict[xsd_elem['@name']], xsd_elem['@name'])
                else:
                    self.__go_deeper(current_xsd_elem, current_schema, xml_dict, xsd_elem['@name'])
            else:
                if isinstance(xml_dict[elem_name], list):
                    for i, xml_item in enumerate(xml_dict[elem_name]):
                        xml_dict[elem_name][i] = eval("{}(xml_item)".format(type_dict[xsd_elem['@base']]))
                else:
                    xml_dict[elem_name] = eval("{}(xml_dict[elem_name])".format(type_dict[xsd_elem['@type']]))

        elif key == 'xs:sequence':
            if isinstance(xsd_elem['xs:sequence'], list):
                for xsd_item in xsd_elem['xs:sequence']:
                    self.__go_deeper(xsd_item, schema, xml_dict, elem_name)
            else:
                self.__go_deeper(xsd_elem['xs:sequence'], schema, xml_dict, elem_name)
        elif key == 'xs:element':
            if isinstance(xsd_elem['xs:element'], list):
                for xsd_item in xsd_elem['xs:element']:
                    if xsd_item['@name'] in xml_dict:
                        self.__go_deeper(xsd_item, schema, xml_dict, xsd_item['@name'])
            else:
                xsd_item = xsd_elem['xs:element']
                if xsd_item['@name'] in xml_dict:
                    self.__go_deeper(xsd_item, schema, xml_dict, xsd_item['@name'])

    def __find_elem_in_schema(self, element_type, schema):
        found = False
        if ':' in element_type:
            current_schema = self.schema_dict[element_type.split(':')[0]]
            current_type = element_type.split(':')[1]
        else:
            current_schema = schema
            current_type = element_type
        if not isinstance(current_schema, list):
            for elem in current_schema['xs:complexType']:
                if elem['@name'] == current_type:
                    found = True
                    type_ = 'complex'
                    break
            if not found:
                for elem in current_schema['xs:simpleType']:
                    if elem['@name'] == current_type:
                        found = True
                        type_ = 'simple'
                        break
        else:
            for elem in current_schema:
                if elem['@name'] == current_type:
                    found = True
                    type_ = 'complex'
                    break
        if not found:
            print(element_type)
        assert(found)
        return elem, current_schema, type_

    def __change_base_types(self):
        schema = self.schema_dict['base']
        assert( ('xs:simpleType' in schema.keys()) and (isinstance(schema['xs:simpleType'], list))),\
            "Invalid BaseTypes.xsd"
        for elem in schema['xs:simpleType']:
            if elem['@name'] in xsd_base_types_conversion.keys():
                elem['@type'] = xsd_base_types_conversion[elem['@name']]
        self.schema_dict['base'] = schema

    def _preprocessing(self, dic, copy_dic):
        dic = dict(dic)
        assert(isinstance(copy_dic, dict)), "Copy dic is not a dict"
        for elem in dic:
            valid = True
            for item in set_of_forbidden:
                if item in elem:
                    valid = False
            if valid and (dic[elem] != None):
                temp_elem = ''
                if ':' in elem:
                    temp_elem = elem.split(':')[1]
                else:
                    temp_elem = elem
                if isinstance(dic[elem], dict):
                    copy_dic[temp_elem] = {}
                    self._preprocessing(dic[elem], copy_dic[temp_elem])
                elif isinstance(dic[elem], list):
                    copy_dic[temp_elem] = []
                    for i, item in enumerate(dic[elem]):
                        if isinstance(item, dict):
                            temp_item = {}
                            self._preprocessing(item, temp_item)
                            copy_dic[temp_elem].append(temp_item)
                        else:
                            if isinstance(item, str):
                                copy_dic[temp_elem].append(item)
                                done = Pathfinder.__preprocess_values(dic[elem], i, copy_dic[temp_elem], i)
                                if not done:
                                    copy_dic[temp_elem][i] = item
                            elif item is None:
                                pass
                            else:
                                raise Exception("{} inside list".format(type(item)))
                else:
                    done = Pathfinder.__preprocess_values(dic, elem, copy_dic, temp_elem)
                    if not done:
                        copy_dic[temp_elem] = dic[elem]

    @staticmethod
    def __preprocess_values(dic, elem, copy_dic, temp_elem):
        done = False
        if dic[elem] == 'false':
            copy_dic[temp_elem] = 0
            done = True
        elif dic[elem] == 'true':
            copy_dic[temp_elem] = 1
            done = True
        elif re.match("^20[0-9][0-9]-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]).*", dic[elem]) and ('+' in dic[elem]):
            copy_dic[temp_elem] = dic[elem].split('+')[0]
            done = True
        return done

    @staticmethod
    def __fill_ident_dict(ident_dict, schema):
        for ident_elem in schema:
            if '@xmlns:' in ident_elem:
                ident_dict[ident_elem.split(':')[1]] = schema[ident_elem]

    @staticmethod
    def __fill_import_dict(import_dict, schema):
        if 'xs:import' in schema:
            import_sch = schema['xs:import']
            if isinstance(import_sch, list):
                for import_elem in import_sch:
                    import_dict[import_elem['@namespace']] = import_elem['@schemaLocation']
            else:
                import_dict[import_sch['@namespace']] = import_sch['@schemaLocation']

    @staticmethod
    def __make_prefix_dict (xsd_path):
        ident_dict = {}
        import_dict = {}
        prefix_dict = {}
        xsd_files = []
        for file in listdir(xsd_path):
            if '.xsd' in file:
                xsd_files.append(file)
        for file in xsd_files:
            schema = xmltodict.parse(open(xsd_path + file, 'rb'))['xs:schema']
            Pathfinder.__fill_ident_dict(ident_dict, schema)
            Pathfinder.__fill_import_dict(import_dict, schema)
        for prefix in ident_dict:
            if ident_dict[prefix] in import_dict.keys():
                prefix_dict[prefix] = import_dict[ident_dict[prefix]]
        return prefix_dict

    @staticmethod
    def __make_schema_dict(xsd_path):
        pr_dict = Pathfinder.__make_prefix_dict(xsd_path)
        schema_dict = {}
        for prefix in pr_dict:
            schema_dict[prefix] = xmltodict.parse(open(xsd_path + pr_dict[prefix], 'rb'))['xs:schema']
        return schema_dict

    