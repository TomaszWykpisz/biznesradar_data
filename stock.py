import requests
from bs4 import BeautifulSoup
import pandas as pd

class Stock():
    
    def __init__(self, n):
        
        self.name = n
        self.current_price = 0
        self.df = {}

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
        f.close()


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
    

    def read_data_from_csv_to_DF(self):

        """ Reading data from a csv that has been previously saved"""

        po = {}
        f = open(f'data/{self.name}.csv', "r")
        lines = f.readlines()

        for line in lines:
            data = line.strip().split(";")
            if data[0] == "date":
                d = data[1:]
            elif data[0] in ['share_amount', 'price']:
                d = [float(x) for x in data[1:]]
            else:
                d = [float(x)*1000 for x in data[1:]]
            po[data[0]] = d
        f.close()

        self.df = pd.DataFrame(po)
        self.add_ttm_to_DF()
        self.add_indicators_to_DF()

    
    def add_ttm_to_DF(self):

        """ Adding trailing twelve months to DataFrame 
            Revenue TTM
            EBIT TTM
            Net profit TTM
        """

        rev_ttm = [0,0,0]
        ebit_ttm = [0,0,0]
        net_ttm = [0,0,0]
        
        rev = self.df['revenue']
        ebit = self.df['EBIT']
        net = self.df['net_profit']

        for index, row in self.df.iterrows():

            if index > 2:
                rev_ttm.append(rev[index] + rev[index-1] + rev[index-2] + rev[index-3])
                ebit_ttm.append(ebit[index] + ebit[index-1] + ebit[index-2] + ebit[index-3])
                net_ttm.append(net[index] + net[index-1] + net[index-2] + net[index-3])
            
        self.df['revenue_ttm'] = rev_ttm
        self.df['EBIT_ttm'] = ebit_ttm
        self.df['net_profit_ttm'] = net_ttm


    def add_indicators_to_DF(self):

        """ Adding indicators to DataFrame 
            EV, EV/EBIT
            Working capital, EBIT/Working capital
            EPS, P/E
            Current Ratio
        """

        self.df['EV'] = self.df['share_amount'] \
            * self.df['price'] \
            + self.df['c_borrowings'] \
            + self.df['non_c_borrowings'] \
            - self.df['cash']

        self.df['EV/EBIT'] = self.df['EV'] / self.df['EBIT_ttm']

        self.df['working capital'] = self.df['c_assets'] - self.df['c_liabilities']
        self.df['EBIT/working capital'] = self.df['EBIT_ttm'] / self.df['working capital']

        self.df['EPS'] = self.df['net_profit_ttm'] / self.df['share_amount']
        self.df['P/E'] = self.df['price'] / self.df['EPS']

        self.df['current ratio'] = self.df['c_assets'] / self.df['c_liabilities']


    def set_current_price(self, price):

        self.current_price = price


    def weighted_mean(self, mean, median):

        return (mean + median * 9) / 10

    def length_to_look_back(self):

        """ How many financial quarters look back"""

        l = 0
        le = len(self.df)

        if le > 50: l = 40
        elif le > 30: l = 20
        elif le > 15: l = 12
        else: return 0

        return l


    def estimate_price_PE(self, PE):

        """ Estimate price according to given P/E indicator """

        net = self.df['net_profit_ttm'].iat[-1]
        share = self.df['share_amount'].iat[-1]

        return PE * (net / share)


    def estimate_price_PE_history(self):

        """ Estimate price according to historical P/E indicator """

        l = self.length_to_look_back()
        if not l: return 0
        
        mean = self.df['P/E'][-l:].mean()
        median = self.df['P/E'][-l:].describe()['50%']

        return self.estimate_price_PE(self.weighted_mean(mean, median))


    def estimate_price_EVEBIT(self, EVEBIT):

        """ Estimate price according to given EV/EBIT indicator """
        
        EBIT = self.df['EBIT_ttm'].iat[-1]
        cash = self.df['cash'].iat[-1]
        c_bor = self.df['c_borrowings'].iat[-1]
        non_c_bor = self.df['non_c_borrowings'].iat[-1]
        share = self.df['share_amount'].iat[-1]

        return (EVEBIT * EBIT - c_bor - non_c_bor + cash) / share


    def estimate_price_EVEBIT_history(self):

        """ Estimate price according to historical EV/EBIT indicator """

        l = self.length_to_look_back()
        if not l: return 0

        mean = self.df['EV/EBIT'][-l:].mean()
        median = self.df['EV/EBIT'][-l:].describe()['50%']

        return self.estimate_price_EVEBIT(self.weighted_mean(mean, median))