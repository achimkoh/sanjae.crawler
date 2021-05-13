'''
Code for Korea - #p-산업재해
판례 데이터 분석을 위한 판례 데이터 덤프 생성 코드
2021/05/03 바른생활 심원일
'''

import API_Industrial_disasters as API
from pandas import DataFrame    # 코드 없이 데이터 분석을 용이하게 할 수 있도록 엑셀로 저장
import datetime                 # 저장 파일 이름에 날짜 사용

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
today = datetime.datetime.today()
filename = 'case_count_'+str(today.year)+'_'+str(today.month)+'_'+str(today.day)+'.xlsx'
df.to_excel(filename,index=False, header=True, encoding='utf8')

#### 사건 상세 내용 조회
details_for_Cases = API.get_detials_for_Cases(counts_for_Cases)

df = DataFrame(details_for_Cases,columns=['사건번호','법원','판결유형','사건유형','사고질병 구분','판결문','제목','연관사건'])
filename = 'sentence_'+str(today.year)+'_'+str(today.month)+'_'+str(today.day)+'.xlsx'
df.to_excel(filename,index=False, header=True, encoding='utf8')

print("---------------------- 출력 완료 -------------------------")