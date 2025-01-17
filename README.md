# Industrial_disasters
산업재해 관련 프로젝트 - 판례 분석 등

TODO 라이브러리 사용설명 수정

#  프로젝트의 목적
근로자가 자신에게 발생했거나 발생 할 가능성이 있는 산업재해 판례 정보를 손쉽게 조회 해 볼 수 있는 서비스를 만드는 것이 궁극적인 목표.

# 최근에 내려받은 데이터들
처음에는 빠르게 데이터를 받아 공유하기 위해 로컬에서 돌아가는 로직으로 구현했으나, python 개발 환경이 없는 분들이 쉽게 데이터를 받을 수 있도록 하기 위해 웹 기반의 시스템을 다시 개발하고 있습니다. 시스템 개발 중에 데이터를 새로 받는 경우가 있는데, 개발 환경 없는 분들 중 최신 데이터가 필요한 분들은 아래 공유 폴더에서 데이터를 받아 보시기 바랍니다.
https://drive.google.com/drive/folders/1gKOPq0uhw_P0eIyBnG9eYKw3MhMC1mUE?usp=sharing


## 관련 프로젝트

### 웹 기반 판례 데이터 조회
https://github.com/Code-for-Korea/sanjae.server


###  산재 판례 데이터 수집
https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15041878

근로복지공단_산재보험 판례 판결문 조회 서비스 데이터 활용

- 사용법
 1. api_industrial_disasters.py 에 발급받은 라이센스 키(Encoded)를 extract_sentence_details.py와 같은 위치에 userkey.py라고 만들고, 아래와 같은 변수명에 본인의 키를 설정함.
    
    encSvcKey ='----------YOUR ENCODING KEY-------------------'

 2. extract_sentence_details.py 를 실행함
 3. 각 사건 상세 내용이 기록 된 엑셀 파일이 'sentenc_날짜.xlsx' 형식으로 생성 됨.
 4. 연관 재판 정보는 상세 내용 파일의 마지막 컬럼을 엑셀의 데이터 분리 기능으로 쉼표와 빼기를 구분자로 하여 나누면 됨.

- 보완 할 사항
 1. 추출 된 판례 데이터 자체도 소중하지만, 근로자가 자신과 관련 된 질병에 대한 판례를 검색 해 보는데 활용 할 수 있게 해야 함.
 2. 현재는 이 과정이 수동으로 되고 있기 때문에, 판례 내용에서 검색에 필요한 정보를 추출해 내는 것을 다음 단계의 프로젝트로 정함.

###  산재 판례로부터 검색 키워드 추출

- 추출 할 사항
 1. 관련 재판 정보(완료)
    - XML의 판결문 Tag는 noncontent이며, 관련 재판 정보는 모두 판결문 가장 앞에 있었다. 
    - '연관판결 : '로 시작하며 '주문' 앞까지 관련 재판 정보가 포함되어 있다.
    - 주문의 시작은 '주문'으로 표시 된 것이 대부분이지만, '주 문'인 경우도 있었다.
    - '주문' 혹은 '주 문' 중 발견 된 위치와 '연관판결 : ' 사이의 문구에서 관련 재판 정보를 추출 할 수 있다.
    - '연관판결 : ' 문구가 없는 경우도 있는데, 1심에서 기각 된 경우에는 관련 재판이 없기 때문에 '연관판결 : ' 문구가 없다.
    - 연관판결 문구의 각 재판의 구분은 '-'로 하며, 각 재판의 재판번호/법원명/사건번호는 ','로 구분된다.
    - 연관판결을 셀로 구분하면 컬럼수가 달라지기 때문에, 추출 할 때는 일단 하나의 컬럼에 두고, 재판 구분이 필요할 경우, 엑셀에서 데이터 분리 시 '-'와 ','로 쉽게 분리 할 수 있다.
    - 샘플
     연관판결 : 서울행정법원,20##구단####,1심-대법원,2014두####,3심   주문
     1. 제1심 판결을 취소한다.

 2. 근로자의 직업/ 질병 분류
    - @진하님께서 주신 관련 된 가이드 내용
   
      @바른생활 심원일 네 안녕하세요. 월요일에 포럼 모임 있었습니다.  논의 된 것은 시민들이 찾아 볼 수 있게, 즉 종사자/질병을 키워드로  서치하고 이후 원문을 볼수 있는 방법 논의 되었습니다.    1) 판결문 질병분류 설정은 주로 '이 사건 상병'이라는 키워드 앞에 있는 것 같고, 2) 종사자는 '업무에 종사'하여왔다 앞에 있는 용접일 것 같습니다. 어디는 업무 내용이라는 항에 있고 일정치 않은 것 같습니다.  그리고 데이터 파일 올리겠습니다.
      
@바른생활 심원일 여기 빨간 줄에 있는 것 앞에 '30여 년간 배관설비 및 용접 업무'와 '피부근염'이 업무/질병의 colum 에 값이면 찾기 편할 것 같습니다. (편집됨) 

   - 가이드를 바탕으로 데이터를 검토한 결과
       * 가이드의 형식과 다른 형식들이 많아서 일반화 하기가 어려움.
       * 대법원은 법리적인 검토만을 하기 때문인지 근로 내용이나 질병 관련 언급은 거의 없다.
       * 질병분류의 명칭이 판결문에 그대로 사용되지 않는 경우도 있어서 단순히 그 질병분류의 존재 여부로 판단하는 것은 무리다.
       * 오히려, 근무에 대한 내용이 있을 것으로 추정되는 문장을 자동으로 추출하고, 질병분류와 관련 된 키워드를 자동으로 추출하여 화면에 보여주고, 그 문맥을 바탕으로 판단하여, 입력을 쉽게(클릭 등으로) 해 주는 것이 좋지 않을까???
    - 데이터를 누적 해 나간다면, 앞서 한 작업 결과를 다시 덮어쓰지 않도록 업데이트 하는 처리가 필요하다. 즉, 이전에 받은 데이터에 없는 데이터만 추가하는 방식


