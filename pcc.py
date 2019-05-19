import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

class tender():
    def __init__(self, search_keyword):
        self.search_keyword = search_keyword
        self.url = r"https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic"
        search_StartDate = str(datetime.datetime.now() - datetime.timedelta(days=7))[:10].split("-")
        search_StartDate = str(int(search_StartDate[0])-1911) + "/" + search_StartDate[1] + "/" + search_StartDate[2]
        self.search_StartDate = search_StartDate
        search_EndDate = str(datetime.datetime.now())[:10].split("-")
        search_EndDate = str(int(search_EndDate[0])-1911) + "/" + search_EndDate[1] + "/" + search_EndDate[2]
        self.search_EndDate = search_EndDate

    def search(self):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        data = {"method" : "search", "searchMethod" : True, "hid_1" : 1, "tenderName" : self.search_keyword, "tenderType" : "tenderDeclaration", "tenderWay" : "1,2,3,4,5,6,7,10,12", "tenderDateRadio" : "on", "tenderStartDateStr" : self.search_StartDate, "tenderEndDateStr" : self.search_EndDate, "tenderStartDate" : self.search_StartDate, "tenderEndDate" : self.search_EndDate, "isSpdt" : "N", "treaties" : "GPA", "treaties" : "ANZTEC", "treaties" : "ASTEP", "btnQuery" : "查詢"}
        session = requests.Session()
        resp = session.post(self.url, headers=headers, data=data)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        soup = soup.find_all("table", {"style":"word-break:break-all"})[0]
        table_text = soup.find_all("td")[:-1]
        result_table = pd.DataFrame(index=range(int(len(table_text)/9)-1), columns=["項次","機關名稱","標案案號 // 標案名稱","傳輸次數","招標方式","採購性質","公告日期","截止投標","預算金額"])
        for i in range(1, int(len(table_text)/9)):
            result_table.iloc[i-1,0] = "".join(table_text[(9*i)+0].get_text().split())
            result_table.iloc[i-1,1] = "".join(table_text[(9*i)+1].get_text().split())
            result_table.iloc[i-1,2] = " // ".join(table_text[(9*i)+2].get_text().split())
            result_table.iloc[i-1,3] = "".join(table_text[(9*i)+3].get_text().split())
            result_table.iloc[i-1,4] = "".join(table_text[(9*i)+4].get_text().split())
            result_table.iloc[i-1,5] = "".join(table_text[(9*i)+5].get_text().split())
            result_table.iloc[i-1,6] = "".join(table_text[(9*i)+6].get_text().split())
            result_table.iloc[i-1,7] = "".join(table_text[(9*i)+7].get_text().split())
            result_table.iloc[i-1,8] = "".join(table_text[(9*i)+8].get_text().split())
        return result_table

    def message(self, result_table):
        if len(result_table) <= 100:
            case_num = str(len(result_table))
        else:
            case_num = "超過100"
        case_list = list(result_table.iloc[:,2].values)
        case_name = [i.split("//")[-1] for i in case_list]
        article_content = self.search_StartDate + " 到 " + self.search_EndDate + "\n \"" + self.search_keyword + "\" 共" + case_num + "條搜尋結果\n\n" + "\n\n".join(case_name)
        return article_content
