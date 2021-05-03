# Industrial_disasters
산업재해 관련 프로젝트 - 판례 분석 등

#  산재 판례 데이터 수집
https://github.com/Code-for-Korea/Industrial_disasters
근로복지공단_산재보험 판례 판결문 조회 서비스 데이터 활용

- 사용법
 1. API_Industrial_disasters.py 에 발급받은 라이센스 키(Encoded)를 설정함.
 2. Extract_sentence_details.py 를 실행함
 3. 유형별 사건 개수와 각 사건 상세 내용이 기록 된 엑셀 파일이 2개 생성 됨.
 4. 연관 재판 정보는 상세 내용 파일의 마지막 컬럼을 엑셀의 데이터 분리 기능으로 쉼표와 빼기를 구분자로 하여 나누면 됨.
 