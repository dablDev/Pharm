from dateutil.parser import parse

class purchaseNumberType:
    "Тип: Номер закупки"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 19), "Length is {}, must be 19".format(len(string))
        self.value = string
        
class hrefType:
    "Тип: Гиперссылка"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 1024)), "Length is {}, must be between 1 and 1024".format(len(string))
        self.value = string
        
class externalIdType:
    "Тип: Внешний идентификатор"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 40)), "Length is {}, must be between 1 and 40".format(len(string))
        self.value = string
        
class spzNumType:
    "Тип: Код по СПЗ"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 11), "Length is {}, must be 11".format(len(string))
        self.value = string
        
class consRegistryNumType:
    "Тип: Код по Сводному реестру"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 8), "Length is {}, must be 8".format(len(string))
        self.value = string

class text10Type:
    "Тип: Текстовое поле 10 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 10)), "Length is {}, must be between 1 and 10".format(len(string))
        self.value = string    
        
class text1000Type:
    "Тип: Текстовое поле 1000 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 1000)), "Length is {}, must be between 1 and 1000".format(len(string))
        self.value = string    

class text100Type:
    "Тип: Текстовое поле 100 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 100)), "Length is {}, must be between 1 and 100".format(len(string))
        self.value = string    
        
class text2000Type:
    "Тип: Текстовое поле 2000 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 2000)), "Length is {}, must be between 1 and 2000".format(len(string))
        self.value = string
        
class text4000Type:
    "Тип: Текстовое поле 4000 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 4000)), "Length is {}, must be between 1 and 4000".format(len(string))
        self.value = string


class text500Type:
    "Тип: Текстовое поле 500 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 500)), "Length is {}, must be between 1 and 500".format(len(string))
        self.value = string

class text200Type:
    "Тип: Текстовое поле 200 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 200)), "Length is {}, must be between 1 and 200".format(len(string))
        self.value = string
        
class text50Type:
    "Тип: Текстовое поле 50 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 50)), "Length is {}, must be between 1 and 50".format(len(string))
        self.value = string

        
class printFormFileType:
    "Тип файла печатной формы"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        type_list = ['pdf', 'docx', 'doc', 'rtf', 'xls', 'xlsx', 'jpeg', 'jpg', 'bmp', 'tif', 'tiff', 'txt', 'zip', 'rar', 'gif', 'csv', 'odp', 'odf', 'ods', 'odt', 'sxc', 'sxw', 'xml']
        assert(string in type_list), 'Invalid type'
        self.value = string
        
class innOrganizationType:
    "Тип: ИНН организации"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 10), "Length is {}, must be 10".format(len(string))
        self.value = string
        
class kppType:
    "Тип: КПП"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 9), "Length is {}, must be 9s".format(len(string))
        self.value = string

class emailType:
    "Тип: Адрес электронной почты"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 256)), "Length is {}, must be between 1 and 256".format(len(string))
        self.value = string
        
class phoneType:
    "Тип: Номер телефона/факса"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 30)), "Length is {}, must be between 1 and 30".format(len(string))
        self.value = string
    
class placingWayCodeType:
    "Тип: Код способа размещения заказа (определения поставщика)"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 7)), "Length is {}, must be between 1 and 7".format(len(string))
        self.value = string

class article15PartsType:
    "Тип: Особенности осуществления закупки в соответствии с ч. 4-6 ст. 15 Закона № 44-ФЗ"

#     P4 - В соответствии с ч. 4 ст. 15 Закона № 44-ФЗ;
#     P5 - В соответствии с ч. 5 ст. 15 Закона № 44-ФЗ;
#     P6 - В соответствии с ч. 6 ст. 15 Закона № 44-ФЗ:
#     P41 - В соответствии с ч. 4.1 ст. 15 Закона № 44-ФЗ.

    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        descr_dict = {'P4': "В соответствии с ч. 4 ст. 15 Закона № 44-ФЗ", 'P5': "В соответствии с ч. 5 ст. 15 Закона № 44-ФЗ", 'P6': "В соответствии с ч. 6 ст. 15 Закона № 44-ФЗ", 'P41': "В соответствии с ч. 4.1 ст. 15 Закона № 44-ФЗ"}
        assert(string in descr_dict), "{} is invalid code".format(string)
        self.value = string
        self.descr = descr_dict[string]
        
class schemeVersionType:
    "Тип: Версия схемы"
    
    def __init__ (self, string):
        version_list = ['1.0', '4.1', '4.2', '4.3', '4.3.100', '4.4', '4.4.2', '4.5', '4.6', '5.0', '5.1', '5.2', '6.0', '6.1', '6.2', '6.2.100', '6.3', '6.4', '7.0', '7.2', '7.3', '7.5', '8.0', '8.1', '8.2', '8.2.100', '8.3', '9.0', '9.1']
        assert(string in version_list), "{} is invalid version".format(string)
        self.value = string

class etpCodeType:
    "Тип: Кодовое наименование электронной площадки"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 20)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string
        
class moneyType:
    "Тип: Сумма"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 21)), "Length is {}, must be between 1 and 21".format(len(string))
        self.value = string

class standardContractNumberType:
    "Номер типового контракта, типовых условий контракта"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 16), "Length is {}, must be 16".format(len(string))
        self.value = string
        
class currencyCodeType:
    "Тип: Код ОКВ"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 3)), "Length is {}, must be between 1 and 3".format(len(string))
        self.value = string
        
class currencyCBRFRef:
    'Ссылка на справочник "Список валют, курс на которые устанавливается ЦБ РФ" (nsiContractCurrencyCBRF) '
    
    def __init__ (self, dic):
        self.code = currencyCodeType(dic['code']) #Код валюты
        if 'name' in dic:
            self.name = text50Type(dic['name']) #Наименование валюты. Игнорируется при приеме.  При передаче заполняется значением из справочника "Список валют, курс на которые устанавливается ЦБ РФ" (nsiContractCurrencyCBRF)
        else:
            self.name = None
        
class countryCodeType:
    "Тип: Цифровой код страны"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 3)), "Length is {}, must be between 1 and 3".format(len(string))
        self.value = string
        
class settlementAccountType:
    "Тип: Расчетный счет"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 20), "Length is {}, must be 20".format(len(string))
        self.value = string

class personalAccountType:
    "Тип: Лицевой счет"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 30)), "Length is {}, must be between 1 and 30".format(len(string))
        self.value = string
        
class bikType:
    "Тип: БИК"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 9), "Length is {}, must be 9".format(len(string))
        self.value = string
    
class guidType:
    "Тип: Глобальный идентификатор"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 36)), "Length is {}, must be between 1 and 36".format(len(string))
        self.value = string

class ikzCodeType:
    "Тип: Индивидуальный код закупки (ИКЗ)"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 36), "Length is {}, must be 36".format(len(string))
        self.value = string

class tenderPlan2017RegNumberType:
    "Тип: Реестровый номер плана-графика с 01.01.2017"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 22), "Length is {}, must be 22".format(len(string))
        self.value = string
        
class kbkType:
    "Тип: КБК"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 20), "Length is {}, must be 20".format(len(string))
        self.value = string
        
class boNumberType:
    "Тип: Номер бюджетного обязательства"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 19)), "Length is {}, must be between 1 and 19".format(len(string))
        self.value = string

class moneyPosNegMaxLengthToPoint18Type:
    "Тип: Cумма c максимальной длиной до точки 18 символов"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 21)), "Length is {}, must be between 1 and 21".format(len(string))
        self.value = string

class ktruDictNameType:
    "Тип КТРУ: Наименование в справочнике"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 500)), "Length is {}, must be between 1 and 500".format(len(string))
        self.value = string
        
class okeiCodeType:
    "Тип: Код ОКЕИ"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 4)), "Length is {}, must be between 1 and 4".format(len(string))
        self.value = string

class ktruCharacteristicValueFormatType:
    "Тип КТРУ: Формат значения характеристики: N - числовой; A - дополнительный"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (string == 'N') or (string == 'A') ), "Invalid value"
        self.value = string

class ktruMinMathNotationType:
    "Тип КТРУ: Математическое обозначение отношения к минимальному значению диапазона"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (string == 'greater') or (string == 'greaterOrEqual') ), "Invalid value"
        self.value = string

class ktruMaxMathNotationType:
    "Тип КТРУ: Математическое обозначение отношения к максимальному значению диапазона"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (string == 'less') or (string == 'lessOrEqual') ), "{} is invalid value".format(string)
        self.value = string

class ktruDictCodeType:
    "Тип КТРУ: Код в справочнике"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 10)), "Length is {}, must be between 1 and 10".format(len(string))
        self.value = string

class ktruCharacteristicTypeType:
    "Тип КТРУ: Тип характеристики позиции КТРУ:1 - качественная, 2 - количественная"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (string == '1') or (string == '2') ), "Invalid value"
        self.value = string

class ktruCharacteristicKindType:
    "Тип КТРУ: Вид характеристики позиции КТРУ:1 - неизменяемая заказчиком, 2 - изменемая заказчиком с выбором одного значения, 3 - изменяемая заказчиком, выбор нескольких значений"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (string == '1') or (string == '2') or (string == '3') ), "Invalid value"
        self.value = string
        
class quantity18p11Type:
    "Тип: Количество с 18 знаками до запятой и 11 знаками после запятой"
    
    def __init__ (self, string):
        self.value = string
        
class drugExternalCodeType:
    "Тип: Уникальный код в справочнике для справочника 'Лекарственные препараты' "
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 50)), "Length is {}, must be between 1 and 50".format(len(string))
        self.value = string
        
class drugNameType:
    "Тип: Наименование для справочника 'Лекарственные препараты'"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 500)), "Length is {}, must be between 1 and 500".format(len(string))
        self.value = string

class drugPackaging1QuantityType:
    "Тип: Количество лекарственных форм в первичной упаковке в справочнике 'Лекарственные препараты'"
    
    def __init__ (self, string):
        self.value = string
        
class drugPackaging2QuantityType:
    'Тип: Количество первичных упаковок во вторичной (потребительской) упаковке в справочнике "Лекарственные препараты"'
    
    def __init__ (self, string):
        self.value = string
        
class drugSumaryPackagingQuantityType:
    'Тип: Количество первичных упаковок во вторичной (потребительской) упаковке в справочнике "Лекарственные препараты"'
    
    def __init__ (self, string):
        self.value = string

class drugChangeReasonRef:
    "Ссылка на справочник: Причины корректировки справочных данных о лекарственных препаратах"
    
    def __init__ (self, dic):
        self.code = text10Type(dic['code']) #Код причины корректировки
        if 'name' in dic:
            self.name = text2000Type(dic['name'])#Наименование причины корректировки. Игнорируется при приеме.  При передаче заполняется значением из справочника "Причины корректировки справочных данных о лекарственных препаратах" (nsiDrugChangeReason)
        else:
            self.name = None
            
class OKEIRef:
    "Ссылка на ОКЕИ"
    
    def __init__ (self, dic):
        self.code = okeiCodeType(dic['code']) #Код
        if 'nationalCode' in dic:
            assert( (len(dic['nationalCode']) >= 1) & (len(dic['nationalCode']) <= 50) ), "Invalid value"
            self.nationalCode = dic['nationalCode'] #Национальное условное обозначение (поле localSymbol в справочнике ОКЕИ (nsiOKEI)). Игнорируется при приеме. автоматически заполняется значением из справочника и выгружается
        else:
            self.nationalCode = None
        
        if 'name' in dic:
            self.name = text1000Type(dic['name']) #Полное наименование единицы измерения (поле fullName  в справочнике ОКЕИ (nsiOKEI)). Игнорируется при приеме. автоматически заполняется значением из справочника и выгружается
        else:
            self.name = None

class NPASt14CodeType:
    "Тип: Код Нормативно-правового акта, регулирующего допуск товаров, работ, услуг в соответствии со ст.14 Закона 44-ФЗ"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 20)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string
        
            
class NPASt14Ref:
    "Ссылка на справочник Нормативно-правовые акты, регулирующие допуск товаров, работ, услуг в соответствии со ст.14 Закона 44-ФЗ"
    
    def __init__ (self, dic):
        self.code = NPASt14CodeType(dic['code']) #Код нормативно-правового акта по справочнику "Нормативно-правовые акты, регулирующие допуск товаров, работ, услуг в соответствии со ст.14 Закона 44-ФЗ" (nsiTRUAdmissionNPA)
        if 'name' in dic:
            self.name = text2000Type(dic['name']) #Наименование нормативно-правового акта.  Игнорируется при приеме. Заполняется  при передаче
        else:
            self.name = None
        
        if 'shortName' in dic:
            self.shortName = text100Type(dic['shortName']) #Краткое наименование нормативно-правового акта.  Игнорируется при приеме. Заполняется  при передаче
        else:
            self.shortName = None
        
class publicDiscussionNumType:
    "Тип: Реестровый номер общественного обсуждения"
    
    def __init__ (self, string):
        assert( (len(string) == 8) or (len(string) == 12) ), "Invalid value"
        self.value = string
        
class publicDiscussionPlaceEnum:
    "Тип: Место проведения общественного обсуждения: E - в разделе «Общественные обсуждения крупных закупок» Официального сайта Единой информационной системы в сфере закупок; F - на форуме Официального сайта Единой информационной системы в сфере закупок"
    
    def __init__ (self, string):
        assert( (string == 'E') or (string == 'F') ), "Invalid value"
        self.value = string
        
class checkResultNumberType:
    "Тип: Реестровый номер результата контроля, сформированный контрольным органом"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 256)), "Length is {}, must be between 1 and 256".format(len(string))
        self.value = string
        
class prescriptionNumberType:
    "Тип: Номер предписания"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 20)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string
    
class authorityType:
    "Тип: Вид органа, возможные значения"
    
#     FA - Федеральная антимонопольная служба;
#     FO - Федеральная служба по оборонному заказу;
#     S - Орган исполнительной власти субъекта РФ;
#     M - Орган местного самоуправления муниципального района, городского округа.

    def __init__ (self, string):
        assert ( (string == 'FA') or (string == 'FO') or (string == 'S') or (string == 'M') ), "Invalid value"
        self.value = string
        
class ktruCodeType:
    "Тип КТРУ: Код позиции"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 25)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string

class versionNumberType:
    "Тип: Номер версии"
    
    def __init__ (self, string):
        self.value = string
        
class journalNumberType:
    "Тип: Номер заявки"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 100)), "Length is {}, must be between 1 and 100".format(len(string))
        self.value = string

class rejectReasonCode:
    "Тип: Код причины для отказа в допуске заявки"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 20)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string
    
class rejectReasonName:
    "Тип: Наименование причины для отказа в допуске заявки"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 500)), "Length is {}, must be between 1 and 500".format(len(string))
        self.value = string
    
class abandonedReasonCode:
    "Тип: Код основания признания торгов несостоявшимися"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 20)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string

class abandonedReasonName:
    "Тип: Наименование основания признания торгов несостоявшимися"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 1000)), "Length is {}, must be between 1 and 1000".format(len(string))
        self.value = string
    
class abandonedReasonObjectName:
    "Тип: Наименование интеграционного объекта в справочнике оснований признания процедуры несостоявшейся"
    
    def __init__(self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 350)), "Length is {}, must be between 1 and 350".format(len(string))
        self.value = string
       