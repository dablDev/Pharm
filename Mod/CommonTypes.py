from Mod import BaseTypes as bt

class currencyRateType:
    "Тип: Курс валюты"
    
    def __init__ (self, dic):
        self.rate = dic['rate']; assert(isinstance(self.rate, float)) #Курс валюты по отношению к рублю
        if 'raiting' in dic:
            self.raiting = dic['raiting'] #Номинал валюты. Поле игнорируется при приеме, заполняется автоматически значением из ОКВ на дату последнего сохранения извещения/изменения извещения (приема интеграционного пакета)
        else:
            self.raiting = None


class purchaseIsMaxPriceCurrencyType:
    "Тип: НМЦК в валюте контракта"
    
    def __init__ (self, dic):
        if 'maxPriceCurrency' in dic:
            self.maxPriceCurrency = bt.moneyType(dic['maxPriceCurrency']) 
            #Начальная (максимальная) цена в валюте контракта.
#             Заполняется автоматически по формуле:
#             Для валют с номиналом = 1 или номинал не указан:
#             maxPrice / currencyRate/rate, где  currencyRate/rate - курс валюты по отношению к рублю на дату последнего сохранения извещения/изменения извещения (приема интеграционного пакета).
#             Для валют с номиналом не равным 1:
#             maxPrice * «Номинал» (из справочника валют для соответствующей валюты) / currencyRate/rate
        else:
            self.maxPriceCurrency = None
        
        self.currency = bt.currencyCBRFRef(dic['currency']) #Валюта из справочника "Список валют, курс на которые устанавливается ЦБ РФ" (nsiContractCurrencyCBRF)
        if 'currencyRate' in dic:
            self.currencyRate = currencyRateType(dic['currencyRate']) #Курс валюты по отношению к рублю на дату последнего сохранения извещения/изменения извещения (приема интеграционного пакета). Если блок не задан, то поле "Курс валюты по отношению к рублю"(rate) заполняется автоматически значением из ОКВ курса ЦБ РФ на дату последнего сохранения извещения/изменения извещения (приема интеграционного пакета)
        else:
            self.currencyRate = None
            
class bankSupportContractRequiredInfoType:
    "Тип: Информации о банковском и (или) казначейском сопровождении контакта"
    
    def __init__ (self, dic):
        if 'bankSupportContractRequired' in dic:
            assert( (dic['bankSupportContractRequired'] == 'false') or (dic['bankSupportContractRequired'] == 'true') ), "Invalid value"
            self.bankSupportContractRequired = dic['bankSupportContractRequired'] #Требуется банковское сопровождение контракта
            self.treasurySupportContractRequired = None
        elif 'treasurySupportContractRequired' in dic:
            assert( (dic['treasurySupportContractRequired'] == 'false') or (dic['treasurySupportContractRequired'] == 'true') ), "Invalid value"
            self.treasurySupportContractRequired = dic['treasurySupportContractRequired'] #Требуется казначейское сопровождение контракта
            self.bankSupportContractRequired = None
        
class drugChangeInfoType:
    "Тип: Информация указываемая при ручном изменении лекарственного препарата"
    
    def __init__ (self, dic):
        self.drugChangeReason = bt.drugChangeReasonRef(dic['drugChangeReason']) #Причина корректировки сведений о лекарственных препаратах
        if 'drugChangeReason' in dic:
            self.commentOrRequestNumber = bt.text2000Type(dic['commentOrRequestNumber']) #Комментарий / номер обращения в службу технической поддержки. Требуется обязательное указание, если в справочнике "Причины корректировки справочных данных о лекарственных препаратах" (nsiDrugChangeReason) для записи с соответствующим кодом причины корректировки поле "Признак «Обязательно указание комментарий / номер обращения в службу тех поддержки»" (mustSpecifyCommentOrRequestNumber) имеет значение true
        else:
            self.drugChangeReason = None
        if 'drugRef' in dic:
            self.drugRef = bt.text2000Type(dic['drugRef']) #Ссылка на сведения о лекарственном препарате в ГРЛС. Требуется обязатеьное указание, если в справочнике "Причины корректировки справочных данных о лекарственных препаратах" (nsiDrugChangeReason) для записи соответствующим кодом причины корректировки поле "Признак «Обязательно указание ссылки на сведения о ЛП в ГРЛС»" (mustSpecifyDrugRef) имеет значение true
        else:
            self.drugRef = None
            
class restrictionSt14Type:
    "Тип: Сведения по запрету, ограничению участия, условию допуска"
    
    class restrictionSt14:
        "Сведения по запрету, ограничению участия, условию допуска"
        
        class requirementsType:
            "Виды требований"
            
            class requirementType:
                "Вид требования"
                
                def __init__ (self, dic):
                    assert( (dic['type'] == 'AC') or (dic['type'] == 'RA') or (dic['type'] == 'BAN') ), "Invalid value"
                    self.type = dic['type'] #Вид требования: AC - условия допуска; RA - ограничение допуска; BAN - запрет.
                    
            def __init__ (self, dic):
                self.requirementType = []
                if isinstance(dic['requirementType'], list):
                    for t in dic['requirementType']:
                        self.requirementType.append(restrictionSt14Type.restrictionSt14.requirementsType.requirementType(t)) #Вид требования
                else:
                    self.requirementType.append(restrictionSt14Type.restrictionSt14.requirementsType.requirementType(dic['requirementType']))
              
        class exception:
            "Присутствуют обстоятельства, допускающие исключение, влекущее неприменение запрета, ограничения допуска"
            
            def __init__ (self, dic):
                assert( (dic['imposibilityBan'] == 'true') or (dic['imposibilityBan'] == 'false') ), "Invalid value"
                self.imposibilityBan = dic['imposibilityBan'] #Присутствуют обстоятельства, допускающие исключение, влекущее неприменение запрета, ограничения допуска
                self.imposibilityBanReason = bt.text2000Type(dic['imposibilityBanReason']) #Обоснование невозможности запрета, ограничения допуска
        
        def __init__ (self, dic):
            self.requirementsType = restrictionSt14Type.restrictionSt14.requirementsType(dic['requirementsType']) #Виды требований
            self.NPAInfo = bt.NPASt14Ref(dic['NPAInfo']) #Сведения о нормативно-правовом акте
            if 'exception' in dic:
                self.exception = restrictionSt14Type.restrictionSt14.exception(dic['exception']) #Присутствуют обстоятельства, допускающие исключение, влекущее неприменение запрета, ограничения допуска
            else:
                self.exception = None
            if 'note' in dic:
                self.note = bt.text2000Type(dic['note']) #Примечание
    
    def __init__ (self, dic):
        self.restrictionSt14 = []
        if isinstance(dic['restrictionSt14'], list):
            for r in dic['restrictionSt14']:
                self.restrictionSt14.append(restrictionSt14Type.restrictionSt14(r))
        else:
            self.restrictionSt14.append(restrictionSt14Type.restrictionSt14(dic['restrictionSt14']))
            
class printFormType:
    "Тип: Печатная форма"
    
    def __init__ (self, dic):
        self.url = bt.hrefType(dic['url']) #Ссылка для скачивания печатной формы
        if 'signature' in dic:
            dic['signature'] = ''
            
class extPrintForm:
    "Тип: Электронный документ, полученный из внешней системы"
    
    def __init__ (self, dic):
        assert( ('content' in dic) or ('contentId' in dic) or ('url' in dic) ), "No required fields"
        if 'content' in dic:
            self.content = dic['content'] #Содержимое файла электронного документа. Контролируется заполнение поля content или contentID при приёме. Поле не заполняется при передаче
            self.contentId = None
            self.url = None
        elif 'contentId' in dic:
            self.contentId = bt.guidType(dic['contentId']) #Уникальный идентификатор контента прикрепленного документа в ЕИС. Поле не заполняется при передаче
            self.content = None
            self.url = None
        elif 'url' in dic:
            self.url = bt.hrefType(dic['url']) #Ссылка для скачивания электронного документа. При приеме в ЕИС контролируется недопустимость заполнения данного поля. Поле заполняется при передаче
            self.content = None
            self.contentId = None
        self.fileType = bt.printFormFileType(dic['fileType'])
        dic['signature'] = ''
        
        
        
        
        
        