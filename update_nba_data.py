import pandas as pd
import json
import time
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandingsv3

def fetch_and_save_data():
    print("開始獲取 NBA 最新戰力與勝率數據...")
    
    try:
        # 獲取聯盟最新排名與勝率數據
        standings = leaguestandingsv3.LeagueStandingsV3().get_data_frames()[0]
        
        # 篩選我們需要的關鍵欄位
        columns_to_keep = ['TeamName', 'TeamCity', 'WINS', 'LOSSES', 'WinPCT', 'L10', 'Streak']
        df = standings[columns_to_keep]
        
        # 將數據轉換為字典格式，方便未來 APK (APP) 讀取
        data_dict = df.to_dict(orient='records')
        
        final_output = {
            "update_time": pd.Timestamp.now(tz='Asia/Taipei').strftime('%Y-%m-%d %H:%M:%S'),
            "data": data_dict
        }
        
        # 寫入 JSON 檔案
        with open('nba_daily_stats.json', 'w', encoding='utf-8') as f:
            json.dump(final_output, f, ensure_ascii=False, indent=4)
            
        print("✅ 數據收集完成！已儲存為 nba_daily_stats.json")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
