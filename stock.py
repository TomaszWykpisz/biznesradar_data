import requests
from bs4 import BeautifulSoup

class Stock():
    
    def __init__(self, n):
        
        self.name = n

        self.domain = "https://www.biznesradar.pl"
        self.f_statement = "/raporty-finansowe-rachunek-zyskow-i-strat/"
        self.b_sheet = "/raporty-finansowe-bilans/"
        self.indicators = "/wskazniki-wartosci-rynkowej/"

        self.date = []

        self.revenue = []
        self.EBIT = []
        self.net_profit = []

        self.c_assets = []
        self.cash = []
        self.total_assets = []
        self.equity = []
        self.c_liabilities = []
        self.c_borrowings = []
        self.non_c_borrowings = []

        self.price = []
        self.share_amount = []
    

    def get_tr_numbers(self, handler, list):

        """ Get values for all Financial Quarters """


        tds = handler.find_all(attrs={"class" : "h"})
        for td in tds:
            value = 0
            h = td.find(attrs={"class" : "value"})
            if h:
                value = h.get_text().replace(" ", "")
                if not value or value == "0.00":
                    value = 0
            list.append(float(value)) 
        


    def get_data_from_f_statement(self):

        """ Get data from Financial Statement Quarterly """


        url = self.domain + self.f_statement + self.name + ",Q"
        re = requests.get(url)
        bs = BeautifulSoup(re.text, 'html.parser')
        
        report_table = bs.find(class_="report-table")
        
        # GET DATES 
        date_tr = report_table.find_all("tr")[0]
        tds = date_tr.find_all(attrs={"class" : "h"})
        for td in tds:
            self.date.append(td.get_text().strip()[:7]) 

        # GET REVENUE 
        revenue_tr = bs.find(attrs={"data-field" : "IncomeRevenues"})
        if not revenue_tr:
            revenue_tr = bs.find(attrs={"data-field" : "IncomeIntrestIncome"})    
        self.get_tr_numbers(revenue_tr, self.revenue)

        # GET EBIT
        EBIT_tr = bs.find(attrs={"data-field" : "IncomeEBIT"})
        if not EBIT_tr:
            EBIT_tr = bs.find(attrs={"data-field" : "IncomeNetoperatingProfit"})
        self.get_tr_numbers(EBIT_tr, self.EBIT)

        # GET NET PROFIT
        net_profit_tr = bs.find(attrs={"data-field" : "IncomeNetProfit"})
        self.get_tr_numbers(net_profit_tr, self.net_profit)
        

    def get_data_from_b_sheet(self):

        """ Get data from Balance Sheet Quarterly """


        url = self.domain + self.b_sheet + self.name + ",Q,0"
        re = requests.get(url)
        bs = BeautifulSoup(re.text, 'html.parser')
        
        report_table = bs.find(class_="report-table")

        # GET CURRENT ASSETS
        c_assets_tr = bs.find(attrs={"data-field" : "BalanceCurrentAssets"})
        self.get_tr_numbers(c_assets_tr, self.c_assets)

        # GET CASH
        cash_tr = bs.find(attrs={"data-field" : "BalanceCash"})
        self.get_tr_numbers(cash_tr, self.cash)

        # GET TOTAL ASSETS
        total_assets_tr = bs.find(attrs={"data-field" : "BalanceTotalAssets"})
        self.get_tr_numbers(total_assets_tr, self.total_assets)

        # GET EQUITY
        equity_tr = bs.find(attrs={"data-field" : "BalanceCapital"})
        self.get_tr_numbers(equity_tr, self.equity)

        # GET CURRENT LIABILITIES
        c_liabilities_tr = bs.find(attrs={"data-field" : "BalanceCurrentLiabilities"})
        self.get_tr_numbers(c_liabilities_tr, self.c_liabilities)

        # GET CURRENT BORROWINGS
        c_borrowings_tr = bs.find(attrs={"data-field" : "BalanceCurrentBorrowings"})
        self.get_tr_numbers(c_borrowings_tr, self.c_borrowings)

        # GET NON CURRENT BORROWINGS
        non_c_borrowings_tr = bs.find(attrs={"data-field" : "BalanceNoncurrentBorrowings"})
        self.get_tr_numbers(non_c_borrowings_tr, self.non_c_borrowings)


    def get_data_from_indicators(self):

        """ Get data from Indicators Quarterly """
        

        url = self.domain + self.indicators + self.name
        re = requests.get(url)
        bs = BeautifulSoup(re.text, 'html.parser')
        
        report_table = bs.find(class_="report-table")
        
        # GET HISTORICAL SHARE PRICE
        price_tr = bs.find(attrs={"data-field" : "Quote"})
        self.get_tr_numbers(price_tr, self.price)

        # GET HISTORICAL SHARE AMOUNT 
        share_amount_tr = bs.find(attrs={"data-field" : "ShareAmount"})
        self.get_tr_numbers(share_amount_tr, self.share_amount)


    def save_to_file(self):

        """ Save data in csv format """


        f = open("data/" + self.name + ".csv", "w")
        f.write("date;" + ";".join(str(d) for d in self.date) + "\n")
        f.write("price;" + ";".join(str(d) for d in self.price) + "\n")
        f.write("share_amount;" + ";".join(str(d) for d in self.share_amount) + "\n")
        f.write("revenue;" + ";".join(str(d) for d in self.revenue)  + "\n")
        f.write("EBIT;" + ";".join(str(d) for d in self.EBIT)  + "\n")
        f.write("net_profit;" + ";".join(str(d) for d in self.net_profit)  + "\n")
        f.write("c_assets;" + ";".join(str(d) for d in self.c_assets)  + "\n")
        f.write("cash;" + ";".join(str(d) for d in self.cash)  + "\n")
        f.write("total_assets;" + ";".join(str(d) for d in self.total_assets)  + "\n")
        f.write("equity;" + ";".join(str(d) for d in self.equity)  + "\n")
        f.write("c_liabilities;" + ";".join(str(d) for d in self.c_liabilities)  + "\n")
        f.write("c_borrowings;" + ";".join(str(d) for d in self.c_borrowings)  + "\n")
        f.write("non_c_borrowings;" + ";".join(str(d) for d in self.non_c_borrowings)  + "\n")


    def check_length(self):

        """ Check if all data list have same length otherwise add empty values """


        ld = len(self.date)
        lp = len(self.price)
        if ld != lp:
            t = ld - lp
            while t > 0:
                print("ADD 1 to " + self.name)
                self.price.insert(0, 0.0)
                self.share_amount.insert(0, 0.0)
                t -= 1
        ld = len(self.date)
        lp = len(self.price)
        if ld != lp:
            print(f"CHECK {self.name} \n")


    def get_data(self):

        """ Get important data from biznesradar and save to csv """


        self.get_data_from_f_statement()
        self.get_data_from_b_sheet()
        self.get_data_from_indicators()
        self.check_length()
        self.save_to_file()
    
        

