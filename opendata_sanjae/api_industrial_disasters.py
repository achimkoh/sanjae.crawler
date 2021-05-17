import requests                 # API 연결
from bs4 import BeautifulSoup   # XML 파싱
import re                       # 정규식으로 정보 추출
import datetime                 # 저장 파일 이름에 날짜 사용

class API:
    # API Base URL
    BASE_URL = 'http://apis.data.go.kr/B490001/sjPrecedentInfoService/'
    # API Key: 인스턴스 생성 후 지정해주어야 함.
    ENCODED_SERVICE_KEY = ''
    NUM_OF_ROWS = 100

    # 판결 유형 조회
    def get_precedent_types_a(self):
        # 유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
        sentence_api_url = self.BASE_URL + 'getPrecedentResultYuhyeongPstate?ServiceKey={}&pageNo=1&numOfRows=100'
        req_url = sentence_api_url.format(self.ENCODED_SERVICE_KEY)
        res = requests.get(req_url)
        soup = BeautifulSoup(res.content, 'lxml')
        items = soup.find_all('kinda')

        sentence_types = []
        for kinda in items:
            sentence_types.append(kinda.string)
        return sentence_types


    # 사건 유형 조회
    def get_case_types_b(self):
        # 유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
        case_api_url = self.BASE_URL + 'getSageonYuhyeongPstate?ServiceKey={}&pageNo=1&numOfRows=100'
        req_url = case_api_url.format(self.ENCODED_SERVICE_KEY)
        res = requests.get(req_url)
        soup = BeautifulSoup(res.content, 'lxml')
        items = soup.find_all('kindb')

        case_types = []
        for kindb in items:
            case_types.append(kindb.string)
        return case_types


    # 사고/질병 구분 조회
    def get_accident_disease_types_c(self):
        # 유형의 개수가 많지 않으므로 한 페이지에 다 조회 되도록 함
        accident_disease_api_url = self.BASE_URL + 'getSagoJilbyeongGubunPstate?ServiceKey={}&pageNo=1&numOfRows=100'
        req_url = accident_disease_api_url.format(self.ENCODED_SERVICE_KEY)
        res = requests.get(req_url)
        soup = BeautifulSoup(res.content, 'lxml')
        items = soup.find_all('kindc')

        accident_disease_types = []
        for kindc in items:
            accident_disease_types.append(kindc.string)
        return accident_disease_types


    # 유형별 개수 조회
    def get_types_counts(a_types_list, b_types_list, c_types_list):
        types_counts_list = []
        types_count_url = self.BASE_URL + 'getYuhyeongByCountPstate?serviceKey={}&kindA={}&kindB={}&kindC={}&numOfRows=100&pageNo=1'

        for tA in a_types_list:
            for tB in b_types_list:
                for tC in c_types_list:
                    req_url = types_count_url.format(self.ENCODED_SERVICE_KEY, tA, tB, tC)
                    res = requests.get(req_url)

                    soup = BeautifulSoup(res.content, 'lxml')
                    cnt = int(soup.cnt.string)

                    types_counts_list.append([tA, tB, tC, cnt])
                    print(tA, tB, tC, cnt)

        return types_counts_list

    # 전체 개수 조회
    def get_all_cases_counts(self):
        get_types_count_url = self.BASE_URL + 'getYuhyeongByCountPstate?serviceKey={}&numOfRows=100&pageNo=1'
        req_url = get_types_count_url.format(self.ENCODED_SERVICE_KEY)
        res = requests.get(req_url)
        soup = BeautifulSoup(res.content, 'lxml')
        cnt = int(soup.cnt.string)

        return cnt

    # 사건 상세 내용 조회
    def get_all_cases(self):
        detail_url = self.BASE_URL + 'getSjPrecedentNaeyongPstate?ServiceKey={}&numOfRows={}&pageNo={}'
        details_list = []

        # 사건 개수가 0이 아니면 사건 정보들을 추출하여 더함.
        # 한페이지당 100개씩
        num_count = self.get_all_cases_counts()
        num_pages = (num_count // self.NUM_OF_ROWS) + 1

        # 여러 건이 조회 되었을 경우, 페이지 단위로 처리함.
        for pageIdx in range(1, num_pages+1):
            req_url = detail_url.format(self.ENCODED_SERVICE_KEY, self.NUM_OF_ROWS, pageIdx)
            res = requests.get(req_url)
            soup = BeautifulSoup(res.content, 'lxml')

            print(pageIdx, '/', num_pages)
            # 조회 된 아이템 처리
            items = soup.find_all('item')
            for item in items:
                case_number = item.accnum.string if item.accnum else ''         # 사건번호
                court_name = item.courtname.string if item.courtname else ''    # 법원명
                court_name = court_name.replace(' ', '')                        # 법원명에서 공백을 제거한다
                ruling_type = item.kinda.string if item.kinda else ''           # 판결 유형
                case_type = item.kindb.string if item.kindb else ''             # 사건 유형
                issue_category = item.kindc.string if item.kindc else ''        # 사고질병 구분
                ruling_text = item.noncontent.string if item.noncontent else ''  # 판결문
                case_title = item.title.string if item.title else ''                 # 제목

                # 연관 재판 추출
                related_cases = self.extract_related_cases(ruling_text)
                details_list.append([case_number, court_name, ruling_type, case_type, issue_category, ruling_text, case_title, related_cases])

        return details_list

    # 판결문에서 연관재판 정보 추출 - 없으면 빈 문자열
    def extract_related_cases(self, ruling_text):
        # 연관판결 추출
        pattern = re.compile(r'(?:연관판결 \: )(.*)(?: ){3,}')

        match_result = pattern.search(ruling_text)
        if match_result is None:
            return ''
        return match_result.group(1)
