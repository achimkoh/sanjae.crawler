import requests                 # API 연결
from bs4 import BeautifulSoup   # XML 파싱
# import userkey                  # 공공데이터 포털에서 발급 받은 서비스키 (개인에게 발급되므로 각자 자기 코드 사용)
import re                       # 정규식으로 정보 추출
import datetime                 # 저장 파일 이름에 날짜 사용

# API Base URL
BASE_URL = 'http://apis.data.go.kr/B490001/sjPrecedentInfoService/'
# API Key
# ENCODED_SERVICE_KEY = userkey.encSvcKey
ENCODED_SERVICE_KEY = ''
NUM_OF_ROWS = 300
TIMEOUT = 1000

#연관판결 추출
regex = re.compile(r'(?:연관판결 \: )(.*)(?: ){3,}')


# 판결 유형 조회
def get_precedent_types_a():
    # 유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
    sentence_api_url = BASE_URL + 'getPrecedentResultYuhyeongPstate?ServiceKey={}&pageNo=1&numOfRows=100'

    req_url = sentence_api_url.format(ENCODED_SERVICE_KEY)
    # Timeout 시간은 특별한 기준이 있는 것은 아니고 충분히 넉넉히 부여하였음.
    res = requests.get(req_url, timeout=TIMEOUT)

    soup = BeautifulSoup(res.content, 'lxml')
    items = soup.find_all('kinda')

    sentence_types = []
    for kinda in items:
        sentence_types.append(kinda.string)
    return sentence_types


# 사건 유형 조회
def get_case_types_b():
    # 유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
    case_api_url = BASE_URL + 'getSageonYuhyeongPstate?ServiceKey={}&pageNo=1&numOfRows=100'

    req_url = case_api_url.format(ENCODED_SERVICE_KEY)
    # Timeout 시간은 특별한 기준이 있는 것은 아니고 충분히 넉넉히 부여하였음.
    res = requests.get(req_url, timeout=TIMEOUT)

    soup = BeautifulSoup(res.content, 'lxml')
    items = soup.find_all('kindb')

    case_types = []
    for kindb in items:
        case_types.append(kindb.string)
    return case_types


# 사고/질병 구분 조회
def get_accident_disease_types_c():
    # 유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
    accident_disease_api_url = BASE_URL + 'getSagoJilbyeongGubunPstate?ServiceKey={}&pageNo=1&numOfRows=100'

    req_url = accident_disease_api_url.format(ENCODED_SERVICE_KEY)
    # Timeout 시간은 특별한 기준이 있는 것은 아니고 충분히 넉넉히 부여하였음.
    res = requests.get(req_url, timeout=TIMEOUT)

    soup = BeautifulSoup(res.content, 'lxml')
    items = soup.find_all('kindc')

    accident_disease_types = []
    for kindc in items:
        accident_disease_types.append(kindc.string)
    return accident_disease_types


# 유형별 개수 조회
def get_types_counts(a_types_list, b_types_list, c_types_list):
    types_counts_list = []
    types_count_url = BASE_URL + 'getYuhyeongByCountPstate?serviceKey={}&kindA={}&kindB={}&kindC={}&numOfRows=100&pageNo=1'

    for tA in a_types_list:
        for tB in b_types_list:
            for tC in c_types_list:
                req_url = types_count_url.format(ENCODED_SERVICE_KEY, tA, tB, tC)
                res = requests.get(req_url, timeout=TIMEOUT)

                soup = BeautifulSoup(res.content, 'lxml')
                cnt = int(soup.cnt.string)

                types_counts_list.append([tA, tB, tC, cnt])
                print(tA, tB, tC, cnt)

    return types_counts_list


# 전체 개수 조회
def get_all_cases_counts():
    get_types_count_url = BASE_URL + 'getYuhyeongByCountPstate?serviceKey={}&numOfRows=100&pageNo=1'

    req_url = get_types_count_url.format(ENCODED_SERVICE_KEY)
    res = requests.get(req_url, timeout=TIMEOUT)

    soup = BeautifulSoup(res.content, 'lxml')
    cnt = int(soup.cnt.string)

    return cnt


# 타입별 사건 상세 내용 조회
def get_cases_for_types(counts_for_cases):
    detail_url = BASE_URL + 'getSjPrecedentNaeyongPstate?ServiceKey={}&kindA={}&kindB={}&kindC={}&numOfRows={}&pageNo={}'
    related_key = '연관판결 : '  # 연관판결 정보 포함 여부 확인 키워드
    details_list = []
    for case in counts_for_cases:
        # 사건 개수가 0이면 다음 사건 확인
        if case[3] == 0:
            continue

        # 사건 개수가 0이 아니면 사건 정보들을 추출하여 더함.
        # 한페이지당 100개씩
        num_pages = case[3] // NUM_OF_ROWS

        # 여러 건이 조회 되었을 경우, 페이지 단위로 처리함.
        for pageIdx in range(0, num_pages+1):
            req_url = detail_url.format(ENCODED_SERVICE_KEY, case[0], case[1], case[2], NUM_OF_ROWS, pageIdx + 1)
            res = requests.get(req_url, timeout=TIMEOUT)
            soup = BeautifulSoup(res.content, 'lxml')

            # 조회 된 아이템 처리
            items = soup.find_all('item')
            for item in items:
                case_number = item.accnum.string        # 사건번호
                court_name = item.courtname.string      # 법원명
                ruling_type = item.kinda.string         # 판결 유형
                case_type = item.kindb.string           # 사건 유형
                issue_category = item.kindc.string      # 사고질병 구분
                ruling_text = item.noncontent.string    # 판결문
                case_title = item.title.string

                # 연관 재판 추출
                related_cases = extract_related_cases(ruling_text)
                if related_cases is None:
                    details_list.append([case_number, court_name, ruling_type, case_type, issue_category, ruling_text, case_title, ' '])
                else:
                    details_list.append([case_number, court_name, ruling_type, case_type, issue_category, ruling_text, case_title, related_cases])

        print("Done - ", case)

    return details_list


# 사건 상세 내용 조회
def get_all_cases():
    detail_url = BASE_URL + 'getSjPrecedentNaeyongPstate?ServiceKey={}&numOfRows={}&pageNo={}'
    details_list = []

    # 사건 개수가 0이 아니면 사건 정보들을 추출하여 더함.
    # 한페이지당 100개씩
    num_count = get_all_cases_counts()
    num_pages = num_count // NUM_OF_ROWS

    # 여러 건이 조회 되었을 경우, 페이지 단위로 처리함.
    for pageIdx in range(0, num_pages+1):
        req_url = detail_url.format(ENCODED_SERVICE_KEY, NUM_OF_ROWS, pageIdx + 1)
        res = requests.get(req_url, timeout=TIMEOUT)
        soup = BeautifulSoup(res.content, 'lxml')

        print(pageIdx, num_pages)
        # 조회 된 아이템 처리
        items = soup.find_all('item')
        for item in items:
            case_number = item.accnum.string        # 사건번호
            court_name = item.courtname.string      # 법원명
            ruling_type = "-"                       # 판결 유형
            case_type = "-"                         # 사건 유형
            issue_category = "-"                    # 사고질병 구분

            if item.kinda is not None:
                ruling_type = item.kinda.string

            if item.kindb is not None:
                case_type = item.kindb.string

            if item.kindc is not None:
                issue_category = item.kindc.string

            ruling_text = item.noncontent.string    # 판결문
            case_title = item.title.string          # 제목

            # 연관 재판 추출
            related_cases = extract_related_cases(ruling_text)
            if related_cases is None:
                details_list.append([case_number, court_name, ruling_type, case_type, issue_category, ruling_text, case_title, ' '])
            else:
                details_list.append([case_number, court_name, ruling_type, case_type, issue_category, ruling_text, case_title, related_cases])

    return details_list

# 판결문에서 연관재판 정보 추출 - 없으면 None
def extract_related_cases(ruling_text):
    matched_part = regex.search(ruling_text)
    if matched_part is None:
        return None
    matched_string = matched_part.group()
    return matched_string[6:].strip()

def save_all_cases_excel():
    today = datetime.datetime.today()
    all_cases = get_all_cases()
    df = DataFrame(all_cases, columns=['사건번호', '법원', '판결유형', '사건유형', '사고질병 구분', '판결문', '제목', '연관사건'])
    filename = 'sentence_'+str(today.year)+'_'+str(today.month)+'_'+str(today.day)+'.xlsx'
    df.to_excel(filename, index=False, header=True, encoding='utf8')

def save_all_cases_csv():
    today = datetime.datetime.today()
    all_cases = get_all_cases()
    df = DataFrame(all_cases, columns=['사건번호', '법원', '판결유형', '사건유형', '사고질병 구분', '판결문', '제목', '연관사건'])
    filename = 'sentence_'+str(today.year)+'_'+str(today.month)+'_'+str(today.day)+'.csv'
    df.to_csv(filename, index=False, header=True, encoding='utf8')