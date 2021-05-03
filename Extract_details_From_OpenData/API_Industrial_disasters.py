import requests                 # API 연결
from bs4 import BeautifulSoup   # XML 파싱

# API Base URL
BASE_URL = 'http://apis.data.go.kr/B490001/sjPrecedentInfoService/'
# API Key - 주로 Encoding Service Key가 사용되고 있음.
encSvcKey = '-------------------------YOUR ENCODING SERVICE KEY---------------------------------'

# 판결 유형 조회
def get_KindA_PrecedentResult_types():
    #유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
    get_sentence_API_url = BASE_URL + 'getPrecedentResultYuhyeongPstate?ServiceKey={}&pageNo=1&numOfRows=100'

    reqURL = get_sentence_API_url.format(encSvcKey)
    # Timeout 시간은 특별한 기준이 있는 것은 아니고 충분히 넉넉히 부여하였음.
    result = requests.get(reqURL, timeout=10)

    soup = BeautifulSoup(result.content, 'lxml')
    items = soup.find_all('kinda')

    sentence_types = []
    for kinda in items:
        sentence_types.append(kinda.string)
    return sentence_types

# 사건 유형 조회
def get_KindB_case_types():
    #유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
    get_case_API_url = BASE_URL + 'getSageonYuhyeongPstate?ServiceKey={}&pageNo=1&numOfRows=100'

    reqURL = get_case_API_url.format(encSvcKey)
    # Timeout 시간은 특별한 기준이 있는 것은 아니고 충분히 넉넉히 부여하였음.
    result = requests.get(reqURL, timeout=10)

    soup = BeautifulSoup(result.content, 'lxml')
    items = soup.find_all('kindb')

    case_types = []
    for kindb in items:
        case_types.append(kindb.string)
    return case_types

# 사고/질병 구분 조회
def get_KindC_AccidentDisease_types():
    #유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
    get_AccidentDisease_API_url = BASE_URL + 'getSagoJilbyeongGubunPstate?ServiceKey={}&pageNo=1&numOfRows=100'

    reqURL = get_AccidentDisease_API_url.format(encSvcKey)
    # Timeout 시간은 특별한 기준이 있는 것은 아니고 충분히 넉넉히 부여하였음.
    result = requests.get(reqURL, timeout=10)

    soup = BeautifulSoup(result.content, 'lxml')
    items = soup.find_all('kindc')

    AccidentDisease_types = []
    for kindc in items:
        AccidentDisease_types.append(kindc.string)
    return AccidentDisease_types

# 유형별 개수 조회
def get_Types_counts(kindA_types_list, kindB_types_list, kindC_types_list):
    types_counts_list = []
    get_types_count_URL = BASE_URL + 'getYuhyeongByCountPstate?serviceKey={}&kindA={}&kindB={}&kindC={}&numOfRows=100&pageNo=1'

    for tA in kindA_types_list:
        for tB in kindB_types_list:
            for tC in kindC_types_list:
                reqURL = get_types_count_URL.format(encSvcKey, tA, tB, tC)
                result = requests.get(reqURL, timeout=10)

                soup = BeautifulSoup(result.content, 'lxml')
                cnt = int(soup.cnt.string)

                types_counts_list.append([tA,tB,tC,cnt])
                print(tA,tB,tC,cnt)

    return types_counts_list

# 사건 상세 내용 조회
def get_detials_for_Cases(counts_for_Cases):
    detailURL = BASE_URL + 'getSjPrecedentNaeyongPstate?ServiceKey={}&kindA={}&kindB={}&kindC={}&numOfRows={}&pageNo={}'
    related_key = '연관판결 : ' #연관판결 정보 포함 여부 확인 키워드
    details_list = []
    for case in counts_for_Cases:
        # 사건 개수가 0이면 다음 사건 확인
        if case[3] == 0:
            continue

        # 사건 개수가 0이 아니면 사건 정보들을 추출하여 더함.
        # 한페이지당 100개씩
        numOfRows = 100
        numPage = case[3] // numOfRows

        # 여러 건이 조회 되었을 경우, 페이지 단위로 처리함.
        for pageIdx in range(0,numPage+1):
            #detailURL = BASE_URL + 'getSjPrecedentNaeyongPstate?ServiceKey={}&kindA={}&kindB={}&kindC={}&numOfRows={}&pageNo={}'
            reqURL = detailURL.format(encSvcKey, case[0], case[1], case[2],numOfRows,pageIdx+1)
            result = requests.get(reqURL, timeout=100)
            soup = BeautifulSoup(result.content, 'lxml')

            # 조회 된 아이템 처리
            items = soup.find_all('item')
            for item in items:
                accnum = item.accnum.string
                courtname = item.courtname.string
                kinda = item.kinda.string
                kindb = item.kindb.string
                kindc = item.kindc.string
                noncontent = item.noncontent.string
                title = item.title.string

                # 연관판결 여부 확인 - '연관판결 : '
                start_pos = noncontent.find(related_key)
                if start_pos < 0:   # 연관판결 정보 없음.
                    details_list.append([accnum, courtname, kinda, kindb, kindc, noncontent, title, ' '])
                    continue

                # 연관 판결이 포함되어 있다면 연관판결 키워드부터 '주문' 혹은 '주 문' 앞까지를 잘라냄.
                # 주문이 한번만 있다고 가정함. 실제 데이터에 띄어쓰기가 있는 것과 없는 것이 있었음.
                end_pos = max(noncontent.find('주문'),noncontent.find('주 문'))
                if end_pos < 0: #주문이 없으면 연관 재판 정보만 있는 경우로, 끝까지
                    details_list.append([accnum, courtname, kinda, kindb, kindc, noncontent, title, noncontent[start_pos+6:].strip()])
                    continue

                details_list.append([accnum, courtname, kinda, kindb, kindc, noncontent, title, noncontent[start_pos+6:end_pos].strip()])

        print("Done - ", case)

    return details_list