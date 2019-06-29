from Mod import BaseTypes as bt
from Mod import CommonTypes as cmn
from dateutil.parser import parse

class zfcs_documentNumberType:
    "Номер документа"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(str) <= 100), "Length is {}, must be <100".format(len(string))

        
class zfcs_organizationRef:
    "Тип: Ссылка на организацию с учетом кодов по СПЗ и по СвР"
    
    def __init__ (self, dic):
        self.regNum = bt.spzNumType(dic['regNum']) #Код по СПЗ.  В случае если организация идентифицируется по коду СвР, а код СПЗ неизвестен, необходимо заполнить данное поле значением 00000000000, и обязательно указать код СвР
        if 'consRegistryNum' in dic:
            self.consRegistryNum = bt.consRegistryNumType(dic['consRegistryNum']) #Код по Сводному Реестру. Должен быть заполнен в случае, если в поле regNum указано значение 00000000000
        else:
            self.consRegistryNum = None
        
        if 'fullName' in dic:
            self.fullName = bt.text2000Type(dic['fullName']) #Полное наименование. Игнорируется при приеме. При передаче заполняется значением из справочника "Сводный перечень заказчиков (СПЗ)" (nsiOrganizationList)
        else:
            self.fullName = None

            
class zfcs_printFormType:
    "Печатная форма"
    
    def __init__ (self, dic):
        self.url = dic['url']; assert(isinstance(dic['url'], str)); assert(len(dic['url']) <= 1024); #Ссылка для скачивания печатной формы
        dic['signature'] = ''

class zfcs_extPrintFormType:
    "Электронный документ, полученный из внешней системы"
    
    def __init__ (self, dic):
        assert(('content' in dic) or ('url' in dic)), "No content and url"
        if 'content' in dic:
            self.content = dic['content'] #Содержимое файла электронного документа
            self.url = None
        elif 'url' in dic:
            self.url = dic['url']; assert(isinstance(dic['url'], str)); assert(len(dic['url']) <= 1024); #Ссылка для скачивания печатной формы
            self.content = None
        dic['signature'] = ''
        self.fileType = bt.printFormFileType(dic['fileType']) #Тип файла электронного документа
        if 'controlPersonalSignature' in dic:
            dic['controlPersonalSignature'] = ''

            
class zfcs_longTextType:
    "Длинное текстовое поле"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) <= 2000), "Length is {}, must be <2000".format(len(string))
        self.value = string

        
class zfcs_contactPersonType:
    "ФИО"
    
    def __init__ (self, dic):
        self.lastName = dic['lastName']; assert(isinstance(self.lastName, str)); assert( (len(self.lastName) >= 1) & (len(self.lastName) <= 50)) #Фамилия
        self.firstName = dic['firstName']; assert(isinstance(self.firstName, str)); assert( (len(self.firstName) >= 1) & (len(self.firstName) <= 50)) #Имя
        if 'middleName' in dic:
            self.middleName = dic['middleName']; assert(isinstance(self.middleName, str)); assert( (len(self.middleName) >= 1) & (len(self.middleName) <= 50)) #Отчество
        else:
            self.middleName = None
        
        
class zfcs_contactInfoType:
    "Контактная информация"
    
    def __init__ (self, dic):
        self.orgPostAddress = zfcs_longTextType(dic['orgPostAddress']) #Почтовый адрес организации
        self.orgFactAddress = zfcs_longTextType(dic['orgFactAddress']) #Адрес местонахождения организации
        self.contactPerson = zfcs_contactPersonType(dic['contactPerson']) #Ответственное должностное лицо
        self.contactEmail = bt.emailType(dic['contactEMail']) #e-mail адрес контактного лица
        self.contactPhone = bt.phoneType(dic['contactPhone']) #Телефон контактного лица
        if 'contactFax' in dic:
            self.contactFax = bt.phoneType(dic['contactFax']) #Факс контактного лица
        else:
            self.contactFax = None
        if 'addInfo' in dic:
            self.addInfo = zfcs_longTextType(dic['addInfo']) #Дополнительная информация
        else:
            self.addInfo = None
        
        
        
class zfcs_purchaseOrganizationType:
    "Данные организации для печатной формы"
    
    def __init__ (self, dic):
        self.regNum = bt.spzNumType(dic['regNum']) #Код по СПЗ. В случае если организация идентифицируется по коду СвР, а код СПЗ неизвестен, необходимо заполнить данное поле значением 00000000000, и обязательно указать код СвР
        if 'consRegistryNum' in dic:
            self.consRegistryNum = bt.consRegistryNumType(dic['consRegistryNum']) #Код по Сводному Реестру. Должен быть заполнен в случае, если в поле spzCode указано значение 00000000000
        else:
            self.consRegistryNum = None
        
        if 'fullName' in dic:
            self.fullName = zfcs_longTextType(dic['fullName']) #Полное наименование
        else:
            self.fullName = None

        if 'shortName' in dic:
            self.shortName = zfcs_longTextType(dic['shortName']) #Сокращенное наименование
        else:
            self.shortName = None
        
        if 'postAddress' in dic:
            self.postAddress = zfcs_longTextType(dic['postAddress']) #Почтовый адрес организации
        else:
            self.postAddress = None
        
        if 'factAddress' in dic:
            self.factAddress = zfcs_longTextType(dic['factAddress']) #Почтовый адрес организации
        else:
            self.factAddress = None
            
        if 'INN' in dic:
            self.INN = bt.innOrganizationType(dic['INN']) #ИНН организации
        else:
            self.INN = None
            
        if 'KPP' in dic:
            self.KPP = bt.kppType(dic['KPP']) #КПП организации
        else:
            self.KPP = None
            
class zfcs_responsibleRoleType:
    "Роль организации, осуществляющей закупку"
# CU - Заказчик;
# OCU - Заказчик в качестве организатора совместного аукциона;
# RA - Уполномоченный орган;
# ORA- Уполномоченный орган в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ;
# AI - Уполномоченное учреждение;
# OAI- Уполномоченное учреждение в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ;
# OA - Организация, осуществляющая полномочия заказчика на осуществление закупок на основании договора (соглашения);
# OOA- Организация, осуществляющая полномочия заказчика на осуществление закупок на основании договора (соглашения) в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ;
# CS - Заказчик, осуществляющий закупки в соответствии с частью 5 статьи 15 Федерального закона № 44-ФЗ;
# OCS -  Заказчик, осуществляющий закупки в соответствии с частью 5 статьи 15 Федерального закона № 44-ФЗ, в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ;
# CC - Заказчик, осуществляющий закупки в соответствии с Федеральным законом № 44-ФЗ, в связи с неразмещением положения о закупке в соответствии с положениями Федерального закона № 223-ФЗ;
# OCC - Заказчик, осуществляющий закупки в соответствии с Федеральным законом № 44-ФЗ, в связи с неразмещением положения о закупке в соответствии с положениями Федерального закона № 223-ФЗ,
# в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ;
# AU - Заказчик, осуществляющий закупку на проведение обязательного аудита (код AU);
# OAU - Заказчик, осуществляющий закупку на проведение обязательного аудита (код AU), в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ;
# RO - Региональный оператор;
# TKO - Региональный оператор для обращения с ТБО;
# CN - Заказчик, осуществляющий закупки в соответствии с частью 4.1 статьи 15 Федерального закона № 44-ФЗ.
# OCN - Заказчик, осуществляющий закупки в соответствии с частью 4.1 статьи 15 Федерального закона № 44-ФЗ в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ.
            
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        descr_dict = {'CU': "Заказчик", 'OCU': "Заказчик в качестве организатора совместного аукциона", 'RA': "Уполномоченный орган", 'ORA': "Уполномоченный орган в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ", 'AI': "Уполномоченное учреждение", 'OAI': "Уполномоченное учреждение в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ", 'OA': "Организация, осуществляющая полномочия заказчика на осуществление закупок на основании договора (соглашения)", 'OOA': "Организация, осуществляющая полномочия заказчика на осуществление закупок на основании договора (соглашения) в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ", 'CS' : "Заказчик, осуществляющий закупки в соответствии с частью 5 статьи 15 Федерального закона № 44-ФЗ", 'OCS': "Заказчик, осуществляющий закупки в соответствии с частью 5 статьи 15 Федерального закона № 44-ФЗ, в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ", 'CC': "Заказчик, осуществляющий закупки в соответствии с Федеральным законом № 44-ФЗ, в связи с неразмещением положения о закупке в соответствии с положениями Федерального закона № 223-ФЗ", 'OCC': "Заказчик, осуществляющий закупки в соответствии с Федеральным законом № 44-ФЗ, в связи с неразмещением положения о закупке в соответствии с положениями Федерального закона № 223-ФЗ", 'AU': "Заказчик, осуществляющий закупку на проведение обязательного аудита (код AU)", 'OAU': "Заказчик, осуществляющий закупку на проведение обязательного аудита (код AU), в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ", 'RO': "Региональный оператор", 'TKO': "Региональный оператор для обращения с ТБО", 'CN': "Заказчик, осуществляющий закупки в соответствии с частью 4.1 статьи 15 Федерального закона № 44-ФЗ", 'OCN': "Заказчик, осуществляющий закупки в соответствии с частью 4.1 статьи 15 Федерального закона № 44-ФЗ в качестве организатора совместного конкурса (аукциона) согласно ст. 25 №44ФЗ"}
        assert(string in descr_dict), "{} is invalid code".format(string)
        self.value = string
        self.descr = descr_dict[string]
        
class zfcs_placingWayType:
    "Тип: Подспособ определения поставщика"
    
    def __init__ (self, dic):
        self.code = bt.placingWayCodeType(dic['code']) #Код подспособа определения поставщик
        if 'name' in dic:
            self.name = bt.text500Type(dic['name']) #Наименование подспособа определения поставщика.Игнорируется при приеме. При передаче заполняется значением из справочника "Способы размещения заказа (определения поставщика)" (nsiPlacingWay)
        else:
            self.name = None

class zfcs_ETPType:
    "Тип: Ссылка на справочник Электронные площадки"
    
    def __init__ (self, dic):
        self.code = bt.etpCodeType(dic['code']) #Кодовое наименование электронной площадки
        if 'name' in dic:
            self.name = bt.text200Type(dic['name']) #Наименование электронной площадки. Игнорируется при приеме. При передаче заполняется значением из справочника "Справочник: Электронные площадки" (nsiETP)
        else:
            self.name = None
        
        if 'url' in dic:
            self.url = bt.hrefType(dic['url']) #Адрес электронной площадки. Игнорируется при приеме.     При передаче заполняется значением из справочника "Справочник: Электронные площадки" (nsiETP)
        else:
            self.url = None

class zfcs_purchaseProcedureCollectingType:
    "Данные процедуры сбора заявок"
    
    def __init__ (self, dic):
        self.startDate = parse(dic['startDate']) #Дата и время начала подачи заявок
        self.place = zfcs_longTextType(dic['place']) #Место подачи заявок
        self.order = zfcs_longTextType(dic['order']) #Порядок подачи заявок
        self.endDate = parse(dic['endDate']) #Дата и время окончания заявок

class zfcs_purchaseNotificationType:
    "Общая информация об извещении по закупке"
    
    class purchaseResponsible:
        "Информация об организации, осуществляющей закупку"
        
        def __init__ (self, dic):
            self.responsibleOrg = zfcs_purchaseOrganizationType(dic['responsibleOrg']) #Организация, осуществляющая закупку
            self.responsibleRole = zfcs_responsibleRoleType(dic['responsibleRole']) #Роль организации, осуществляющей закупку
            self.responsibleInfo = zfcs_contactInfoType(dic['responsibleInfo']) #Контактная информация
            if 'specializedOrg' in dic:
                self.specializedOrg = zfcs_purchaseOrganizationType(dic['specializedOrg']) #Специализированная организация
            else:
                self.specializedOrg = None

            if 'lastSpecializedOrg' in dic:
                self.lastSpecializedOrg = zfcs_purchaseOrganizationType(dic['lastSpecializedOrg']) #Специализированная организация, последняя осуществившая изменения в проекте извещения (для печатной формы)
            else:
                self.lastSpecializedOrg = None
            

    def __init__ (self, dic):
        if "id" in dic:
            self.id = dic['id'] #Идентификатор документа ЕИС
        else:
            self.id = None
        
        if 'externalId' in dic:
            self.externalId = bt.externalIdType(dic['externalId']) #Внешний идентификатор документа
        else:
            self.externalId = None
        
        if 'purchaseNumber' in dic:
            self.purchaseNumber = bt.purchaseNumberType(dic['purchaseNumber']) #Номер закупки
        else:
            self.purchaseNumber = None
        
        if 'directDate' in dic:
            self.directDate = parse(dic['directDate']) #Дата направления на размещение документа. Игнорируется при приеме. Заполняется автоматически датой направления на размещение текущей версии
        else:
            self.directDate = None
            
        self.docPublishDate = parse(dic['docPublishDate']) #Дата размещения документа. Планируемая или фактическая
        if 'docNumber' in dic:
            self.docNumber = dic['docNumber'] #Номер документа
        else:
            self.docNumber = None
        
        if 'href' in dic:
            self.href = bt.hrefType(dic['href']) #Гиперссылка на опубликованный документ
        else:
            self.href = None
       
        if 'printForm' in dic:
            self.printForm = zfcs_printFormType(dic['printForm']) #Печатная форма документа
        else:
            self.printForm = None
        
        if 'extPrintForm' in dic:
            self.extPrintForm = zfcs_extPrintForm(dic['extPrintForm']) #Электронный документ, полученный из внешней системы
        else:
            self.extPrintForm = None
        self.purchaseObjectInfo = zfcs_longTextType(dic['purchaseObjectInfo']) #Наименование объекта закупки
        if 'isBudgetUnionState' in dic:
            assert( (dic['isBudgetUnionState'] == 'false') or (dic['isBudgetUnionState'] == 'true') ), 'Invalid value'
            self.isBudgetUnionState = dic['isBudgetUnionState'] #Закупка за счет средств бюджета Союзного государства. Принимается только если все заказчики закупки указаны в настройке ЕИС "Настройка перечня организаций, осуществляющих закупки за счет средств союзного государства", иначе игнорируется при приеме
        else:
            self.isBudgetUnionState = None
        
        if 'isGOZ' in dic:
            assert( (dic['isGOZ'] == 'false') or (dic['isGOZ'] == 'true') ), 'Invalid value'
            self.isGOZ = dic['isGOZ'] #Закупка товаров, работ, услуг по государственному оборонному заказу в соответствии с ФЗ № 275-ФЗ от 29 декабря 2012 г. Не может быть задан одновременно с признаком "Закупка за счет средств бюджета Союзного государства" (isBudgetUnionState). Проверяется принадлежность всех Заказчиков к перечню настройки "Настройка дополнительного перечня организаций для ГОЗ" или "Настройка перечня кодов ОКФС для ГОЗ". Игнорируется при приеме, начиная с версии ЕИС 9.0, для извещений предварительного отбора (notificationPO)
        else:
            self.isGOZ = None

        if 'isBBST' in dic:
            assert( (dic['isBBST'] == 'false') or (dic['isBBST'] == 'true') ), 'Invalid value'
            self.isBBST = dic['isBBST'] #Закупка в части заказа на создание, модернизацию, поставку, ремонт, сервисное обслуживание и утилизацию вооружения, военной и специальной техники. Может быть задано, только при указании признака "Закупка товаров, работ, услуг по государственному оборонному заказу в соответствии с ФЗ № 275-ФЗ от 29 декабря 2012 г" (isGOZ), а также если у документа закупки нет связи с позицией плана-графика (в закупке не заполнен ни один блок tenderPlanInfo). Игнорируется при приеме для извещений предварительного отбора (notificationPO)
        else:
            self.isBBST = None
        self.purchaseResponsible = zfcs_purchaseNotificationType.purchaseResponsible(dic['purchaseResponsible']) #Информация об организации, осуществляющей закупку
        self.placingWay = zfcs_placingWayType(dic['placingWay']) #Подспособ определения поставщика
        if 'article15FeaturesInfo' in dic:
            self.article15FeaturesInfo = bt.article15PartsType(dic['article15FeaturesInfo']) #Информация об особенностях осуществления закупки в соответствии с ч. 4-6 ст. 15 Закона № 44-ФЗ
        else:
            self.article15FeaturesInfo = None
        
        if 'contractConclusionOnSt83Ch2' in dic:
            assert( (dic['contractConclusionOnSt83Ch2'] == 'false') or (dic['contractConclusionOnSt83Ch2'] == 'true') ), 'Invalid value'
            self.contractConclusionOnSt83Ch2 = dic['contractConclusionOnSt83Ch2'] #Заключение контракта по статье 83 ч. 2. Игнорируется при приёме, заполняется при выгрузке. Для закупок со способом определения поставщика "Электронный аукцион" если признак не заполнен или заполнен false, то по данной закупке  от электронной площадки в ЕИС передается документ CоntractSign (как и раньше), протоколы ПОК и ППУ формируются на площадке и передаются в ЕИС. Если признак заполнен в true, то по данной закупке будет формироваться проект контракта, документ CоntractSign от площадки в ЕИС не передается, протоколы ПОК и ППУ формируются в ЕИС
        else:
            self.contractConclusionOnSt83Ch2 = None
        
        if 'contractConclusionOnSt83Ch2' in dic:
            assert( (dic['contractConclusionOnSt83Ch2'] == 'false') or (dic['contractConclusionOnSt83Ch2'] == 'true') ), 'Invalid value'
            self.contractConclusionOnSt83Ch2 = dic['contractConclusionOnSt83Ch2']#Заключение контракта по статье 83 ч. 2. Игнорируется при приёме, заполняется при выгрузке. Для закупок со способом определения поставщика "Электронный аукцион" если признак не заполнен или заполнен false, то по данной закупке  от электронной площадки в ЕИС передается документ CоntractSign (как и раньше), протоколы ПОК и ППУ формируются на площадке и передаются в ЕИС. Если признак заполнен в true, то по данной закупке будет формироваться проект контракта, документ CоntractSign от площадки в ЕИС не передается, протоколы ПОК и ППУ формируются в ЕИС
        else:
            self.contractConclusionOnSt83Ch2 = None
        
        if 'okpd2okved2' in dic:
            assert( (dic['okpd2okved2'] == 'false') or (dic['okpd2okved2'] == 'true') ), 'Invalid value'
            self.okpd2okved2 = dic['okpd2okved2'] #Классификация по ОКПД2/ОКВЭД2. Элемент не используется в импорте
        else:
            self.okpd2okved2 = None

        self.schemeVersion = bt.schemeVersionType(dic['@schemeVersion'])
        

class zfcs_currencyRef:
    "Тип: Ссылка на ОКВ"
    
    def __init__ (self, dic):
        self.code = bt.currencyCodeType(dic['code']) #Код валюты
        if 'name' in dic:
            self.name = bt.text50Type(dic['name']) #Наименование валюты. Игнорируется при приеме.  При передаче заполняется значением из справочника "Общероссийский классификатор валют (ОКВ)" (nsiCurrency)
        else:
            self.name = None        

            
class zfcs_countryRef:
    "Ссылка на страну"
    
    def __init__ (self, dic):
        self.countryCode = bt.countryCodeType(dic['countryCode']) #Цифровой код страны
        if 'countryFullName' in dic:
            assert(isinstance(dic['countryFullName'], str)), "Not a string"
            assert(len(dic['countryFullName']) <= 200), "Length is {}, must be <200".format(len(dic['countryFullName']))
            self.countryFullName = dic['countryFullName'] #Полное наименование страны
        else:
            self.countryFullName = None
        
            
            
class zfcs_kladrType:
    "Адрес по КЛАДР"
    
    def __init__ (self, dic):
        assert(isinstance(dic['kladrType'], str)), "Not a string"
        assert(len(dic['kladrType']) == 1), "Length is {}, must be 1".format(len(dic['kladrType']))
        if 'kladrType' in dic:
            self.kladrType = dic['kladrType'] #тип элемента КЛАДР
        else:
            self.kladrType = None
        assert(isinstance(dic['kladrCode'], str)), "Not a string"
        assert(len(dic['kladrCode']) <= 20), "Length is {}, must be <20".format(len(dic['kladrCode']))
        self.kladrCode = dic['kladrCode'] #Код КЛАДР
        if 'fullName' in dic:
            assert(isinstance(dic['fullName'], str)), "Not a string"
            assert(len(dic['fullName']) <= 200), "Length is {}, must be <200".format(len(dic['fullName']))
            self.fullName = dic['fullName'] #Полное наименование
        else:
            self.fullName = None
            
class zfcs_kladrPlacesType:
    "Места доставки ТРУ по КЛАДР"
    
    class kladrPlace:
        "Место доставки товара, выполнения работы или оказания услуги по справочнику КЛАДР"
        
        class noKladrForRegionSettlement:
            "КЛАДР не используется для задания района/города и населенного пункта"
            
            def __init__ (self, dic):
                if 'region' in dic:
                    assert(isinstance(dic['region'], str)), "Not a string"
                    assert(len(dic['region']) <= 100), "Length is {}, must be <100"
                    self.region = dic['region'] #Район/город
                else:
                    self.region = None
                    
                if 'settlement' in dic:
                    assert(isinstance(dic['settlement'], str)), "Not a string"
                    assert(len(dic['settlement']) <= 100), "Length is {}, must be <100"
                    self.settlement = dic['settlement'] #Населенный пункт
                else:
                    self.settlement = None
        
        def __init__ (self, dic):
            if 'kladr' in dic:
                self.kladr = zfcs_kladrType(dic['kladr']) #Код КЛАДР - если поставка в РФ
                self.country = None
            elif 'country' in dic:
                self.kladr = None
                self.country = zfcs_countryRef(dic['country']) #Код страны в ОКСМ - если поставка не в РФ
            else:
                self.kladr = None
                self.country = None
            self.deliveryPlace = zfcs_longTextType(dic['deliveryPlace']) #Место
            if 'noKladrForRegionSettlement' in dic:
                self.noKladrForRegionSettlement = zfcs_kladrPlacesType.kladrPlace.noKladrForRegionSettlement(dic['noKladrForRegionSettlement'])
            else:
                self.noKladrForRegionSettlement = None

    
    def __init__ (self, dic):
        self.kladrPlace = []
        if isinstance(dic['kladrPlace'], list):
            for place in dic['kladrPlace']:
                self.kladrPlace.append(zfcs_kladrPlacesType.kladrPlace(place))
        else:
            self.kladrPlace.append(zfcs_kladrPlacesType.kladrPlace(dic['kladrPlace']))
                

class zfcs_paymentInfoType:
    "Информация о платеже для обеспечения заявки (исполнения контракта) или за предоставление документации"
    
    def __init__ (self, dic):
        self.amount = bt.moneyType(dic['amount']) #Размер обеспечения
        if 'part' in dic:
            assert( (len(dic['part']) >= 1) & (len(dic['part']) <= 4) ), "Number is {}, must be between 0 and 1000".format(dic['part'])
            self.part = dic['part'] #Доля от начальной (максимальной) цены контракта
        else:
            self.part = None
        self.procedureInfo = zfcs_longTextType(dic['procedureInfo']) #Порядок внесения денежных средств в качестве обеспечения заявки (порядок предоставления обеспечения исполнения контракта)
        self.settlementAccount = bt.settlementAccountType(dic['settlementAccount']) #Номер расчётного счёта
        if 'personalAccount' in dic:
            self.personalAccount = bt.personalAccountType(dic['personalAccount']) #Номер лицевого счёта
        else:
            self.personalAccount = None
        self.bik = bt.bikType(dic['bik'])
        
        
class zfcs_attachmentType:
    "Прикрепленный документ"
    
    def __init__ (self, dic):
        if 'publishedContentId' in dic:
            self.publishedContentId = bt.guidType(dic['publishedContentId']) #Уникальный идентификатор контента прикрепленного документа на ЕИС
        else:
            self.publishedContentId = None
        assert(isinstance(dic['fileName'], str)), "Not a string"
        assert(len(dic['fileName']) <= 1024), "Length is {}, must be <1024".format(len(dic['fileName']))
        self.fileName = dic['fileName'] #Имя файла
        if 'fileSize' in dic:
            assert(isinstance(dic['fileSize'], str)), "Not a string"
            assert(len(dic['fileSize']) <= 40), "Length is {}, must be <40".format(len(dic['fileSize']))
            self.fileSize = dic['fileSize'] #Размер файла
        else:
            self.fileSize = None
            
        if 'docDescription' in dic:
            assert(isinstance(dic['docDescription'], str)), "Not a string"
            assert(len(dic['docDescription']) <= 1024), "Length is {}, must be <1024".format(len(dic['docDescription']))
            self.docDescription = dic['docDescription'] #Описание прикрепляемого документа
        else:
            self.docDescription = None
       
        if 'docDate' in dic:
            self.docDate = parse(dic['docDate']) #Дата/время прикрепления документа
        else:
            self.docDate = None
        assert( ('url' in dic) or ('contentId' in dic) or ('content' in dic) ), "No required fields in doc"
        if 'url' in dic:
            assert(isinstance(dic['url'], str)), "Not a string"
            assert(len(dic['url']) <= 1024), "Length is {}, must be <1024".format(len(dic['url']))
            self.url = dic['url'] #Ссылка для скачивания прикрепленного документа. Поле заполняется при передаче документов из ЕИС во внешние системы
            self.contentId = None
            self.content = None
        elif 'contentId' in dic:
            self.url = None
            self.contentId = bt.guidType(dic['contentId']) #Уникальный идентификатор контента прикрепленного документа на ЕИС. Поле contentId или content должно  быть заполнено при приеме в ЕИС документов от  внешних систем
            self.content = None
        elif 'content' in dic:
            self.url = None
            self.contentId = None
            assert(len(dic['content']) >= 1), "Length is {}, must be >1".format(len(dic['content']))
            self.content = dic['content'] #Содержимое файла. Поле contentId или content должно  быть заполнено при приеме в ЕИС документов от  внешних систем
        if 'cryptoSigns' in dic:
            dic['cryptoSigns'] = ''
        
        
class zfcs_attachmentListType:
    "Прикрепленные документы"
    
    def __init__ (self, dic):
        self.attachment = []
        if isinstance(dic['attachment'], list):
            for attachment in dic['attachment']:
                self.attachment.append(zfcs_attachmentType(attachment))
        else:
            self.attachment.append(zfcs_attachmentType(dic['attachment']))

            
class zfcs_tenderPlanNumberType:
    "Реестровый номер плана-графика"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 20)), "Length is {}, must be between 1 and 20".format(len(string))
        self.value = string

        
class zfcs_tenderPlanPositionNumberType:
    "Реестровый номер позиции в плане-графике"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert( (len(string) >= 1) & (len(string) <= 27)), "Length is {}, must be between 1 and 27".format(len(string))
        self.value = string


class zfcs_tenderPlan2017PositionNumberType:
    "Реестровый номер позиции (уникальный реестровый номер закупки) в плане-графике с 01.01.2017"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) <= 28), "Length is {}, must be 28".format(len(string))
        self.value = string
        

class zfcs_purchasePlanPositonExtNumberType:
    "Внешний номер позиции плана закупок (плана-графика)"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 100)), "Length is {}, must be between 1 and 100".format(len(string))
        self.value = string


        
class zfcs_tenderPlanInfoType:
    "Информация о плане-графике"
    
    def __init__ (self, dic):
        assert( ( ('planNumber' in dic) & ( ('positionNumber' in dic) or ('purchase83st544' in dic) )) or ( ('plan2017Number' in dic) & ( ('position2017Number' in dic) or ('position2017ExtNumber' in dic) ))), "No required fields"
        if 'planNumber' in dic:
            self.planNumber = zfcs_tenderPlanNumberType(dic['planNumber']) #Реестровый номер плана-графика
            self.plan2017Number = None
            self.position2017Number = None
            self.position2017ExtNumber = None
            if 'positionNumber' in dic:
                self.positionNumber = zfcs_tenderPlanPositionNumberType(dic['positionNumber']) #Номер позиции в плане-графике     
                self.purchase83st544 = None
            elif 'purchase83st544' in dic:
                assert( (dic['purchase83st544'] == 'false') or (dic['purchase83st544'] == 'true') ), "Invalid value"
                self.purchase83st544 = dic['purchase83st544'] #Итоговая позиция закупки лекарственных препаратов в соответствии с п. 7 ч. 2 ст. 8З
                self.positionNumber = None
        elif 'plan2017Number' in dic:
            self.plan2017Number = bt.tenderPlan2017RegNumberType(dic['plan2017Number']) #Реестровый номер плана-графика с 01.01.2017
            self.planNumber = None
            self.positionNumber = None
            self.purchase83st544 = None
            if 'position2017Number' in dic:
                self.position2017Number = zfcs_tenderPlan2017PositionNumberType(dic['position2017Number']) #Номер позиции в плане-графике с 01.01.2017 (уникальный реестровый номер закупки)
                self.position2017ExtNumber = None
            elif 'position2017ExtNumber' in dic:
                self.position2017ExtNumber = zfcs_purchasePlanPositonExtNumberType(dic['position2017ExtNumber']) #Внешний номер позиции в плане-графике с 01.01.2017
                self.position2017Number = None

                
class zfcs_yearType:
    "Номер года"
    
    def __init__ (self, number):
        assert( (len(number) >= 3) & (len(number) <= 4) ), "{} not a valid number".format(number)
        self.value = number
                

class zfcs_budgetFinancingsType:
    "План исполнения контракта за счет бюджетных средств"
    
    class budgetFinancing:
        "Запись плана исполнения контракта за счет бюджетных средств"
        
        def __init__ (self, dic):
            assert( ('kbkCode' in dic) or ('kbkCode2016' in dic) ), "No required fields"
            if 'kbkCode' in dic:
                self.kbkCode = bt.kbkType(dic['kbkCode']) #Код бюджетной классификации (указывается до 01.01.2016)
                self.kbkCode2016 = None
            elif 'kbkCode2016' in dic:
                self.kbkCode2016 = bt.kbkType(dic['kbkCode']) #Код бюджетной классификации (указывается c 01.01.2016)
                self.kbkCode = None
            self.year = zfcs_yearType(dic['year']) #Год
            if 'sum' in dic:
                self.sum = bt.moneyType(dic['sum']) #Сумма контракта за год
            else:
                self.sum = None
    
    def __init__ (self, dic):
        self.budgetFinancing = []
        if isinstance(dic['budgetFinancing'], list):
            for financing in dic['budgetFinancing']:
                self.budgetFinancing.append(zfcs_budgetFinancingsType.budgetFinancing(financing)) #Запись плана исполнения контракта за счет бюджетных средств
        else:
            self.budgetFinancing.append(zfcs_budgetFinancingsType.budgetFinancing(dic['budgetFinancing']))
        if 'totalSum' in dic:
            self.totalSum = bt.moneyType(dic['totalSum']) #Общая сумма бюджетного финансирования
        else:
            self.totalSum = None

            
class zfcs_kosguType:
    "КОСГУ"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 3), "Length is {}, must be 3".format(len(string))
        self.value = string        
        
class zfcs_kosguType:
    "Код вида расходов (справочник КВР)"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert(len(string) == 3), "Length is {}, must be 3".format(len(string))
        self.value = string        


    
class zfcs_nonBudgetFinancingsType:
    "План исполнения контракта за счет внебюджетных средств"
    
    class nonBudgetFinancing:
        "Запись плана исполнения контракта за счет внебюджетных средств"
        
        def __init__ (self, dic):
            assert( ('kosguCode' in dic) or ('kvrCode' in dic) ), "No required fields"
            if 'kosguCode' in dic:
                self.kosguCode = zfcs_kosguType(dic['kosguCode']) #Код операции сектора государственного управления (указывается до 01.01.2016)
                self.kvrCode = None
            elif 'kvrCode' in dic:
                self.kvrCode = zfcs_KVRCodeType(dic['kvrCode']) #Код вида расходов (указывается с 01.01.2016
                self.kosguCode = None
            self.year = zfcs_yearType(dic['year']) #Год
            if 'sum' in dic:
                self.sum = bt.moneyType(dic['sum']) #Сумма контракта за год
            else:
                self.sum = None
            
            
            
    
    
    def __init__ (self, dic):
        self.nonBudgetFinancing = []
        if isinstance(dic['nonBudgetFinancing'], list):
            for financing in dic['nonBudgetFinancing']:
                self.nonBudgetFinancing.append(zfcs_nonBudgetFinancingsType.nonBudgetFinancing(financing))
        else:
            self.nonBudgetFinancing.append(zfcs_nonBudgetFinancingsType.nonBudgetFinancing(dic['nonBudgetFinancing']))

            
class zfcs_purchasePlanFinanceResourcesType:
    "Финансовое обеспечение закупки для плана закупок"
    
    def __init__ (self, dic):
        if 'total' in dic:
            self.total = bt.moneyPosNegMaxLengthToPoint18Type(dic['total']) #Всего. Значение игнорируется при приеме. автоматически рассчитывается как сумма нижеследующих полей (т.е. total=currentYear+firstYear+secondYear+subsecYears).
        else:
            self.total = None
        
        if 'currentYear' in dic:
            self.currentYear = bt.moneyPosNegMaxLengthToPoint18Type(dic['currentYear']) #Сумма на текущий плановый год
        else:
            self.currentYear = None
           
        if 'firstYear' in dic:
            self.firstYear = bt.moneyPosNegMaxLengthToPoint18Type(dic['firstYear']) #Сумма на первый плановый год
        else:
            self.firstYear = None
            
        if 'secondYear' in dic:
            self.secondYear = bt.moneyPosNegMaxLengthToPoint18Type(dic['secondYear']) #Сумма на второй плановый год
        else:
            self.secondYear = None
            
        if 'subsecYear' in dic:
            self.subsecYear = bt.moneyPosNegMaxLengthToPoint18Type(dic['subsecYear']) #Сумма на последующие годы
        else:
            self.subsecYear = None
            
            
class zfcs_purchaseBOBudgetFinancingType:
    "Тип: Запись плана исполнения контракта за счет бюджетных средств"
    
    def __init__ (self, dic):
        self.KBKCode = bt.kbkType(dic['KBKCode']) #Код бюджетной классификации
        self.KBKYearsInfo = zfcs_purchasePlanFinanceResourcesType(dic['KBKYearsInfo']) #План исполнения контракта
            
            
class zfcs_purchaseBOBudgetFinancingsType:
    "Тип: План оплаты исполнения контракта"
    
    def __init__ (self, dic):
        self.currentYear = zfcs_yearType(dic['currentYear']) #Текущий плановый год
        self.budgetFinancing = []
        if isinstance(dic['budgetFinancing'], list):
            for financing in dic['budgetFinancing']:
                self.budgetFinancing.append(zfcs_purchaseBOBudgetFinancingType(financing)) #Запись плана исполнения контракта за счет бюджетных средств
        else:
            self.budgetFinancing.append(zfcs_purchaseBOBudgetFinancingType(dic['budgetFinancing']))
            
        if 'totalSum' in dic:
            self.totalSum = bt.moneyType(dic['totalSum']) #Общая сумма бюджетного финансирования
        else:
            self.totalSum = None
            
            
class zfcs_purchaseBOInfoType:
    "Тип: Информация о бюджетном обязательстве в требованиях заказчика"
    
    class nonbudgetFinancings:
        "План оплаты исполнения контракта за счет внебюджетных средств"
        # Принимается только для следующих организаций:
        # • СПЗ организации = 09950000002 (ГОСУДАРСТВЕННАЯ КОРПОРАЦИЯ ПО КОСМИЧЕСКОЙ ДЕЯТЕЛЬНОСТИ "РОСКОСМОС");
        # • СПЗ организации = 07731000003 (ГОСУДАРСТВЕННАЯ КОРПОРАЦИЯ ПО АТОМНОЙ ЭНЕРГИИ "РОСАТОМ").
        # Контролируется бизнес-контролем ПРИЗ_АК_0000_0679"

        def __init__(self, dic):
            self.totalSum = bt.moneyType(dic['totalSum']) #Всего оплата за счет внебюджетных средств
    
    def __init__ (self, dic):
        self.BONumber = bt.boNumberType(dic['BONumber']) #Номер принимаемого бюджетного обязательства
        self.BODate = parse(dic['BODate']) #Дата принимаемого бюджетного обязательства
        if 'inputBOFlag' in dic:
            assert( (dic['inputBOFlag'] == 'auto') or (dic['inputBOFlag'] == 'manual') )
            self.inputBOFlag = dic['inputBOFlag']#Признак автоматического/ручного ввода информации о бюджетном обязательстве:
# auto - автоматический ввод;
# manual - ручной ввод.
        else:
            self.inputBOFlag = None
            
        if 'budgetFinancings' in dic:
            self.budgetFinancings = zfcs_purchaseBOBudgetFinancingsType(dic['budgetFinancings']) #Блок «План оплаты исполнения контракта» 
# Если признак ручного ввода для данной организзации в ЕИС = FALSE, то автоматически заполняется при передаче сведения на основании связанного БО.
# Если признак ручного ввода = TRUE, то в ЕИС принимается содержимое блока
        else:
            self.budgetFinancings = None
        
        if 'nonbudgetFinancings' in dic:
            self.nonbudgetFinancings = zfcs_purchaseBOInfoType.nonbudgetFinancings(dic['nonbudgetFinancings'])
        else:
            self.nonbudgetFinancings = None
        if 'BORegistered' in dic:
            assert( (dic['BORegistered'] == 'true') or (dic['BORegistered'] == 'false')), "Invalid value"
            self.BORegistered = dic['BORegistered']
        else:
            self.BORegistered = None
            
        
class zfcs_longText4000MinType:
    "Текстовое поле размерности 4000 с ограничением минимального значения"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 4000)), "Length is {}, must be between 1 and 4000".format(len(string))
        self.value = string

        
class zfcs_OKPDRef:
    "Ссылка на ОКПД"
    
    def __init__ (self, dic):
        assert(isinstance(dic['code'], str)), "Not a string"
        assert((len(dic['code']) >= 1) & (len(dic['code']) <= 20)), "Length is {}, must be between 1 and 20".format(len(dic['code']))
        self.code = dic['code'] #Код товара, работы или услуги
        if 'name' in dic:
            assert(isinstance(dic['name'], str)), "Not a string"
            assert((len(dic['name']) >= 1) & (len(dic['name']) <= 500)), "Length is {}, must be between 1 and 500".format(len(dic['name']))
            self.name = dic['name'] #Наименование товара, работы или услуги
        else:
            self.name = None

            
class zfcs_OKEIRef:
    "Тип: Ссылка на ОКЕИ"
    
    def __init__ (self, dic):
        self.code = bt.okeiCodeType(dic['code']) #Код
        if 'name' in dic:
            self.name = bt.text1000Type(dic['name']) #Наименование товара, работы или услуги
        else:
            self.name = None
        
class zfcs_KTRURef:
    "Тип: Ссылка на КТРУ"
    
    def __init__ (self, dic):
        self.code = bt.ktruCodeType(dic['code']) #Код товара, работы или услуги в справочнике Каталог товаров, работ, услуг (КТРУ) (nsiKTRU)
        if 'name' in dic:
            self.name = bt.text2000Type(dic['name'])
        else:
            self.name = None
        
        if 'versionId' in dic:
            self.versionId = dic['versionId'] #Идентификатор версии позиции. Не используется, добавлено на развитие
        else:
            self.versionId = None
            
class zfcs_KTRUCharacteristicValueType:
    "Тип КТРУ: Значение характеристики позиции КТРУ"
    
    class rangeSet:
        "Набор диапазонов значений характеристик"
        
        class valueRange:
            "Диапазон значений"
            
            def __init__ (self, dic):
                if 'minMathNotation' in dic:
                    self.minMathNotation = bt.ktruMinMathNotationType(dic['minMathNotation']) #Математическое обозначение отношения к минимальному значению диапазона
                else:
                    self.minMathNotation = None
                
                if 'min' in dic:
                    self.min = dic['min'] #Минимальное значение диапазона
                else:
                    self.min = None
                
                if 'maxMathNotation' in dic:
                    self.maxMathNotation = bt.ktruMaxMathNotationType(dic['maxMathNotation']) #Математическое обозначение отношения к максимальному значению диапазона
                else:
                    self.maxMathNotation = None
                
                if 'max' in dic:
                    self.max = dic['max'] #Максимальное значение диапазона
                else:
                    self.max = None
        
        def __init__(self, dic):
            self.valueRange = zfcs_KTRUCharacteristicValueType.rangeSet.valueRange(dic['valueRange']) #Диапазон значений
    
    class valueSet:
        "Набор конкретных значений характеристики"
        
        def __init__ (self, dic):
            self.concreteValue = dic['concreteValue'] #Конкретное значение
    
    def __init__ (self, dic):
        assert( ('qualityDescription' in dic) or ('OKEI' in dic) or ('valueFormat' in dic) or ('rangeSet' in dic) or ('valueSet' in dic) ), print(dic.keys())
        if 'qualityDecription' in dic:
            self.qualityDecription = bt.ktruDictNameType(dic['quailityDescription']) #Текстовое описание значения качественной характеристики
            self.OKEI = None
            self.valueFormat = None
            self.rangeSet = None
            self.valueSet = None
        elif ('OKEI' in dic) or ('valueFormat' in dic):            
            self.qualityDescription = None
            if 'OKEI' in dic:
                self.OKEI = zfcs_OKEIRef(dic['OKEI']) #Единица измерения. Ссылка на классификатор ОКЕИ (nsiOKEI). Допустимо указание как постоянных, так и временных единиц измерения (для которых установлено поле isTemporaryForKTRU в выгрузке справочника nsiOKEI).  Игнорируется при приеме для извещений предварительного отбора, начиная с версии 9.0
            else:
                self.OKEI = None
                
            if 'valueFormat' in dic:
                self.valueFormat = bt.ktruCharacteristicValueFormatType(dic['valueFormat']) #Формат значения характеристики:N-числовой; A-дополнительный
            else:
                self.valueFormat = None
            assert( ('rangeSet' in dic) or ('valueSet' in dic) ), "No required fields"
            if 'rangeSet' in dic:
                self.rangeSet = zfcs_KTRUCharacteristicValueType.rangeSet(dic['rangeSet'])
                self.valueSet = None
            elif 'valueSet' in dic:
                self.valueSet = zfcs_KTRUCharacteristicValueType.valueSet(dic['valueSet'])
                self.rangeSet = None            
            
class zfcs_tenderPlan2017ManualKtruCharacteristicType:
    "Тип: Характеристика товаров, работ, услуг для ввода в текстовой форме"
    
    class values:
        "Допустимые значения характеристики"
        
        def __init__ (self, dic):
            self.value = []
            if isinstance(dic['value'], list):
                for value in dic['value']:
                    self.value.append(zfcs_KTRUCharacteristicValueType(value)) #Допустимое значение характеристики
            else:
                self.value.append(zfcs_KTRUCharacteristicValueType(dic['value'])) 
    
    def __init__ (self, dic):
        self.name = bt.ktruDictNameType(dic['name']) #Наименование характеристики
        self.type = bt.ktruCharacteristicTypeType(dic['type']) #Тип характеристики: 1 - качественная;  2 - количественная
        self.values = zfcs_tenderPlan2017ManualKtruCharacteristicType.values(dic['values']) #Допустимые значения характеристики
         
            
class zfcs_longTextMinType:
    "Длинное текстовое поле с ограничением минимального значения"
    
    def __init__ (self, string):
        assert(isinstance(string, str)), "Not a string"
        assert((len(string) >= 1) & (len(string) <= 2000)), "Length is {}, must be between 1 and 2000".format(len(string))
        self.value = string
        

class zfcs_tenderPlan2017RefKtruCharacteristicType:
    "Тип: Характеристика товаров, работ, услуг для ввода из справочника"
    
    class values:
        "Допустимые значения характеристики позиции КТРУ. "
        
        def __init__ (self, dic):
            self.value = []
            if isinstance(dic['value'], list):
                for value in dic['value']:
                    self.value.append(zfcs_KTRUCharacteristicValueType(value))
            else:
                self.value.append(dic['value'])
                
    
    def __init__ (self, dic):
        if 'code' in dic:
            self.code = bt.ktruDictCodeType(dic['code']) #Код характеристики. Игнорируется при приеме.
        else:
            self.code = None
        
        if 'name' in dic:
            self.name = bt.ktruDictNameType(dic['name']) #Наименование характеристики. Контролируется обязательность заполнения. Является полем, идентифицирующим характеристику
        else:
            self.name = None
            
        if 'type' in dic:
            self.type = bt.ktruCharacteristicTypeType(dic['type']) #Тип характеристики: 1 - качественная;  2 - количественная
        else:
            self.type = None
            
        if 'kind' in dic:
            self.kind = bt.ktruCharacteristicKindType(dic['kind']) #Вид характеристики позиции КТРУ
        else:
            self.kind = None
        
        if 'values' in dic:
            self.values = zfcs_tenderPlan2017RefKtruCharacteristicType.values(dic['values'])
        else:
            self.values = None
            
class zfcs_MNNInfoType:
    "Тип: Международное, группировочное или химическое наименование лекарственного препарата (МНН)"
    
    def __init__ (self, dic):
        self.MNNExternalCode = bt.drugExternalCodeType(dic['MNNExternalCode']) #Уникальный внешний код МНН по справочнику "Лекарственные препараты" (поле MNNInfo\MNNExternalCode документа nsiFarmDrugDictionary). При приеме контролируется наличие в справочнике "Лекарственные препараты" ЕИС МНН с таким кодом
        if 'MNNName' in dic:
            self.MNNName = bt.drugNameType(dic['MNNName']) #Наименование МНН. Игнорируется при приеме, автоматически заполняется при передаче из справочника "Лекарственные препараты" (поле MNNInfo\MNNName документа nsiFarmDrugDictionary)
        else:
            self.MNNName = None

class zfcs_tradeInfoType:
    "Тип: Торговое наименование (ТН) лекарственного препарата"
    
    def __init__ (self, dic):
        self.positionTradeNameExternalCode = bt.drugExternalCodeType(dic['positionTradeNameExternalCode']) #Уникальный внешний код лекарственного препарата по справочнику "Лекарственные препараты"
        if 'tradeName' in dic:
            self.tradeName = bt.drugNameType(dic['tradeName']) #Торговое наименование (ТН) препарата по справочнику "Лекарственные препараты" (nsiFarmDrugDictionary)
        else:
            self.tradeName = None
            
            
class zfcs_drugInfoType:
    "Тип: Сведения о МНН, ТН, лекарственной форме и дозировке"
    
    class medicamentalFormInfo:
        "Лекарственная форма. Игнорируется при приеме, автоматически заполняется при передаче по справочнику 'Лекарственные препараты'"
        
        def __init__ (self, dic):
            self.medicamentalFormName = bt.drugNameType(dic['medicamentalFormName']) #Наименование лекарственной формы по справочнику "Лекарственные препараты" (nsiFarmDrugDictionary) (поле MNNsInfo\MNNInfo\medicamentalFormInfo\medicamentalFormName)
            
    class dosageInfo:
        "Дозировка. Игнорируется при приеме, автоматически заполняется при передаче по справочнику 'Лекарственные препараты'"
        
        def __init__ (self, dic):
            self.dosageGRLSValue = bt.drugNameType(dic['dosageGRLSValue']) #Полная форма дозировки по справочнику   "Лекарственные препараты" (nsiFarmDrugDictionary) (поле MNNsInfo\MNNInfo\dosagesInfo\dosageInfo\dosageGRLSValue )
            self.dosageUserOKEI = zfcs_OKEIRef(dic['dosageUserOKEI']) #Потребительская единица  измерения дозировки по справочнику  "Лекарственные препараты" (nsiFarmDrugDictionary) (блок MNNsInfo\MNNInfo\dosagesInfo\dosageInfo\dosageUser\ dosageUserOKEI). Ссылка на классификатор ОКЕИ (nsiOKEI)
    
    class packagingInfo:
        "Сведения об упаковке. В  случае заполнения блока mustSpecifyDrugPackage при приеме контролируется заполненность блока packagingInfo во всех  вариантах поставки лекарственных препаратов"
        
        def __init__ (self, dic):
            self.packaging1Quantity = bt.drugPackaging1QuantityType(dic['packaging1Quantity']) #Количество лекарственных форм в первичной упаковке.
            self.packaging2Quantity = bt.drugPackaging2QuantityType(dic['packaging2Quantity']) #Количество первичных упаковок во вторичной (потребительской) упаковке
            self.sumaryPackagingQuantity = bt.drugSumaryPackagingQuantityType(dic['sumaryPackagingQuantity']) #Количество лекарственных форм во вторичной (потребительской) упаковке. Игнорируется при приеме, автоматически рассчитывается как произведение packaging1Quantity*packaging2Quantity
            
            
    
    def __init__ (self, dic):
        self.MNNInfo = zfcs_MNNInfoType(dic['MNNInfo']) #Международное, группировочное или химическое наименование лекарственного препарата (МНН). При приеме контролируется принадлежность каждого из набора МНН лекарственных препаратов к одному и тому же списку МНН (т.е. МНН в списке должны иметь одни и те же наименования) 
        if 'tradeInfo' in dic:
            self.tradeInfo = []
            if isinstance(dic['tradeInfo'], list):
                for info in dic['tradeInfo']:
                    self.tradeInfo.append(zfcs_tradeInfoType(info)) #Торговое наименование (ТН) лекарственного препарата
            else:
                self.tradeInfo.append(zfcs_tradeInfoType(dic['tradeInfo']))
        else:
            self.tradeInfo = None
            
        if 'medicamentalFormInfo' in dic:
            self.medicamentalFormInfo = zfcs_drugInfoType.medicamentalFormInfo(dic['medicamentalFormInfo']) #Лекарственная форма
        else:
            self.medicamentalFormInfo = None
        
        if 'dosageInfo' in dic:
            self.dosageInfo = zfcs_drugInfoType.dosageInfo(dic['dosageInfo']) #Дозировка
        else:
            self.dosageInfo = None
        
        if 'packagingInfo' in dic:
            self.packagingInfo = zfcs_drugInfoType.packagingInfo(dic['packagingInfo']) #Сведения об упаковке
        else:
            self.packagingInfo = None
            
        if 'manualUserOkei' in dic:
            self.manualUserOkei = zfcs_OKEIRef(dic['manualUserOkei']) #Единица измерения товара, введенная вручную
        else:
            self.manualUserOkei = None
            
        if 'basicUnit' in dic:
            assert( (dic['basicUnit'] == 'true') or (dic['basicUnit'] == 'false') ), "Invalid value"
            self.basicUnit = dic['basicUnit']
        else:
            self.basicUnit = None

class zfcs_contract_OKEIType: #original name: zfcs_contract.OKEIType
    "Тип: Ссылка на ОКЕИ в Реестре контрактов"
    
    def __init__ (self, dic):
        self.code = bt.okeiCodeType(dic['code']) #Код
        if 'nationalCode' in dic:
            self.nationalCode = bt.text50Type(dic['nationalCode']) #Национальное условное обозначение (поле localSymbol в справочнике ОКЕИ (nsiOKEI)). Игнорируется при приеме. автоматически заполняется значением из справочника и выгружается
        else:
            self.nationalCode = None
        
        if 'fullName' in dic:
            self.fullName = bt.text1000Type(dic['fullName']) #Полное наименование единицы измерения (поле fullName  в справочнике ОКЕИ (nsiOKEI)). Игнорируется при приеме. автоматически заполняется значением из справочника и выгружается
        else:
            self.fullName = None
            
class zfcs_drugInfoUsingTextFormType:
    "Тип: Сведения о МНН, ТН, лекарственной форме и дозировке в случае когда информация о лекарственных препаратах формируется в текстовой форме"
    
    class MNNInfo:
        "Международное, группировочное или химическое наименование лекарственного препарата (МНН). При приеме контрролируется, что МНН в списке лекарственных препаратов  должны иметь одни и те же наименования"
        
        def __init__ (self, dic):
            self.MNNName = bt.drugNameType(dic['MNNName']) #Наименование МНН
            if 'drugChangeInfo' in dic:
                self.drugChangeInfo = cmn.drugChangeInfoType(dic['drugChangeInfoType']) #Информация, указываемая при ручном изменении лекарственного препарата
            else:
                self.drugChangeInfo = None
            
    class tradeInfo:
        "Торговое наименование (ТН) лекарственного препарата. Бизнес-контролем проверяется, что блок может быть заполнен только в случае если способ определения поставщика по закупке - «Закупка у единственного поставщика (подрядчика, исполнителя)»"
        
        def __init__ (self, dic):
            self.tradeName = bt.drugNameType(dic['tradeName']) #Торговое наименование (ТН) препарата
            if 'drugChangeInfo' in dic:
                self.drugChangeInfo = cmn.drugChangeInfoType(dic['drugChangeInfo']) #Информация, указываемая при ручном изменении лекарственного препарата
            else:
                self.drugChangeInfo = None
                
    class medicamentalFormInfo:
        "Лекарственная форма"
        
        def __init__ (self, dic):
            self.medicamentalFormName = bt.drugNameType(dic['medicamentalFormName']) #Наименование лекарственной формы
            
    class dosageInfo:
        "Дозировка"
        
        def __init__ (self, dic):
            self.dosageGRLSValue = bt.drugNameType(dic['dosageGRLSValue']) #Полная форма дозировки
            
    class packagingInfo:
        "Сведения об упаковке. В  случае заполнения блока mustSpecifyDrugPackage при приеме контролируется заполненность блока packagingInfo во всех  вариантах поставки лекарственных препаратов"
        
        def __init__ (self, dic):
            self.packaging1Quantity = bt.drugPackaging1QuantityType(dic['packaging1Quantity']) #Количество лекарственных форм в первичной упаковке.
            self.packaging2Quantity = bt.drugPackaging2QuantityType(dic['packaging2Quantity']) #Количество первичных упаковок во вторичной (потребительской) упаковке
            self.sumaryPackagingQuantity = bt.drugSumaryPackagingQuantityType(dic['sumaryPackagingQuantity']) #Количество лекарственных форм во вторичной (потребительской) упаковке. Игнорируется при приеме, автоматически рассчитывается как произведение packaging1Quantity*packaging2Quantity
    
                
    
    def __init__(self, dic):
        self.MNNInfo = zfcs_drugInfoUsingTextFormType.MNNInfo(dic['MNNInfo']) #Международное, группировочное или химическое наименование лекарственного препарата (МНН)
        if 'tradeInfo' in dic:
            self.tradeInfo = zfcs_drugInfoUsingTextFormType.tradeInfo(dic['tradeInfo']) #Торговое наименование (ТН) лекарственного препарата
        else:
            self.tradeInfo = None
            
        self.medicamentalFormInfo = zfcs_drugInfoUsingTextFormType.medicamentalFormInfo(dic['medicamentalFormInfo']) #Лекарственная форма
        self.dosageInfo = zfcs_drugInfoUsingTextFormType.dosageInfo(dic['dosageInfo']) #Дозировка
        if 'packagingInfo' in dic:
            self.packagingInfo = zfcs_drugInfoUsingTextFormType.packagingInfo(dic['packagingInfo']) #Сведения об упаковке
        else:
            self.packagingInfo = None
            
        self.manualUserOKEI = bt.OKEIRef(dic['manualUserOKEI']) #Единица измерения товара
        if 'drugChangeInfo' in dic: 
            self.drugChangeInfo = cmn.drugChangeInfoType(dic['drugChangeInfo']) #Информация, указываемая при ручном изменении лекарственного препарата
        else:
            self.drugChangeInfo = None
            
        if 'basicUnit' in dic:
            assert( (dic['basicUnit'] == 'true') or (dic['basicUnit'] == 'false') ), "Invalid value"
            self.basicUnit = dic['basicUnit']
        else:
            self.basicUnit = None
        
            
class zfcs_purchaseDrugPurchaseObjectsInfoType:
    "Тип: Сведения об объектах закупки в том случае, когда объектами закупки являются лекарственные препараты (ПРИЗ)"
    
    class drugPurchaseObjectInfo:
        "Сведения об объекте закупки в том случае, когда объектом закупки является лекарственный препарат"
        
        class objectInfoUsingReferenceInfo:
            "Информация о вариантах поставки лекарственных препаратов формируется с использованием справочной информации (не в текстовой форме)"
            
            class drugsInfo:
                "Сведения о вариантах поставки лекарственных препаратов"
                
                class drugInfo(zfcs_drugInfoType):
                    "Сведения о варианте поставки лекарственного препарата"

                    def __init__ (self, dic):
                        zfcs_drugInfoType.__init__(self, dic)
                        self.drugQuantity = bt.quantity18p11Type(dic['drugQuantity']) #Количество (объем) закупаемого лекарственного препарата
                def __init__ (self, dic):
                    self.drugInfo = []
                    if isinstance(dic['drugInfo'], list):
                        for drug in dic['drugInfo']:
                            self.drugInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingReferenceInfo.drugsInfo.drugInfo(drug))
                    else:
                        self.drugInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingReferenceInfo.drugsInfo.drugInfo(dic['drugInfo']))
                    
                    
            class mustSpecifyDrugPackage:
                "Необходимо указание сведений об упаковке закупаемого лекарственного препарата. В случае указания блока контролируется заполненность блока packagingInfo во всех  вариантах поставки лекарственных препаратов"
                
                def __init__ (self, dic):
                    self.specifyDrugPackageReason = bt.text4000Type(dic['specifyDrugPackageReason']) #Обоснование необходимости указания сведений об упаковке лекарственного препарата
            
            def __init__ (self, dic):
                self.drugsInfo = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingReferenceInfo.drugsInfo(dic['drugsInfo']) #Сведения о вариантах поставки лекарственных препаратов
                if 'mustSpecifyDrugPackage' in dic:
                    self.mustSpecifyDrugPackage = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingReferenceInfo.mustSpecifyDrugPackage(dic['mustSpecifyDrugPackage']) #Необходимо указание сведений об упаковке закупаемого лекарственного препарата. В случае указания блока контролируется заполненность блока packagingInfo во всех  вариантах поставки лекарственных препаратов
                else:
                    self.mustSpecifyDrugPackage = None
                
        class objectInfoUsingTextForm:
            "Информация о вариантах поставки лекарственных препаратов  формируется в текстовой форме"
            
            class drugsInfo:
                "Сведения о вариантах поставки лекарственных препаратов"

                class drugInfo(zfcs_drugInfoUsingTextFormType):
                    "Сведения о варианте поставки лекарственного препарата"

                    def __init__ (self, dic):
                        zfcs_drugInfoUsingTextFormType.__init__(self, dic)
                        self.drugQuantity = bt.quantity18p11Type(dic['drugQuantity']) #Количество (объем) закупаемого лекарственного препарата
                def __init__ (self, dic):
                    self.drugInfo = []
                    if isinstance(dic['drugInfo'], list):
                        for drug in dic['drugInfo']:
                            self.drugInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingTextForm.drugsInfo.drugInfo(drug))
                    else:
                        self.drugInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingTextForm.drugsInfo.drugInfo(dic['drugInfo']))
                    
                    
                    
            class mustSpecifyDrugPackage:
                "Необходимо указание сведений об упаковке закупаемого лекарственного препарата. В случае указания блока контролируется заполненность блока packagingInfo во всех  вариантах поставки лекарственных препаратов"
                
                def __init__ (self, dic):
                    self.specifyDrugPackageReason = bt.text4000Type(dic['specifyDrugPackageReason']) #Обоснование необходимости указания сведений об упаковке лекарственного препарата
 
            
            def __init__ (self, dic):
                self.drugsInfo = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingTextForm.drugsInfo(dic['drugsInfo']) #Сведения о вариантах поставки лекарственных препаратов
                if 'mustSpecifyDrugPackage' in dic:
                    self.mustSpecifyDrugPackage = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingTextForm.mustSpecifyDrugPackage(dic['mustSpecifyDrugPackage']) #Необходимо указание сведений об упаковке закупаемого лекарственного препарата. В случае указания блока контролируется заполненность блока packagingInfo во всех  вариантах поставки лекарственных препаратов
                else:
                    self.mustSpecifyDrugPackage = None
                
        class drugQuantityCustomersInfo:
            "Количество (объем) закупаемого лекарственного препарата в разбивке по заказчикам в основном варианте поставки. Поле total в составе блока рассчитывается автоматически"
            
            class drugQuantityCustomerInfo:
                "Количество (объем) закупаемого лекарственного препарата для заказчика"
                
                def __init__ (self, dic):
                    self.customer = zfcs_organizationRef(dic['customer']) #Организация заказчика
                    self.quantity = bt.quantity18p11Type(dic['quantity']) #Количество
                
            
            def __init__ (self, dic):
                self.drugQuantityCustomerInfo = []
                if isinstance(dic['drugQuantityCustomerInfo'], list):
                    for drug in dic['drugQuantityCustomerInfo']:
                        self.drugQuantityCustomerInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.drugQuantityCustomersInfo.drugQuantityCustomerInfo(drug))
                else:
                    self.drugQuantityCustomerInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.drugQuantityCustomersInfo.drugQuantityCustomerInfo(dic['drugQuantityCustomerInfo']))
                if 'total' in dic:
                    self.total = bt.quantity18p11Type(dic['total']) #Всего. Значение игнорируется при приеме. автоматически рассчитывается как сумма количества по всем заказчикам.
                else:
                    self.total = None
        
        
        def __init__ (self, dic):
            assert( ('objectInfoUsingReferenceInfo' in dic) or ('objectInfoUsingTextForm' in dic) ), "No required fields"
            if 'objectInfoUsingReferenceInfo' in dic:
                self.objectInfoUsingReferenceInfo = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingReferenceInfo(dic['objectInfoUsingReferenceInfo'])
                self.objectInfoUsingTextForm = None
            elif 'objectInfoUsingTextForm' in dic:
                self.objectInfoUsingTextForm = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.objectInfoUsingTextForm(dic['objectInfoUsingTextForm'])
                self.objectInfoUsingReferenceInfo = None
            if 'isZNVLP' in dic:
                assert( (dic['isZNVLP'] == 'true') or (dic['isZNVLP'] == 'false') ), "Invalid value"
                self.isZNVLP = dic['isZNVLP'] #Признак включения в реестр жизненно необходимые и важнейших лекарственных препаратов (ЖНВЛП)  для основного варианта поставки
            else:
                self.isZNVLP = None
            self.drugQuantityCustomersInfo = zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo.drugQuantityCustomersInfo(dic['drugQuantityCustomersInfo']) #Количество (объем) закупаемого лекарственного препарата в разбивке по заказчикам в основном варианте поставки. Поле total в составе блока рассчитывается автоматически
            self.pricePerUnit = bt.moneyType(dic['pricePerUnit']) #Цена за единицу в основном варианте поставки
            self.positionPrice = bt.moneyType(dic['positionPrice']) #Стоимость позиции в основном варианте поставки
            
    
    def __init__ (self, dic):
        self.drugPurchaseObjectInfo = []
        if isinstance(dic['drugPurchaseObjectInfo'], list):
            for drug in dic['drugPurchaseObjectInfo']:
                self.drugPurchaseObjectInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo(drug))
        else:
            self.drugPurchaseObjectInfo.append(zfcs_purchaseDrugPurchaseObjectsInfoType.drugPurchaseObjectInfo(dic['drugPurchaseObjectInfo']))
        if 'total' in dic:
            self.total = bt.moneyType(dic['total']) #Всего. Значение игнорируется при приеме. автоматически рассчитывается как сумма стоимости позиций (positionPrice) по всем лекарственным препаратам
        else:
            self.total = None
            
class zfcs_preferenseType:
    "Тип: Преимущество для участников"
    
    def __init__ (self, dic):
        assert( ('code' in dic) or ('shortName' in dic) ), "No required fields"
        if 'code' in dic:
            self.code = dic['code'] #Код преимущества. Устарело, не применяется, оставлено для обратной совместимости схем
            self.shortName = None
        elif 'shortName' in dic:
            assert( (len(dic['shortName']) >= 1) & (len(dic['shortName']) <= 20) ), "Invalid value"
            self.shortName = dic['shortName'] #Символьный код преимущества. Символьный бизнес-код, по которому определяется ссылка на запись справочника "Требования (преимущества, ограничения)" (nsiPurchasePreferences)
            self.code = None
            
        if 'name' in dic:
            assert(len(dic['name']) <= 450), "Invalid value"
            self.name = dic['name'] #Наименование премущества. Игнорируется приеме. Заполняется  при передаче
        else:
            self.name = None
            
        if 'prefValue' in dic:
            self.prefValue = dic['prefValue'] #Величина преимущества
        else:
            self.prefValue = None
        
class zfcs_requirementType:
    "Тип: Требование к участникам"
    
    def __init__ (self, dic):
        assert( ('code' in dic) or ('shortName' in dic) ), "No required fields"
        if 'code' in dic:
            self.code = dic['code'] #Код преимущества. Устарело, не применяется, оставлено для обратной совместимости схем
            self.shortName = None
        elif 'shortName' in dic:
            assert( (len(dic['shortName']) >= 1) & (len(dic['shortName']) <= 20) ), "Invalid value"
            self.shortName = dic['shortName'] #Символьный код требования. Символьный бизнес-код, по которому определяется ссылка на запись справочника "Требования (преимущества, ограничения)" (nsiPurchasePreferences)
            self.code = None
            
        if 'name' in dic:
            self.name = zfcs_longTextType(dic['name']) #Наименование требования. Игнорируется при приеме. Заполняется  при передаче
        else:
            self.name = None
            
        if 'content' in dic:
            assert( (len(dic['content']) >= 1) & (len(dic['content']) <= 4000) ), "Invalid value"
            self.content = dic['content'] #Содержание требования
        else:
            self.content = None
            
class zfcs_restrictionType:
    "Тип: Ограничение для участников"
    
    def __init__ (self, dic):
        assert( (len(dic['shortName']) >= 1) & (len(dic['shortName']) <= 20) ), "Invalid value"
        self.shortName = dic['shortName']
        if 'name' in dic:
            self.name = zfcs_longTextType(dic['name']) #Наименование ограничения.  Игнорируется при приеме. Заполняется  при передаче
        else:
            self.name = None
        if 'content' in dic:
            self.content = bt.text4000Type(dic['content']) #Содержание ограничения
            self.restrictionsSt14 = None
        elif 'restrictionsSt14' in dic:
            self.restrictionsSt14 = cmn.restrictionSt14Type(dic['restrictionsSt14']) #Перечень требований, нормативно-правовых актов, конкретизирующих особенностей применения национального режима. Указание допустимо и обязательно для ограничения «Запрет на допуск товаров, работ, услуг при осуществлении закупок, а также ограничения и условия допуска в соответствии с требованиями, установленными статьей 14 Федерального закона № 44-ФЗ» (код JB2149)
        else:
            self.content = None
            self.restrictionsSt14 = None
            

class zfcs_publicDiscussionType:
    "Информация об общественном обсуждении по лоту закупки"
    
    class publicDiscussion2017:
        "Информация об общественном обсуждении по лоту закупки с 01.01.2017"
        
        class publicDiscussionLargePurchasePhase2:
            "Информация о втором этапе ООКЗ"
            
            class attachments:
                "Протокол этапа"
                
                class attachment(zfcs_attachmentType):
                    "Документ"
                    
                    def __init__ (self, dic):
                        zfcs_attachmentType.__init__(self, dic)
                        if 'placingDate' in dic:
                            self.placingDate = parse(dic['placingDate']) #Дата размещения документа. Элемент не используется при приеме данных
                        else:
                            self.placingDate = None
                
                def __init__ (self, dic):
                    self.attachement = []
                    if isinstance(dic['attachment'], list):
                        for at in dic['attachment']:
                            self.attachment.append(zfcs_publicDiscussionType.publicDiscussion2017.publicDiscussionLargePurchasePhase2.attachments.attachment(at))
                    else:
                        self.attachment.append(zfcs_publicDiscussionType.publicDiscussion2017.publicDiscussionLargePurchasePhase2.attachments.attachment(at))
            
            def __init__ (self, dic):
                if 'protocolDate' in dic:
                    self.protocolDate = parse(dic['protocolDate']) #Дата протокола
                else:
                    self.protocolDate = None
                
                if 'protocolPublishDate' in dic:
                    self.protocolPublishDate = parse(dic['protocolPublishDate']) #Дата размещения протокола<
                else:
                    self.protocolPublishDate = None
                
                if 'publicDiscussionPhase2Num' in dic:
                    self.publicDiscussionPhase2Num = bt.publicDiscussionNumType(dic['publicDiscussionPhase2Num']) #Реестровый номер второго этапа общественного обсуждения
                else:
                    self.publicDiscussionPhase2Num = None
                
                if 'hrefPhase2' in dic:
                    self.hrefPhase2 = zfcs_longTextType(dic['hrefPhase2']) #Ссылка на второй этап общественного обсуждения в сети Интернет
                else:
                    self.hrefPhase2 = None
                    
                if 'attachments' in dic:
                    self.attachments = zfcs_publicDiscussionType.publicDiscussion2017.publicDiscussionLargePurchasePhase2.attachments(dic['attachments']) #Протокол этапа
                else:
                    self.attachments = None
        
        def __init__(self, dic):
            if 'publicDiscussionLargePurchasePhase2' in dic:
                self.publicDiscussionLargePurchasePhase2 = zfcs_publicDiscussionType.publicDiscussion2017.publicDiscussionLargePurchasePhase2(dic['publicDiscussionLargePurchasePhase2']) #Информация о втором этапе ООКЗ
            else:
                self.publicDiscussionLargePurchasePhase2 = None
    
    
    def __init__ (self, dic):
        assert( ('number' in dic) or ('organizationCh5St15' in dic) or ('href' in dic) or ('publicDiscussion2017' in dic) ), "No required fields"
        if 'number' in dic:
            self.number = bt.publicDiscussionNumType(dic['number']) #Номер общественного обсуждения
            self.organizationCh5St15 = None
            self.href = None
            self.publicDiscussion2017 = None
        elif 'organizationCh5St15' in dic:
            assert( (dic['organizationCh5St15'] == 'true') or (dic['organizationCh5St15'] == 'false') ), "Invalid value"
            self.organizationCh5St15 = dic['organizationCh5St15']
            self.href = None
            self.publicDiscussion2017 = None
            self.number = None
        elif 'href' in dic:
            self.href = zfcs_longTextType(dic['href'])
            self.publicDiscussion2017 = None
            self.number = None
            self.organizationCh5St15 = None
        elif 'publicDiscussion2017' in dic:
            self.publicDiscussion2017 = zfcs_publicDiscussionType.publicDiscussion2017(dic['publicDiscussion2017'])
            self.href = None
            self.publicDiscussion2017 = None
            self.number = None
        
        if 'place' in dic:
            self.place = bt.publicDiscussionPlaceEnum(dic['place']) #Место проведения общественного обсуждения: E - в разделе «Общественные обсуждения крупных закупок» Официального сайта Единой информационной системы в сфере закупок; F - на форуме Официального сайта Единой информационной системы в сфере закупок.
        else:
            self.place = None

class zfcs_purchaseChangeType:
    "Основание внесения изменений в закупку/отмены закупки"
    
    class responsibleDecision:
        "По решению заказчика (организации, осуществляющей определение поставщика для заказчика)"
        
        def __init__ (self, dic):
            self.decisionDate = parse(dic['decisionDate']) #Дата принятия решения
            
    class authorityPrescription:
        "Предписание органа, уполномоченного на осуществление контроля"
        
        class reestrPrescription:
            "Данные о предписании, выданном КО"
            
            def __init__ (self, dic):
                self.checkResultNumber = bt.checkResultNumberType(dic['checkResultNumber']) #Номер результата контроля по предписанию. При приеме контролируется наличие контроля с таким номером в актуальном состоянии в реестре результатов контроля и его принадлежность к закупке с номером, указанном в поле purchaseNumber
                if 'prescriptionNumber' in dic:
                    self.prescriptionNumber = bt.prescriptionNumberType(dic['prescriptionNumber']) #Номер предписания. При приеме контролируется, что поле заполнено номером предписания, относящегося к результату контроля с номером, указанным в поле checkResultNumber
                else:
                    self.prescriptionNumber = None
                
                if 'foundation' in dic:
                    self.foundation = zfcs_longTextType(dic['foundation']) #Основание внесения изменений по предписанию
                else:
                    self.foundation = None
                
                if 'authorityName' in dic:
                    self.authorityName = zfcs_longTextType(dic['authorityName']) #Наименование органа, уполномоченного на осуществление контроля (для печатной формы)
                else:
                    self.authorityName = None
                
                if 'docDate' in dic:
                    self.docDate = parse(dic['docDate']) #Дата документа (для печатной формы)
                else:
                    self.docDate = None
                    
        class externalPrescription:
            "Предписание отсутствует в реестре результатов контроля"
            
            def __init__ (self, dic):
                self.authorityName = zfcs_longTextType(dic['authorityName']) #Наименование органа, уполномоченного на осуществление контроля
                self.authorityType = bt.authorityType(dic['authorityType']) #ид органа, уполномоченного на осуществление контроля FA - Федеральная антимонопольная служба; FO - Федеральная служба по оборонному заказу; S - Орган исполнительной власти субъекта РФ; M - Орган местного самоуправления муниципального района, городского округа
                assert(len(dic['docName']) <= 1000), "Invalid value"
                self.docName = dic['docName'] #Наименование документа
                self.docDate = parse(dic['docDate']) #Дата документа
                assert(len(dic['docNumber']) <= 1000), "Invalid value"
                self.docNumber = dic['docNumber'] #Номер документа
        
        def __init__ (self, dic):
            assert( ('reestrPrescription' in dic) or ('externalPrescription' in dic) ), "No required fields"
            if 'reestrPrescription' in dic:
                self.reestrPrescription = zfcs_purchaseChangeType.authorityPrescription.reestrPrescription(dic['reestrPrescription']) #Данные о предписании, выданном КО
                self.externalPrescription = None
            elif 'externalPrescription' in dic:
                self.externalPrescription = zfcs_purchaseChangeType.authorityPrescription.externalPrescription(dic['externalPrescription']) #Предписание отсутствует в реестре результатов контроля
        
        class courtDecision:
            "Решение судебного органа"
            
            def __init__ (self, dic):
                self.court_name = zfcs_longTextType(dic['court_name']) #Наименование судебного органа
                assert(len(dic['docName']) <= 1000), "Invalid value"
                self.docName = dic['docName'] #Наименование документа
                self.docDate = parse(dic['docDate']) #Дата документа
                assert(len(dic['docNumber']) <= 350), "Invalid value"
                self.docNumber = dic['docNumber'] #Номер документа
                
        class discussionResult:
            "Общественное обсуждение"
            
            def __init__ (self, dic):
                assert(len(dic['docName']) <= 1000), "Invalid value"
                self.docName = dic['docName'] #Наименование документа
                self.docDate = parse(dic['docDate']) #Дата документа
                assert(len(dic['docNumber']) <= 350), "Invalid value"
                self.docNumber = dic['docNumber'] #Номер документа
    
    def __init__ (self, dic):
        assert( ('responsibleDecision' in dic) or ('authorityPrescription' in dic) or ('courtDecision' in dic) or ('discussionResult' in dic) ), "No required fields"
        if 'responsibleDecision' in dic:
            self.responsibleDecision = zfcs_purchaseChangeType.responsibleDecision(dic['responsibleDecision']) #По решению заказчика (организации, осуществляющей определение поставщика для заказчика)
            self.authorityPrescription = None
            self.courtDecision = None
            self.discussionResult = None
        elif 'authorityPrescription' in dic:
            self.authorityPrescription = zfcs_purchaseChangeType.authorityPrescription(dic['authorityPrescription']) #Предписание органа, уполномоченного на осуществление контроля
            self.courtDecision = None
            self.discussionResult = None
            self.responsibleDecision = None
        elif 'courtDecision' in dic:
            self.courtDecision = zfcs_purchaseChangeType.courtDecision(dic['courtDecision']) #Решение судебного органа
            self.discussionResult = None
            self.responsibleDecision = None
            self.authorityPrescription = None
        elif 'discussionResult' in dic:
            self.discussionResult = zfcs_purchaseChangeType.discussionResult(dic['discussionResult']) #Общественное обсуждение
            self.responsibleDecision = None
            self.authorityPrescription = None
            self.courtDecision = None
    
            
class zfcs_notificationModificationType:
    "Внесение изменений в извещение"
    
    def __init__ (self, dic):
        self.modificationNumber = bt.versionNumberType(dic['modificationNumber']) #Номер изменения
        self.info = zfcs_longTextType(dic['info']) #Краткое описание изменения
        if 'addInfo' in dic:
            self.addInfo = zfcs_longTextType(dic['addInfo']) #Дополнительная информация
        else:
            self.addInfo = None
        self.reason = zfcs_purchaseChangeType(dic['reason']) #Основание внесения исправлений
        
class zfcs_clarificationProcedureInfoType:
    "Тип: Информация о предоставлении разъяснений положений документации"
    
    def __init__ (self, dic):
        if 'startDate' in dic:
            self.startDate = parse(dic['startDate']) #Дата и время начала предоставления. 
# 1) При приеме первой версии извещения: 
# Если не задано в принимаемом документе, то значение даты и времени начала предоставления будет сформировано автоматически при размещении извещения. Значение будет соответствовать фактической дате и времени размещения первой версии извещения по местному времени организации, осуществляющей размещение;
# 2) При приеме второй и последующих версий извещения: 
# Если не задано в принимаемом документе, то значение даты и времени начала предоставления будет сформировано автоматически при размещении второй и последующей версий извещения. Значение будет соответствовать значению  из предыдущей размещенной версии извещения
        else:
            self.startDate = None
        
        if 'filledManuallyStartDate' in dic:
            assert( (dic['filledManuallyStartDate'] == 'true') or (dic['filledManuallyStartDate'] == 'false') ), "Invalid value"
            self.filledManuallyStartDate = dic['filledManuallyStartDate'] #Задать вручную дату и время начала предоставления. Игнорируется при приеме-передаче, используется в печатной форме
        else:
            self.filledManuallyStartDate = None
        
        if 'endDate' in dic:
            self.endDate = parse(dic['endDate']) #Дата и время окончания предоставления
        else:
            self.endDate = None
            
        self.deliveryProcedure = bt.text2000Type(dic['deliveryProcedure']) #Порядок предоставления
        
class zfcs_documentationEAType:
    "Тип: Структурированная документация в рамках проведения аукционов в электронной форме"
    
    def __init__ (self, dic):
        assert( (dic['purchaseObjectsCh9St37'] == 'true') or (dic['purchaseObjectsCh9St37'] == 'false') ), "Invalid value"
        self.purchaseObjectsCh9St37 = dic['purchaseObjectsCh9St37'] #Предметом контракта является поставка товара, необходимого для нормального жизнеобеспечения в случаях, указанных в части 9 статьи 37 Федерального закона 44-ФЗ
        assert( (dic['modifiable'] == 'true') or (dic['modifiable'] == 'false') ), "Invalid value"
        self.modifiable = dic['modifiable'] #Возможно изменить предусмотренные контрактом количество товара, объем работ или услуг
        self.clarificationInfo = zfcs_clarificationProcedureInfoType(dic['clarificationInfo']) #Информация о предоставлении разъяснений положений документации
        assert( (dic['onesideRejectionCh9St95'] == 'true') or (dic['onesideRejectionCh9St95'] == 'false') ), "Invalid value"
        self.onesideRejectionCh9St95 = dic['onesideRejectionCh9St95'] #Возможность одностороннего отказа от исполнения контракта в соответствии с ч. 9 ст. 95 Закона № 44-ФЗ
        if 'printFormInfo' in dic:
            self.printFormInfo = cmn.printFormType(dic['printFormInfo']) #Печатная форма документа. Элемент игнорируется при приёме. При передаче заполняется ссылкой на печатную форму и электронную подпись размещенного в ЕИС документа
        else:
            self.printFormInfo = None
        
        if 'extPrintFormInfo' in dic:
            self.extPrintFormInfo = cmn.extPrintFormType(dic['extPrintFormInfo']) #Электронный документ, полученный из внешней системы
        else:
            self.extPrintFormInfo = None
        
                
class zfcs_notificationEFType(zfcs_purchaseNotificationType):
    "Извещение о проведении ЭА (электронный аукцион); внесение изменений"
    
    class procedureInfo:
        "Информация о процедуре закупки"
        
        class scoring:
            "Информация о процедуре рассмотрения и оценки заявок на участие в аукционе"
            
            def __init__ (self, dic):
                self.date = parse(dic['date']) #Дата рассмотрения первых частей заявок участников
        
        class bidding:
            "Информация о процедуре проведения аукциона в электронной форме"
            
            def __init__ (self, dic):
                self.date = parse(dic['date']) #Дата и время проведения аукциона в электронной форме
                if 'addInfo' in dic:
                    self.addInfo = zfcs_longTextType(dic['addInfo']) #Дополнительная информация
                else:
                    self.addInfo = None
        
        def __init__ (self, dic):
            self.collecting = zfcs_purchaseProcedureCollectingType(dic['collecting']) #Информация о подаче заявок
            self.scoring = zfcs_notificationEFType.procedureInfo.scoring(dic['scoring']) #Информация о процедуре рассмотрения и оценки заявок на участие в аукционе
            self.bidding = zfcs_notificationEFType.procedureInfo.bidding(dic['bidding']) #Информация о процедуре проведения аукциона в электронной форме                            
    class lot:
        "Лот извещения"
        
        class customerRequirements:
            "Требования заказчика"
            
            class customerRequirement:
                "Требование заказчика"

                def __init__ (self, dic):
                    self.customer = zfcs_organizationRef(dic['customer']) #Организация заказчика данных требований
                    self.maxPrice = bt.moneyType(dic['maxPrice']) #Начальная (максимальная) цена контракта
                    if 'maxPriceCurrency' in dic:
                        self.maxPriceCurrency = bt.moneyType(dic['maxPriceCurrency']) #Начальная (максимальная) цена в валюте контракта.
                    else:
                        self.maxPriceCurrency = None
                    if 'deliveryPlace' in dic:
                        self.deliveryPlace = zfcs_longTextType(dic['deliveryPlace']) #Место доставки товара, выполнения работы или оказания услуги (устарело)
                        self.kladrPlaces = None
                    elif 'kladrPlaces' in dic:
                        self.kladrPlaces = zfcs_kladrPlacesType(dic['kladrPlaces']) #Места доставки товара, выполнения работы или оказания услуги по справочнику КЛАДР
                        self.deliveryPlace = None
                    self.deliveryTerm = zfcs_longTextType(dic['deliveryTerm']) #Сроки доставки товара, выполнения работы или оказания услуги либо график оказания услуг
                    if 'applicationGuarantee' in dic:
                        self.applicationGuarantee = zfcs_paymentInfoType(dic['applicationGuarantee']) #Обеспечение заявок. Блок может быть не заполнен, если заказчик осуществляет деятельность на территории иностранного государства (в справочнике «Субъект контроля по 99 статье» (nsiControl99Subjects) для данного заказчика значение поля «Организация включена в перечень ст. 111.1 Федерального закона №44-ФЗ» (isSt111_1) равно «true»)
                    else:
                        self.applicationGuarantee = None

                    if 'contractGuarantee' in dic:
                        self.contractGuarantee = zfcs_paymentInfoType(dic['contractGuarantee']) #Обеспечение исполнения контракта
                    else:
                        self.contractGuarantee = None

                    if 'unableProvideContractGuaranteeDocs' in dic:
                        self.unableProvideContractGuaranteeDocs = zfcs_attachmentListType(dic['unableProvideContractGuaranteeDocs']) #Отчет с обоснованием невозможности установления требования обеспечения контракта. Контролируется бизнес-контролем заполнение блока, если (И):
    # -первая версия извещения размещена после выхода версии ЕИС 9.1;
    # -не заполнен блок "Обеспечение исполнения контракта" (contractGuarantee);
    # -заказчик осуществляет деятельность на территории иностранного государства (в справочнике «Субъект контроля по 99 статье» (nsiControl99Subjects) для данного заказчика значение поля «Организация включена в перечень ст. 111.1 
    # Федерального закона №44-ФЗ» (isSt111_1) равно «true»)
                    else:
                        self.unableProvideContractGuaranteeDocs = None
                    if 'purchaseCode' in dic:
                        self.purchaseCode = bt.ikzCodeType(dic['purchaseCode']) #Идентификационный код закупки. Заполняется автоматически из плана-графика в случае указания блока tenderPlanInfo. Иначе требуется обязательное заполнение.
                    else:
                        self.purchaseCode = None

                    if 'tenderPlanInfo' in dic:
                        self.tenderPlanInfo = zfcs_tenderPlanInfoType(dic['tenderPlanInfo']) #Сведения о связи с позицией плана-графика. При приеме контролируется, что все позиции ПГ по требованиям заказчиков в рамках лота либо имеют признак "Невозможно определить количество (объём)" (quantityUndefined) либо не имеют такого признака
                    else:
                        self.tenderPlanInfo = None

                    if 'budgetFinancings' in dic:
                        self.budgetFinancings = zfcs_budgetFinancingsType(dic['budgetFinancings']) #План исполнения контракта за счет бюджетных средств.Игнорируется при приеме. Оставлен для обратной совместимости
                    else:
                        self.budgetFinancings = None

                    if 'nonbudgetFinancings' in dic:
                        self.nonbudgetFinancings = zfcs_nonbudgetFinancingsType(dic['nonbudgetFinancings']) #План исполнения контракта за счет внебюджетных средств.
                    else:
                        self.nonbudgetFinancings = None

                    if 'BOInfo' in dic:
                        self.BOInfo = zfcs_purchaseBOInfoType(dic['BOInfo']) #Информация о бюджетном обязательстве. Блок игнорируется при приеме, если данная организация-заказчик включена в настройку «Настройка ПРИЗ для организаций, в извещениях которых не требуется указание сведений о принимаемом БО»
                    else:
                        self.BOInfo = None

                    if 'purchaseObjectDescription' in dic:
                        self.purchaseObjectDescription = zfcs_longText4000MinType(dic['purchaseObjectDescription']) #Описание объекта закупки. В описании объекта закупки могут быть указаны функциональные, технические и качественные характеристики, эксплуатационные характеристики объекта закупки (при необходимости) в соответствии со статьей 33 Закона 44-ФЗ
                    else:
                        self.purchaseObjectDescription = None

                    if 'bankSupportContractRequiredInfo' in dic:
                        self.bankSupportContractRequiredInfo = cmn.bankSupportContractRequiredInfoType(dic['bankSupportContractRequiredInfo']) #Информация о банковском и (или) казначейском сопровождении контакта. Указание допустимо только для базовой версии извещения. Игнорируется при приеме изменений извещения. Игнорируется при приеме и заполняется на основании сведений связанного плана-графика, если указан блок tenderPlanInfo и в связанном ППГ Информация о банковском сопровождении контракта не равна «Требуется банковское или казначейское сопровождение контракта»
                    else:
                        self.bankSupportContractRequiredInfo = None
                        
            
            def __init__ (self, dic):
                self.customerRequirement = []
                if isinstance(dic['customerRequirement'], list):
                    for requirement in dic['customerRequirement']:
                        self.customerRequirement.append(zfcs_notificationEFType.lot.customerRequirements.customerRequirement(requirement))
                else:
                    self.customerRequirement.append(zfcs_notificationEFType.lot.customerRequirements.\
                                                     customerRequirement(dic['customerRequirement']))

                
        class purchaseObjects:
            "Объекты закупки"   

            class purchaseObject:
                "Объект закупки"

                class OKPD2(zfcs_OKPDRef):
                    "Классификация по ОКПД2"

                    class characteristics:
                        "Характеристики товара, работы, услуги. Устарело. Игнорируется при приеме"

                        def __init__ (self, dic):
                            self.characteristicsUsingTextForm = []
                            if isinstance(dic['characteristicsUsingTextForm'], list):
                                for ch in dic['characteristicsUsingTextForm']:
                                    self.characteristicsUsingTextForm.append(zfcs_tenderPlan2017ManualKtruCharacteristicType(ch))
                            else:
                                self.characteristicsUsingTextForm = dic['characteristicsUsingTextForm']
                            if 'addCharacteristics' in dic:
                                self.addCharacteristics = zfcs_longText4000MinType(dic['addCharacteristics']) #Функциональные, технические, качественные характеристики, эксплуатационные характеристики
                            else:
                                self.addCharacteristics = None


                    def __init__ (self, dic):
                        zfcs_OKPDRef.__init__(self, dic)
                        if 'characteristics' in dic:
                            self.characteristics = zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.OKPD2.characteristics(dic['characteristics'])
                        else:
                            self.characteristics = None

                class KTRU(zfcs_KTRURef):
                    "Классификация по КТРУ"

                    class characteristics:
                        "Характеристики товара, работы, услуги позиции КТРУ. Контролируется обязательное заполнение хотя бы одного из дочерних блоков characteristicsUsingReferenceInfo и/или characteristicsUsingTextForm"

                        def __init__ (self, dic):
                            if 'characteristicsUsingReferenceInfo' in dic:
                                self.characteristicsUsingReferenceInfo = []
                                if isinstance(dic['characteristicsUsingReferenceInfo'], list):
                                    for info in dic['characteristicsUsingReferenceInfo']:
                                        self.characteristicsUsingReferenceInfo.append(zfcs_tenderPlan2017RefKtruCharacteristicType(info)) #Характеристика товара, работы услуги позиции КТРУ формируется с использованием справочной информации (справочник Каталог товаров, работ, услуг (КТРУ) (nsiKTRU))
                                else:
                                     self.characteristicsUsingReferenceInfo.append(dic['characteristicsUsingReferenceInfo'])
                            else:
                                self.characteristicsUsingReferenceInfo = None

                            if 'characteristicsUsingTextForm' in dic:
                                self.characteristicsUsingTextForm = []
                                if isinstance(dic['characteristicsUsingTextForm'], list):
                                    for info in dic['characteristicsUsingTextForm']:
                                        self.characteristicsUsingTextForm.append(zfcs_tenderPlan2017ManualKtruCharacteristicType(info)) #Характеристика товара, работы услуги позиции КТРУ формируется в текстовой форме
                                else:
                                     self.characteristicsUsingTextForm.append(dic['characteristicsUsingTextForm'])
                            else:
                                self.characteristicsUsingTextForm = None

                            if 'addCharacteristicInfoReason' in dic:
                                self.addCharacteristicInfoReason = zfcs_longTextMinType(dic['addCharacteristicInfoReason']) #Обоснование включения дополнительной информации в сведения о товаре, работе, услуге. Обязательность заполнения контролируется бизнес-контролем.
                            else:
                                self.addCharacteristicInfoReason = None

                    def __init__ (self, dic):
                        zfcs_KTRURef.__init__(self, dic)
                        if 'characteristics' in dic:
                            self.characteristics = zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.KTRU.characteristics(dic['characteristics'])
                        else:
                            self.characteristics = None

                class customerQuantities:
                    "Количество по заказчикам"

                    class customerQuantity:


                        def __init__ (self, dic):
                            self.customer = zfcs_organizationRef(dic['customer']) #Организация заказчика
                            self.quantity = bt.quantity18p11Type(dic['quantity']) #Количество для заказчика

                    def __init__ (self, dic):
                        self.customerQuantity = []
                        if isinstance(dic['customerQuantity'], list):
                            for q in dic['customerQuantity']:
                                self.customerQuantity.append(zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.customerQuantities.customerQuantity(q))
                        else:
                            self.customerQuantity.append(zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.customerQuantities.customerQuantity(dic['customerQuantity']))


                class quantity:
                    "Общее количество по объекту закупки"

                    def __init__ (self, dic):
                        assert ( ('value' in dic) or ('undefined' in dic) ), "No required fields"
                        if 'value' in dic:
                            self.value = bt.quantity18p11Type(dic['value']) #Количество
                            self.undefined = None
                        elif 'undefined' in dic: 
                            assert( (dic['undefined'] == 'true') or (dic['undefined'] == 'false') ), "Invalid value"
                            self.undefined = dic['undefined'] #Невозможно определить количество
                            self.value = None


                def __init__ (self, dic):
                    assert( ('OKPD' in dic) or ('OKPD2' in dic) or ('KTRU' in dic)), "No required fields"
                    if 'OKPD' in dic:
                        self.OKPD = zfcs_OKPDRef(dic['OKPD']) #Классификация по ОКПД
                        self.OKPD2 = None
                        self.KTRU = None
                    elif 'OKPD2' in dic:
                        self.OKPD2 = zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.OKPD2(dic['OKPD2']) #Классификация по ОКПД2
                        self.OKPD = None
                        self.KTRU = None
                    elif 'KTRU' in dic:
                        self.KTRU = zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.KTRU(dic['KTRU']) #Классификация по КТРУ
                        self.OKPD = None
                        self.OKPD2 = None
                    if 'name' in dic:
                        self.name = zfcs_longTextType(dic['name']) #Наименование товара, работы, услуги. Игнорируется и заполняется наименованием КТРУ, если указана классификация по КТРУ (KTRU/code).  Если указана классификация по ОКПД2 (OKPD2/code), то если поле  заполнено в принимаемом документе, то сохраняется это "ручное" значение, иначе поле автоматически заполняется наименованием ОКПД2 по его коду
                    else:
                        self.name = None

                    if 'OKEI' in dic:
                        self.OKEI = zfcs_contract_OKEIType #original name: zfcs_contract.OKEIType
                    else:
                        self.OKEI = None
                        
                    if 'customerQuantities' in dic:
                        self.customerQuantities = zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.customerQuantities(dic['customerQuantities']) #Количество по заказчикам
                    else:
                        self.customerQunatities = None

                    if 'price' in dic:
                        self.price = bt.moneyType(dic['price']) #Цена за единицу измерения
                    else:
                        self.price = None

                    self.quantity = zfcs_notificationEFType.lot.purchaseObjects.purchaseObject.quantity(dic['quantity']) #Общее количество по объекту закупки


            def __init__ (self, dic):
                self.purchaseObject = []
                if isinstance(dic['purchaseObject'], list):
                    for obj in dic['purchaseObject']:
                        self.purchaseObject.append(zfcs_notificationEFType.lot.purchaseObjects.purchaseObject(obj))
                else:
                    self.purchaseObject.append(zfcs_notificationEFType.lot.purchaseObjects.purchaseObject(dic['purchaseObject']))
                if 'totalSum' in dic:
                    self.totalSum = bt.moneyType(dic['totalSum']) #Общая сумма позиций
                else:
                    self.totalSum = None

                if 'totalSumCurrency' in dic:
                    self.totalSumCurrency = bt.moneyType(dic['totalSumCurrency']) #Общая сумма позиций в валюте контракта
                else:
                    self.totalSumCurrency = None
        
        class preferences:
            "Преимущества"
            
            def __init__ (self, dic):
                self.preferense = []
                if isinstance(dic['preferense'], list):
                    for p in dic['preferense']:
                        self.preferense.append(zfcs_preferenseType(p)) #Преимущество
                else:
                    self.preferense.append(zfcs_preferenseType(dic['preferense']))
                    
        class requirements:
            "Требования"
            
            def __init__ (self, dic):
                self.requirement = []
                if isinstance(dic['requirement'], list):
                    for p in dic['requirement']:
                        self.requirement.append(zfcs_requirementType(p)) #Преимущество
                else:
                    self.requirement.append(zfcs_requirementType(dic['requirement']))
         
        class restrictions:
            "Ограничения"
            
            def __init__ (self, dic):
                self.restriction = []
                if isinstance(dic['restriction'], list):
                    for r in dic['restriction']:
                        self.restriction.append(zfcs_restrictionType(r))
                else:
                    self.restriction.append(zfcs_restrictionType(dic['restriction']))
                    
        class publicDiscussion(zfcs_publicDiscussionType):
            "Общественное обсуждение крупных закупок (для печатной формы). Игнорируется при приеме. Автоматически заполняется при передаче"
            
            def __init__ (self, dic):
                zfcs_publicDiscussionType.__init__(self, dic)

        
        def __init__ (self, dic):
            self.maxPrice = bt.moneyType(dic['maxPrice']) #Начальная (максимальная) цена контрактов
            if 'priceFormula' in dic:
                self.priceFormula = zfcs_longTextType(dic['priceFormula']) #Формула цены. Устанавливается, если закупка осуществляется в соответствии с ПП РФ от 13.01.2014 №19 "Об установлении случаев, в которых при заключении контракта в документации о закупке указываются формула цены и максимальное значение цены контракта
            else:
                self.priceFormula = None
            if 'standardContractNumber' in dic:
                self.standardContractNumber = bt.standardContractNumber(dic['standardContractNumber']) #Номер типового контракта, типовых условий контракта
            else:
                self.standardContractNumber = None
            
            self.currency = zfcs_currencyRef(dic['currency']) #Валюта
            if 'isMaxPriceCurrency' in dic:
                self.isMaxPriceCurrency = dic['isMaxPriceCurrency'] #Указать НМЦК в валюте контракта. Заполнение доступно только при значении «Российский рубль» поля lot/currency
            else:
                self.isMaxPriceCurrency = None
            self.financeSource = zfcs_longTextType(dic['financeSource']) #Источник финансирования
            if 'interBudgetaryTransfer' in dic:
                assert((dic['interBudgetaryTransfer'] == 'false') & (dic['interBudgetaryTransfer'] == 'true')), "{} is invalid value".format(dic['interBudgetaryTransfer'])
                self.interBudgetaryTransfer = dic['interBudgetaryTransfer'] #Закупка осуществляется за счет межбюджетного трансферта из бюджета субъекта Российской Федерации. Значение может быть указано только если организация, осуществляющая закупку, имеет муниципальный уровень, в остальных случаях игнорируется при загрузке
            else:
                self.interBudgetaryTransfer = None
            assert((dic['quantityUndefined'] == 'false') or (dic['quantityUndefined'] == 'true')), "{} is invalid value".format(dic['quantityUndefined'])
            self.quantityUndefined = dic['quantityUndefined'] #Невозможно определить количество товара, объем подлежащих выполнению работ, оказанию услуг
            self.customerRequirements = zfcs_notificationEFType.lot.customerRequirements(dic['customerRequirements'])
            assert( ('purchaseObjects' in dic) or ('drugPurchaseObjectsInfo' in dic) ), "No required fields"
            if 'purchaseObjects' in dic:
                self.purchaseObjects = zfcs_notificationEFType.lot.purchaseObjects(dic['purchaseObjects'])
                self.drugPurchaseObjectsInfo = None
            elif 'drugPurchaseObjectsInfo' in dic:
                self.drugPurchaseObjectsInfo = zfcs_purchaseDrugPurchaseObjectsInfoType(dic['drugPurchaseObjectsInfo'])
                self.purchaseObjects = None
                
            if 'preferenses' in dic:
                self.preferenses = zfcs_notificationEFType.lot.preferences(dic['preferenses']) #Преимущества
            else:
                self.preferenses = None
                
            if 'requirements' in dic:
                self.requirements = zfcs_notificationEFType.lot.requirements(dic['requirements']) #Требования
            else:
                self.requirements = None
                
            if 'restrictions' in dic:
                self.restrictions = zfcs_notificationEFType.lot.restrictions(dic['restrictions']) #Ограничения
            else:
                self.restrictions = None
            
            if 'restrictInfo' in dic:
                self.restrictInfo = zfcs_longTextType(dic['restrictInfo']) #Ограничение участия в определении поставщика (подрядчика, исполнителя), установленное в соответствии с ФЗ (согласно п.4 ст.42 Федерального закона № 44-ФЗ).  Устарело, не применяется, вместо него следует использовать  "Ограничения" (restrictions). Оставлено для обратной совместимости схем
            else:
                self.restrictInfo = None
                
            if 'restrictForeignsInfo' in dic:
                self.restrictForeignsInfo = zfcs_longTextType(dic['restrictForeignsInfo']) #Условия, запреты и ограничения допуска товаров, происходящих из иностранного государства или группы иностранных государств, работ, услуг, соответственно выполняемых, оказываемых иностранными лицами (согласно п.7 ч.5 ст.63 Федерального закона № 44-ФЗ) Игнорируется при приеме. Оставлен для обратной совместимости
            else:
                self.restrictForeignsInfo = None
                
            if 'addInfo' in dic:
                self.addInfo = zfcs_longTextType(dic['addInfo']) #Дополнительная информация
            else:
                self.addInfo = None
                
            if 'noPublicDiscussion' in dic:
                assert( (dic['noPublicDiscussion'] == 'true') or (dic['noPublicDiscussion'] == 'false') ), "Invalid value"
                self.noPublicDiscussion = dic['noPublicDiscussion'] #Закупка не подлежит обязательному общественному обсуждению в соответствии с подпунктами 2) и 3) пункта 1.4 Приказа Минэкономразвития от  30.10.2015г. № 795 (Устарело, не применяется
            else:
                self.noPublicDiscussion = None
            
            if 'publicDiscussion' in dic:
                self.publicDiscussion = zfcs_notificationEFType.lot.publicDiscussion(dic['publicDiscussion']) #Общественное обсуждение крупных закупок (для печатной формы). Игнорируется при приеме. Автоматически заполняется при передаче
            else:
                self.publicDiscussion = None
                
            if 'mustPublicDiscussion' in dic:
                assert( (dic['mustPublicDiscussion'] == 'true') or (dic['mustPublicDiscussion'] == 'false') ), "Invalid value"
                self.mustPublicDiscussion = dic['mustPublicDiscussion']
            else:
                self.mustPublicDiscussion = None
    
    def __init__ (self, dic):
        zfcs_purchaseNotificationType.__init__(self, dic)
        self.ETP = zfcs_ETPType(dic['ETP']) #Электронная торговая площадка
        self.procedureInfo = zfcs_notificationEFType.procedureInfo(dic['procedureInfo']) #Информация о процедуре закупки
        self.lot = zfcs_notificationEFType.lot(dic['lot']) #Лот извещения
        if 'notificationAttachments' in dic:
            self.notificationAttachments = zfcs_attachmentListType(dic['notificationAttachments']) #Файлы извещения. Принимаются только для извещений, первая версия которых была размещена ПОСЛЕ выхода версии 9.0 (01.01.2019) с документацией в структурированном виде (блок documentation). При приеме файлы из блока помещаются на вкладку «Требования к участникам» карточки закупки
        else:
            self.notificationAttachments = None
        self.attachments = zfcs_attachmentListType(dic['attachments']) #Документация об аукционе. При приеме файлы из блока  помещаются на вкладку "Документация об электронном аукционе" карточки закупки
        if 'modification' in dic:
            self.modification = zfcs_notificationModificationType(dic['modification']) #Основание внесения изменений
        else:
            self.modification = None
        
        if 'documentation' in dic:
            self.documentation = zfcs_documentationEAType(dic['documentation']) #Документация об электронном аукционе.  Контролируется обязательность заполнения для извещений, первая версия которых была размещена ПОСЛЕ выхода версии 9.0 (01.01.2019) Игнорируется при приеме  извещений, первая версия которых которых была размещена ДО выхода версии 9.0 (01.01.2019)
        else:
            self.documentation = None
            
class zfcs_commissionRoleType:
    "Роли членов комиссий"
    
    def __init__(self, dic):
        self.id = dic['id'] #Идентификатор
        if 'name' in dic:
            assert( (len(dic['name']) >= 1) and (len(dic['name']) <= 50) ), "Invalid value"
            self.name = dic['name'] #Наименование роли
        else:
            self.name = None
        assert( (dic['rightVote'] == 'false') or (dic['rightVote'] == 'true') ), "Invalid value"
        self.rightVote = dic['rightVote'] #Имеет право голоса             

class zfcs_commissionMemberType:
    "Член комиссии"
    
    def __init__(self, dic):
        self.memberNumber = dic['memberNumber'] #Порядковый номер члена комиссии
        assert( (len(dic['lastName']) >= 1) and (len(dic['lastName']) <= 50) ), "Invalid value"
        self.lastName = dic['lastName']
        assert( (len(dic['firstName']) >= 1) and (len(dic['firstName']) <= 50) ), "Invalid value"
        self.firstName = dic['firstName']
        if 'middleName' in dic:
            assert( (len(dic['middleName']) >= 1) and (len(dic['middleName']) <= 50) ), "Invalid value"
            self.middleName = dic['middleName']
        else:
            self.middleName = None
        self.role = zfcs_commissionRoleType(dic['role']) #Роль члена комиссии

class zfcs_commissionType:
    "Комиссии по размещению заказа (определению поставщика)"
    
    class commissionMembers:
        "Участники комиссии"
        
        class commissionMember(zfcs_commissionMemberType):
            "Участник комиссии"
            
            def __init__(self, dic):
                zfcs_commissionMemberType.__init__(self)
        
        def __init__(self, dic):
            self.comissionMember = []
            if isinstance(dic['comissionMember'], list):
                for m in dic['comissionMember']:
                    self.comissionMember.append(zfcs_commissionType.commissionMembers.commissionMember(m))
    
    def __init__(self, dic):
        self.commissionName = zfcs_longTextType(dic['commissionName']) #Название комиссии
        self.commissionMembers = commissionMembers(dic['commissionMembers']) #Участники комиссии
            
class zfcs_purchaseProtocolEFType:
    "Общий тип для структурированных протоколов электронного аукциона"
    
    class protocolPublisher:
        "Информация об организации, разместившей протокол"
        
        def __init__(self, dic):
            self.publisherOrg = zfcs_purchaseOrganizationType(dic['publisherOrg']) #Организация, разместившая протокол
            self.publisherRole = zfcs_responsibleRoleType(dic['publisherRole']) #Роль организации, разместившей протокол
    
    def __init__ (self, dic):
        if 'id' in dic:
            self.id = dic['id'] #Идентификатор документа ЕИС
        else:
            self.id = None
        
        if 'externalId' in dic:
            self.externalId = bt.externalIdType(dic['externalId']) #Внешний идентификатор документа
        else:
            self.externalId = None
        self.purchaseNumber = bt.purchaseNumberType(dic['purchaseNumber']) #Номер закупки
        self.protocolNumber = zfcs_documentNumberType(dic['protocolNumber']) #Номер протокола
        if 'foundationProtocolNumber' in dic:
            self.foundationProtocolNumber = zfcs_documentNumberType(dic['foundationProtocolNumber']) #Номер предыдущего протокола
        else:
            self.foundationProtocolNumber = None
        
        if 'parentProtocolNumber' in dic:
            self.parentProtocolNumber = zfcs_documentNumberType(dic['parentProtocolNumber']) #Номер родительского протокола - в случае внесения изменений
        else:
            self.parentProtocolNumber = None
        
        self.place = zfcs_longTextType(dic['place']) #Место проведения процедуры
        self.protocolDate = parse(dic['protocolDate']) #Дата составления протокола
        self.signDate = parse(dic['signDate']) #Дата подписания протокола
        if 'directDate' in dic:
            self.directDate = parse(dic['directDate']) #Дата направления на размещение протокола. Игнорируется при приеме. Заполняется автоматически датой направления на размещение текущей версии
        else:
            self.directDate = None
        
        if 'publishDate' in dic:
            self.publishDate = parse(dic['publishDate']) #Дата размещения протокола
        else:
            self.publishDate = None
        
        self.commission = zfcs_commissionType(dic['commission']) #Информация о комиссии
        self.href = bt.hrefType(dic['href']) #Гиперссылка на опубликованный документ
        if 'printForm' in dic:
            self.printForm = zfcs_printFormType(dic['printForm']) #Печатная форма протокола
        else:
            self.printForm = None
        
        if 'extPrintForm' in dic:
            self.extPrintForm = zfcs_extPrintFormType(dic['extPrintForm']) #Электронный документ, полученный из внешней системы
        else:
            self.extPrintForm = None
        
        if 'protocolPublisher' in dic:
            self.protocolPublisher = zfcs_purchaseProtocolEFType.protocolPublisher(dic['protocolPublisher']) #Информация об организации, разместившей протокол
        else:
            self.protocolPublisher = None
        
        if 'attachments' in dic:
            self.attachments = zfcs_attachmentListType(dic['attachments']) #Информация о прикрепленных документах
        else:
            self.attachments = None
        
        if 'modification' in dic:
            self.modification = zfcs_protocolModificationType(dic['modification']) #Основание внесения исправлений
        else:
            self.modification = None
        self.schemeVersion = bt.schemeVersionType(dic['@schemeVersion']) #Версия схемы

        
class zfcs_commissionMemberInAppType:
    "Член комиссии в заявке"
    
    def __init__(self, dic):
        self.memberNumber = dic['memberNumber'] #Порядковый номер члена комиссии
        

class zfcs_appRejectedReasonNotIDType:
    "Причины отказа рассмотрения заявки без указания причины отказа из справочника"
    
    class nsiRejectReason:
        "Причина отказа из справочника 'Справочник причин отказа в допуске заявок' (nsiPurchaseRejectReason)"
        
        def __init__(self, dic):
            assert( ('id' in dic) or ('code' in dic) ), "No required fields"
            if 'id' in dic:
                self.id = dic['id'] #Идентификатор. Устарело, не применяется, оставлено для обратной совместимости
                self.code = None
            elif 'code' in dic:
                self.id = None
                self.code = bt.rejectReasonCode(dic['code']) #Символьный код причины отказа рассмотрения заявки
            if 'reason' in dic:
                self.reason = bt.rejectReasonName(dic['reason']) #Название
            else:
                self.reason = None
            
    
    def __init__(self, dic):
        if 'nsiRejectReason' in dic:
            self.nsiRejectReason = zfcs_appRejectedReasonNotIDType.nsiRejectReason(dic['nsiRejectReason']) #Причина отказа из справочника "Справочник причин отказа в допуске заявок" (nsiPurchaseRejectReason)
        else:
            self.nsiRejectReason = None
        self.explanation = zfcs_longTextMinType(dic['explanation'])


class zfcs_admissionResults:
    "Результаты допуска заявки"
    
    class admissionResult:
        
        def __init__(self, dic):
            self.protocolCommissionMember = zfcs_commissionMemberInAppType(dic['protocolCommissionMember']) #Член комиссии, осуществляющий оценку
            assert( (dic['admitted'] == 'true') or (dic['admitted'] == 'false') ), "Invalid value"
            self.admitted = dic['admitted'] #Флаг допуска
            if 'appRejectedReason' in dic:
                self.appRejectedReason = []
                if isinstance(dic['appRejectedReason'], list):
                    for r in dic['appRejectedReason']:
                        self.appRejectedReason.append(zfcs_appRejectedReasonNotIDType(r)) #Причины отказа в допуске (Устарело)
                else:
                    self.appRejectedReason.append(zfcs_appRejectedReasonNotIDType(dic['appRejectedReason']))
            else:
                self.appRejectedReason = None
    
    def __init__(self, dic):
        self.admissionResult = []
        if isinstance(dic['admissionResult'], list):
            for res in dic['admissionResult']:
                self.admissionResult.append(zfcs_admissionResults.admissionResult(res))
        else:
            self.admissionResult.append(zfcs_admissionResults.admissionResult(dic['admissionResult']))

class zfcs_abandonedReasonTypeEnum:
    """Тип основания:
    OR - По окончании срока подачи заявок подана только одна заявка. Такая заявка признана соответствующей требованиям 44-ФЗ и требованиям, указанным в извещении;
    NR - По окончании срока подачи заявок не подано ни одной заявки;
    OV - По результатам рассмотрения заявок только одна заявка признана соответствующей требованиям ФЗ и требованиям, указанным в извещении;
    NV - Все поданные заявки отклонены;
    OV2 - По результатам рассмотрения вторых частей заявок только одна заявка признана соответствующей требованиям 44-ФЗ и требованиям, указанным в извещении или ни одной заявки не признано соответствующим данным требованиям.
    O - По окончании срока подачи заявок подана только одна заявка;
    NS - Не подано ни одного ценового предложения;
    ON - Подано единственное ценовое предложение о цене договора;
    OO - Отказано в допуске всем участникам электронной процедуры или о допуске только одного участника электронной процедуры;
    OV3 - По результатам рассмотрения вторых частей заявок только одна заявка признана соответствующей требованиям ФЗ и требованиям, указанным в извещении;
    OP  - В течение десяти минут после начала проведения электронного аукциона было подано единственное предложение о цене контракта;
    OV4 - По результатам рассмотрения второй части заявки с единственным ценовым предложением заявка признана соответствующей требованиям 44-ФЗ и требованиям, указанным в извещении;
    NV4 - По результатам рассмотрения второй части заявки с единственным ценовым предложением заявка признана несоответствующей требованиям 44-ФЗ и требованиям, указанным в извещении;
    NV3 - По результатам рассмотрения вторых частей заявок ни одной заявки не признано соответствующим данным требованиям;
    NV2 - По окончании срока подачи заявок подана только одна заявка. Такая заявка признана не соответствующей требованиям 44-ФЗ и требованиям, указанным в извещении
    """
    
    def __init__(self, string):
        type_list = ['OR', 'NR', 'OV', 'NV', 'OV2', 'O', 'NS', 'ON', 'OO', 'OV3', 'OP', 'OV4', 'NV4', 'NV3', 'NV2']
        assert(string in type_list), "Invalid value"
        self.value = string
    
            
class zfcs_abandonedReasonType:
    "Основания признания процедуры несостоявшейся"
    
    def __init__(self, dic):
        self.code = bt.abandonedReasonCode(dic['code']) #Код основания признания процедуры несостоявшейся
        if 'objectName' in dic:
            self.objectName = bt.abandonedReasonObjectName(dic['objectName']) #Наименование основания признания процедуры несостоявшейся
        else:
            self.objectName = None
        
        if 'name' in dic:
            self.name = bt.abandonedReasonName(dic['name']) #Наименование основания признания процедуры несостоявшейся
        else:
            self.name = None
        
        if 'type' in dic:
            self.type = zfcs_abandonedReasonTypeEnum(dic['type']) #Тип основания
        else:
            self.type = None
    
        
class zfcs_protocolEF1Type(zfcs_purchaseProtocolEFType):
    "Протокол рассмотрения заявок на участие в электронном аукционе"
    
    class protocolLot:
        "Лот протокола"
        
        class applications:
            "Заявки по лоту"
            
            class application:
                "Заявка"
                
                def __init__(self, dic):
                    self.journalNumber = bt.journalNumberType(dic['journalNumber']) #Номер заявки в журнале регистрации
                    self.appDate = parse(dic['appDate']) #Дата и время подачи заявки
                    if 'admissionResults' in dic:
                        self.admissionResults = zfcs_admissionResults(dic['admissionResults']) #Результаты допуска заявки
                    else:
                        self.admissionResults = None
                    assert( ('appRejectedReason' in dic) or ('admitted' in dic) ), "No required fields"
                    if 'appRejectedReason' in dic:
                        self.appRejectedReason = zfcs_appRejectedReasonNotIDType(dic['appRejectedReason']) #Причины отказа в допуске
                        self.admitted = None
                    elif 'admitted' in dic:
                        assert( (dic['admitted'] == 'true') or (dic['admitted'] == 'false') ), "Invalid value"
                        self.admitted = dic['admitted'] #Заявка допущена
                        self.appRejectedReason = None
                    
                    if 'commonInfo' in dic:
                        self.commonInfo = zfcs_longTextType(dic['commonInfo']) #Пояснения
                    else:
                        self.commonInfo = None
                    
                    if 'foreignCountryOrigin' in dic:
                        assert( (dic['foreignCountryOrigin'] == 'true') or (dic['foreignCountryOrigin'] == 'false') ), "Invalid value"
                        self.foreignCountryOrigin = dic['foreignCountryOrigin'] #Заявка содержит предложение о поставке товаров, происходящих из иностранного государства или группы иностранных государств, или работы, услуги, соответственно выполняемые, оказываемые иностранными лицами
                    else:
                        self.foreignCountryOrigin = None
            
            def __init__(self, dic):
                self.application = []
                if isinstance(dic['application'], list):
                    for app in dic['application']:
                        self.application.append(zfcs_protocolEF1Type.protocolLot.applications.application(app))
                else:
                    self.application.append(zfcs_protocolEF1Type.protocolLot.applications.\
                                            application(dic['application']))
        
        def __init__(self, dic):
            if 'applications' in dic:
                self.applications = zfcs_protocolEF1Type.protocolLot.applications(dic['applications'])
            else:
                self.applications = None
            
            if 'abandonedReason' in dic:
                self.abandonedReason = zfcs_abandonedReasonType(dic['abandonedReason']) #Признание аукциона несостоявшимся
            else:
                self.abandonedReason = None
            
            
    
    def __init__(self, dic):
        zfcs_purchaseProtocolEFType.__init__(self, dic)
        self.protocolLot = dic['protocolLot'] #Лот протокола
        
    