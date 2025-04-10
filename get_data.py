import os
import json
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API_KEY 불러오기
API_KEY = os.getenv("API_KEY")

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def get_kosis_data(data_key: str) -> pd.DataFrame:
    """
    config.json에 있는 URL 템플릿에서 apiKey를 끼워넣고 데이터를 DataFrame으로 반환
    config.json에 있는 URL 참고

    사용 예시:
    df_age = get_kosis_data("연령별")
    """
    if data_key not in config["urls"]:
        raise ValueError(f"'{data_key}'는 config.json에 정의되어 있지 않습니다.")

    # API URL 생성
    url_template = config["urls"][data_key]
    full_url = url_template.format(apikey=API_KEY)

    # API 호출
    response = requests.get(full_url)
    if response.status_code == 200:
        data = response.json()
        
        # KOSIS API 응답 데이터 구조에 맞게 DataFrame 생성
        if isinstance(data, dict):
            if 'row' in data:
                df = pd.DataFrame(data['row'])
            else:
                # 딕셔너리 형태의 데이터를 리스트로 변환
                df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            raise ValueError("API 응답 데이터 형식이 예상과 다릅니다.")
            
        # 데이터 전처리
        if data_key == "업종별":
            # 업종별 데이터 전처리 코드
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '항목', '값', '단위']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            pass
        elif data_key == "연령별":
            # 연령별 데이터 전처리 코드
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'C2_NM': '연령대', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '연령대', '값']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            pass
        elif data_key == "재해정도":
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'C2_NM': '재해정도', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '재해정도', '값']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            # 재해정도 데이터 전처리 코드
            pass
        elif data_key == "시간별":
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'C2_NM': '시간', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '시간', '값']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            # 시간별 데이터 전처리 코드
            pass
        elif data_key == "입사근속기간별":
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'C2_NM': '입사근속기간', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '입사근속기간', '값']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            # 입사근속기간별 데이터 전처리 코드
            pass
        elif data_key == "발생형태별":
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'C2_NM': '발생형태', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '발생형태', '값']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            # 발생형태별 데이터 전처리 코드
            pass
        elif data_key == "규모별":
            df = df.rename(columns={'DT': '값', 'PRD_DE': '기준년도', 'C1_NM': '산업', 'C2_NM': '규모', 'UNIT_NM': '단위', 'ITM_NM': '항목'})
            df = df[['기준년도', '산업', '규모', '항목', '값', '단위']]
            df['값'] = df['값'].replace('-', np.nan).astype(float)
            # 규모별 데이터 전처리 코드
            pass

        return df
    else:
        raise Exception(f"API 요청 실패 (status {response.status_code})")