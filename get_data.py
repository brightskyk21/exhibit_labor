import os
import json
import requests
import pandas as pd
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
    df_age = get_kosis_data("disaster_by_age")
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
        df = pd.DataFrame(data)

        # 데이터 전처리
        if data_key == "업종별":
            # 업종별 데이터 전처리 코드
            pass
        elif data_key == "연령별":
            # 연령별 데이터 전처리 코드
            pass
        elif data_key == "재해정도":
            # 재해정도 데이터 전처리 코드
            pass
        elif data_key == "시간별":
            # 시간별 데이터 전처리 코드
            pass
        elif data_key == "입사근속기간별":
            # 입사근속기간별 데이터 전처리 코드
            pass
        elif data_key == "발생형태별":
            # 발생형태별 데이터 전처리 코드
            pass

        return df
    else:
        raise Exception(f"API 요청 실패 (status {response.status_code})")