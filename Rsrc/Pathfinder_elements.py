from dateutil.parser import parse

type_dict = {
    # string_types
    'xs:string': 'str',
    'xs:ENTITIES': 'str',
    'xs:ENTITY': 'str',
    'xs:ID': 'str',
    'xs:IDREF': 'str',
    'xs:IDREFS': 'str',
    'xs:language': 'str',
    'xs:Name': 'str',
    'xs:NCName': 'str',
    'xs:NMTOKEN': 'str',
    'xs:NMTOKENS': 'str',
    'xs:normalizedString': 'str',
    'xs:QName': 'str',
    'xs:token': 'str',

    # date_types
    'xs:dateTime': 'parse',
    'xs:date': 'parse',
    'xs:time': 'parse',

    # numeric_types
    'xs:long': 'int',
    'xs:int': 'int',
    'xs:double': 'float',
    'xs:float': 'float',
    'xs:decimal': 'float',
    'xs:byte': 'int',
    'xs:nonNegativeInteger': 'int',
    'xs:integer': 'int',
    'xs:positiveInteger': 'int',
    'xs:short': 'int',
    'xs:negativeInteger': 'int',
    'xs:nonPositiveInteger': 'int',
    'xs:unsignedLong': 'int',
    'xs:unsignedInt': 'int',
    'xs:unsignedShort': 'int',
    'xs:unsignedByte': 'int',

    # miscellaneous_type
    'xs:base64Binary': 'str',
    'xs:boolean': 'bool',
}

set_of_forbidden = [
    'signature',
    '@xmlns',
    'cryptoSigns',
    'schemaLocation',
    'customerSignature',
    'supplierSignature',
    'controlPersonalSignature',
    '@schemeVersion'
]

simple_transition_tags = {
    'xs:complexContent',
    'xs:simpleContent',
    'xs:simpleType',
    'xs:extension',
    'xs:restriction'
}

ignorable_tags = {
    '@name',
    '@nillable',
    '@maxOccurs',
    '@minOccurs',
    '@abstract',
    'xs:annotation',
    'xs:attribute',
    'xs:documentation',
    'xs:pattern',
    'xs:maxLength',
    'xs:minLength',
    'xs:length',
    'xs:enumeration',
    'xs:minInclusive',
    'xs:maxExclusive',
    'xs:totalDigits',
    'xs:fractionDigits',
    'xs:maxInclusive',
    'xs:minExclusive',
    '@fixed',
    '@default',
    'xs:whiteSpace'
}

complex_transition_tags = {
    'xs:complexContent',
    'xs:complexType',
    'xs:choice',
    'xs:sequence',
    '@type',
    '@base',
    'xs:element'
}

xsd_base_types_conversion = {
    'moneyType': 'xs:float',
    'moneyPositiveType': 'xs:float',
    'moneyMaxLengthToPoint18Type': 'xs:float',
    'moneyPosNegMaxLengthToPoint18Type': 'xs:float'
}
