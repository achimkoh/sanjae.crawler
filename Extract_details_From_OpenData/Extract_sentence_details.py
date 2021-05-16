'''
Code for Korea - #p-산업재해
판례 데이터 분석을 위한 판례 데이터 덤프 생성 코드
2021/05/03 바른생활 심원일
'''

import API_Industrial_disasters as API
from pandas import DataFrame    # 코드 없이 데이터 분석을 용이하게 할 수 있도록 엑셀로 저장
import datetime                 # 저장 파일 이름에 날짜 사용

today = datetime.datetime.today()

#-------------------------- 전체 DB 다운로드 받는 것고 직접 연관이 없는 코드는 일단 주석 처리 함 -------------------------------
'''
#### 조회를 위한 세 가지 유형 정보들 조회
# 판결 유형 조회
KindA_precedent_result_type_list = API.get_KindA_PrecedentResult_types()
print(KindA_precedent_result_type_list)

# 사건 유형 조회
KindB_case_type_list = API.get_KindB_case_types()
print(KindB_case_type_list)

# 사고/질병 구분 조회
KindC_AccidentDisease_type_list = API.get_KindC_AccidentDisease_types()
print(KindC_AccidentDisease_type_list)

#### 유형별 사건 개수 조회
counts_for_Cases = API.get_Types_counts(KindA_precedent_result_type_list,KindB_case_type_list,KindC_AccidentDisease_type_list)
# 조회 된 정보 엑셀로 저장
df = DataFrame(counts_for_Cases,columns=['판결유형','사건유형','사고질병 구분','개수'])
filename = 'case_count_'+str(today.year)+'_'+str(today.month)+'_'+str(today.day)+'.xlsx'
df.to_excel(filename,index=False, header=True, encoding='utf8')
'''

#### 사건 상세 내용 조회
# 2021-05-16 세 가지 타입 정보를 넣지 않아도 전체 데이터를 조회 할 수 있다는 achim koh님 조언에 따라, 전체 데이터 조회로 코드 수정
#            이렇게 조회를 하면 두번째나 세번째 타입 정보가 없는 사건들도 있으므로, 예외 처리를 함.

#변경 전 - 각 타입들의 조합으로 데이터 조회하는 방법
#details_for_Cases = API.get_detials_for_Cases(counts_for_Cases)

#변경 후 - 타입 정보 없이 전체 데이터 조회
details_for_Cases = API.get_all_detials_for_Cases()

df = DataFrame(details_for_Cases,columns=['사건번호','법원','판결유형','사건유형','사고질병 구분','판결문','제목','연관사건'])
filename = 'sentence_'+str(today.year)+'_'+str(today.month)+'_'+str(today.day)+'.xlsx'
df.to_excel(filename,index=False, header=True, encoding='utf8')

print("---------------------- 출력 완료 -------------------------")