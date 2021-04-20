import sqlite3
from prettytable import PrettyTable
import plotly.graph_objs as go

#Name: Yi Cao
#uniqname: yiicao

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'

# Part 1: Implement logic to process user commands
def find_1(e):
    return e[1]
def find_2(e):
    return e[2]
def find_3(e):
    return e[3]
def find_4(e):
    return e[4]

def process_command(command):
    number_string_list = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25',
    '26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50']
    
    conn = sqlite3.connect('choc.sqlite')
    
    command_list = command.split()

    results = []
    q_country = '''
    SELECT Id, Alpha2, EnglishName, Region
    FROM Countries
    ORDER BY Id 
    '''
    cur_countries = conn.cursor()
    cur_countries.execute(q_country)
    
    filtered_countries = []
    filtered_data = []

    if command_list[0] == "bars":
        q_bars = '''
        SELECT Bars.SpecificBeanBarName, Bars.Company, sell.EnglishName, Bars.Rating, Bars.CocoaPercent, source.EnglishName
		FROM Bars
		JOIN Countries AS sell ON Bars.CompanyLocationId = sell.Id 
		JOIN Countries AS source ON Bars.BroadBeanOriginId = source.Id
        ORDER BY Bars.Id
        '''
        cur_bars = conn.cursor()
        cur_bars.execute(q_bars)

        if 'country' in command:
            for each in command_list:
                if 'country' == each[:7]:
                    alpha2 = each[8:]
            for every in cur_countries:
                if alpha2 == every[1]:
                    country = every[2]
            if 'sell' in command_list:
                for data in cur_bars:
                    if country == data[2]:
                        filtered_data.append(data)
            if 'source' in command_list:
                for data in cur_bars:
                    if country == data[-1]:
                        filtered_data.append(data)
            if 'sell' not in command_list and 'source' not in command_list:
                for data in cur_bars:
                    if country == data[2]:
                        filtered_data.append(data)

        if 'region' in command:
            for each in command_list:
                if 'region' == each[:6]:
                    continent = each[7:]
            for every in cur_countries:
                if continent == every[3]:
                    filtered_countries.append(every[2])
            if 'sell' in command_list:
                for data in cur_bars:
                    if data[2] in filtered_countries:
                        filtered_data.append(data)
            if 'source' in command_list:
                for data in cur_bars:
                    if data[-1] in filtered_countries:
                        filtered_data.append(data)
            if 'sell' not in command_list and 'source' not in command_list:
                for data in cur_bars:
                    if data[2] in filtered_countries:
                        filtered_data.append(data)
        
        if 'country' not in command and 'region' not in command:
            for data in cur_bars:
                filtered_data.append(data)


        if 'ratings' in command_list:
            if 'top' in command_list:
                filtered_data.sort(key=find_3, reverse=True)
            if 'bottom' in command_list:
                filtered_data.sort(key=find_3)
            if 'top' not in command_list and 'bottom' not in command_list:
                filtered_data.sort(key=find_3, reverse=True)
        if 'cocoa' in command_list:
            if 'top' in command_list:
                filtered_data.sort(key=find_4, reverse=True)
            if 'bottom' in command_list:
                filtered_data.sort(key=find_4)
            if 'top' not in command_list and 'bottom' not in command_list:
                filtered_data.sort(key=find_4, reverse=True)
        if 'ratings' not in command_list and 'cocoa' not in command_list:
            if 'top' in command_list:
                filtered_data.sort(key=find_3, reverse=True)
            if 'bottom' in command_list:
                filtered_data.sort(key=find_3)
            if 'top' not in command_list and 'bottom' not in command_list:
                filtered_data.sort(key=find_3, reverse=True)

        
        if command_list[-1] in number_string_list:
            results = filtered_data[0:int(command_list[-1])]
        if command_list[-1] not in number_string_list:
            results = filtered_data[0:10]

    if command_list[0] == 'companies':
        q_companies_rating = '''
        SELECT Bars.Company, Countries.EnglishName, AVG(Bars.Rating)
        FROM Bars
        JOIN Countries ON Bars.CompanyLocationId = Countries.Id
	    GROUP BY Bars.Company
	    HAVING COUNT(*) > 4
	    ORDER BY Bars.Id
        '''
        cur_companies_rating = conn.cursor()
        cur_companies_rating.execute(q_companies_rating)
        
        q_companies_cocoa = '''
        SELECT Bars.Company, Countries.EnglishName, AVG(Bars.CocoaPercent)
        FROM Bars
        JOIN Countries ON Bars.CompanyLocationId = Countries.Id
	    GROUP BY Bars.Company
        HAVING COUNT(*) > 4
	    ORDER BY Bars.Id
        '''
        cur_companies_cocoa = conn.cursor()
        cur_companies_cocoa.execute(q_companies_cocoa)

        q_companies_count = '''
        SELECT Bars.Company, Countries.EnglishName, COUNT(*)
        FROM Bars
        JOIN Countries ON Bars.CompanyLocationId = Countries.Id
	    GROUP BY Bars.Company
	    HAVING COUNT(*) > 4
	    ORDER BY Bars.Id
        '''
        cur_companies_count = conn.cursor()
        cur_companies_count.execute(q_companies_count)

        if 'country' in command:
            for each in command_list:
                if 'country' == each[:7]:
                    alpha2 = each[8:]
            for every in cur_countries:
                if alpha2 == every[1]:
                    country = every[2]
            if 'ratings' in command_list:
                for data in cur_companies_rating:
                    if country == data[1]:
                        filtered_data.append(data)
            if 'cocoa' in command_list:
                for data in cur_companies_cocoa:
                    if country == data[1]:
                        filtered_data.append(data)
            if 'number_of_bars' in command_list:
                for data in cur_companies_count:
                    if country == data[1]:
                        filtered_data.append(data)
            if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                for data in cur_companies_rating:
                    if country == data[1]:
                        filtered_data.append(data)
        
        if 'region' in command:
            for each in command_list:
                if 'region' == each[:6]:
                    continent = each[7:]
            for every in cur_countries:
                if continent == every[3]:
                    filtered_countries.append(every[2])
            if 'ratings' in command_list:
                for data in cur_companies_rating:
                    if data[1] in filtered_countries:
                        filtered_data.append(data)
            if 'cocoa' in command_list:
                for data in cur_companies_cocoa:
                    if data[1] in filtered_countries:
                        filtered_data.append(data)
            if 'number_of_bars' in command_list:
                for data in cur_companies_count:
                    if data[1] in filtered_countries:
                        filtered_data.append(data)
            if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                for data in cur_companies_rating:
                    if data[1] in filtered_countries:
                        filtered_data.append(data)
        
        if 'country' not in command and 'region' not in command:
            if 'ratings' in command_list:
                for data in cur_companies_rating:
                    filtered_data.append(data)
            if 'cocoa' in command_list:
                for data in cur_companies_cocoa:
                    filtered_data.append(data)
            if 'number_of_bars' in command_list:
                for data in cur_companies_count:
                    filtered_data.append(data)
            if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                for data in cur_companies_rating:
                    filtered_data.append(data)
        
        if 'top' in command_list:
            filtered_data.sort(key=find_2, reverse=True)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]
        if 'bottom' in command_list:
            filtered_data.sort(key=find_2)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]
        if 'top' not in command_list and 'bottom' not in command_list:
            filtered_data.sort(key=find_2, reverse=True)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]

    if command_list[0] == 'countries':
        q_countries_sell_rating = '''
        SELECT Countries.EnglishName, Countries.Region, AVG(Bars.Rating) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.CompanyLocationId
        GROUP BY Countries.EnglishName
        HAVING COUNT(*) > 4
        ORDER BY Countries.Id
        '''
        cur_countries_sell_rating = conn.cursor()
        cur_countries_sell_rating.execute(q_countries_sell_rating)

        q_countries_sell_cocoa = '''
        SELECT Countries.EnglishName, Countries.Region, AVG(Bars.CocoaPercent) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.CompanyLocationId
        GROUP BY Countries.EnglishName
        HAVING COUNT(*) > 4
        ORDER BY Countries.Id
        '''
        cur_countries_sell_cocoa = conn.cursor()
        cur_countries_sell_cocoa.execute(q_countries_sell_cocoa)

        q_countries_sell_number = '''
        SELECT Countries.EnglishName, Countries.Region, COUNT(*) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.CompanyLocationId
        GROUP BY Countries.EnglishName
        HAVING COUNT(*) > 4
        ORDER BY Countries.Id
        '''
        cur_countries_sell_number = conn.cursor()
        cur_countries_sell_number.execute(q_countries_sell_number)
        
        q_countries_source_rating = '''
        SELECT Countries.EnglishName, Countries.Region, AVG(Bars.Rating)
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId
        GROUP BY Countries.EnglishName
        HAVING COUNT(*) > 4
        ORDER BY Countries.Id
        '''
        cur_countries_source_rating = conn.cursor()
        cur_countries_source_rating.execute(q_countries_source_rating)

        q_countries_source_cocoa = '''
        SELECT Countries.EnglishName, Countries.Region, AVG(Bars.CocoaPercent)
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId
        GROUP BY Countries.EnglishName
        HAVING COUNT(*) > 4
        ORDER BY Countries.Id
        '''
        cur_countries_source_cocoa = conn.cursor()
        cur_countries_source_cocoa.execute(q_countries_source_cocoa)
        
        q_countries_source_number = '''
        SELECT Countries.EnglishName, Countries.Region, COUNT(*) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId
        GROUP BY Countries.EnglishName
        HAVING COUNT(*) > 4
        ORDER BY Countries.Id
        '''
        cur_countries_source_number = conn.cursor()
        cur_countries_source_number.execute(q_countries_source_number)

        if 'region' in command:
            for each in command_list:
                if 'region' in each:
                    continent = each[7:]
            if 'sell' in command_list:
                if 'ratings' in command_list:
                    for data in cur_countries_sell_rating:
                        if data[1] == continent:
                            filtered_data.append(data)
            if 'cocoa' in command_list:
                for data in cur_countries_sell_cocoa:
                    if data[1] == continent:
                        filtered_data.append(data)
            if 'number_of_bars' in command_list:
                for data in cur_countries_sell_number:
                    if data[1] == continent:
                        filtered_data.append(data)
            if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                for data in cur_countries_sell_rating:
                    if data[1] == continent:
                        filtered_data.append(data)
            if 'source' in command_list:
                if 'ratings' in command_list:
                    for data in cur_countries_source_rating:
                        if data[1] == continent:
                            filtered_data.append(data)
                if 'cocoa' in command_list:
                    for data in cur_countries_source_cocoa:
                        if data[1] == continent:
                            filtered_data.append(data)
                if 'number_of_bars' in command_list:
                    for data in cur_countries_source_number:
                        if data[1] == continent:
                            filtered_data.append(data)
                if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                    for data in cur_countries_source_rating:
                        if data[1] == continent:
                            filtered_data.append(data)
        
        if 'region' not in command:
            if 'sell' in command_list:
                if 'ratings' in command_list:
                    for data in cur_countries_sell_rating:
                        filtered_data.append(data)
                if 'cocoa' in command_list:
                    for data in cur_countries_sell_cocoa:
                        filtered_data.append(data)
                if 'number_of_bars' in command_list:
                    for data in cur_countries_sell_number:
                        filtered_data.append(data)
                if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                    for data in cur_countries_sell_rating:
                        filtered_data.append(data)
            if 'source' in command_list:
                if 'ratings' in command_list:
                    for data in cur_countries_source_rating:
                        filtered_data.append(data)
                if 'cocoa' in command_list:
                    for data in cur_countries_source_cocoa:
                        filtered_data.append(data)
                if 'number_of_bars' in command_list:
                    for data in cur_countries_source_number:
                        filtered_data.append(data)
                if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                    for data in cur_countries_source_rating:
                        filtered_data.append(data)
        
        if 'top' in command_list:
            filtered_data.sort(key=find_2, reverse=True)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]
        if 'bottom' in command_list:
            filtered_data.sort(key=find_2)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]
        if 'top' not in command_list and 'bottom' not in command_list:
            filtered_data.sort(key=find_2, reverse=True)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]

    if command_list[0] == 'regions':
        q_region_sell_rating = '''
        SELECT Countries.Region, AVG(Bars.Rating) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.CompanyLocationId
        GROUP BY Countries.Region
        HAVING COUNT(*) > 4
        '''
        cur_region_sell_rating = conn.cursor()
        cur_region_sell_rating.execute(q_region_sell_rating)

        q_region_sell_cocoa = '''
        SELECT Countries.Region, AVG(Bars.CocoaPercent) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.CompanyLocationId
        GROUP BY Countries.Region
        HAVING COUNT(*) > 4
        '''
        cur_region_sell_cocoa = conn.cursor()
        cur_region_sell_cocoa.execute(q_region_sell_cocoa)

        q_region_sell_number = '''
        SELECT Countries.Region, COUNT(*) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.CompanyLocationId
        GROUP BY Countries.Region
        HAVING COUNT(*) > 4
        '''
        cur_region_sell_number = conn.cursor()
        cur_region_sell_number.execute(q_region_sell_number)

        q_region_source_rating = '''
        SELECT Countries.Region, AVG(Bars.Rating)
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId
        GROUP BY Countries.Region
        HAVING COUNT(*) > 4
        '''
        cur_region_source_rating = conn.cursor()
        cur_region_source_rating.execute(q_region_source_rating)

        q_region_source_cocoa = '''
        SELECT Countries.Region, AVG(Bars.CocoaPercent)
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId
        GROUP BY Countries.Region
        HAVING COUNT(*) > 4
        '''
        cur_region_source_cocoa = conn.cursor()
        cur_region_source_cocoa.execute(q_region_source_cocoa)

        q_region_source_number = '''
        SELECT Countries.Region, COUNT(*) 
        FROM Countries
        JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId
        GROUP BY Countries.Region
        HAVING COUNT(*) > 4
        '''
        cur_region_source_number = conn.cursor()
        cur_region_source_number.execute(q_region_source_number)

        if 'sell' in command_list:
            if 'ratings' in command_list:
                for data in cur_region_sell_rating:
                    filtered_data.append(data)
            if 'cocoa' in command_list:
                for data in cur_region_sell_cocoa:
                    filtered_data.append(data)
            if 'number_of_bars' in command_list:
                for data in cur_region_sell_number:
                    filtered_data.append(data)
            if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                for data in cur_region_sell_rating:
                    filtered_data.append(data)
        if 'source' in command_list:
            if 'ratings' in command_list:
                for data in cur_region_source_rating:
                    filtered_data.append(data)
            if 'cocoa' in command_list:
                for data in cur_region_source_cocoa:
                    filtered_data.append(data)
            if 'number_of_bars' in command_list:
                for data in cur_region_source_number:
                    filtered_data.append(data)
            if 'ratings' not in command_list and 'cocoa' not in command_list and 'number_of_bars' not in command_list:
                for data in cur_region_source_rating:
                    filtered_data.append(data)
        
        if 'top' in command_list:
            filtered_data.sort(key=find_1, reverse=True)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]
        if 'bottom' in command_list:
            filtered_data.sort(key=find_1)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]
        if 'top' not in command_list and 'bottom' not in command_list:
            filtered_data.sort(key=find_1, reverse=True)
            if command_list[-1] in number_string_list:
                results = filtered_data[0:int(command_list[-1])]
            if command_list[-1] not in number_string_list:
                results = filtered_data[0:10]


    return results


def barplot(command):
    command_list = command.split()
    if command_list[-1] != 'barplot':
        results = process_command(command)
        organize_table(results)
    if command_list[-1] == 'barplot':
        command_new = command[:-8]
        results_raw = process_command(command_new)
        command_list_new = command_new.split()
        xvals = []
        yvals = []
        if command_list_new[0] == 'bars':
            for data in results_raw:
                xvals.append(data[0])
            if 'ratings' in command_list_new:
                for data in results_raw:
                    yvals.append(data[3])
            if 'cocoa' in command_list_new:
                for data in results_raw:
                    yvals.append(data[4])
            if 'ratings' not in command_list_new and 'cocoa' not in command_list_new:
                for data in results_raw:
                    yvals.append(data[3])
            bar_data = go.Bar(x=xvals, y=yvals)
            basic_layout = go.Layout(title="A Bar Graph")
            fig = go.Figure(data=bar_data, layout=basic_layout)
            fig.show()
        if command_list_new[0] in ['companies','countries', 'regions']:
            for data in results_raw:
                xvals.append(data[0])
                yvals.append(data[-1])
            bar_data = go.Bar(x=xvals, y=yvals)
            basic_layout = go.Layout(title="A Bar Graph")
            fig = go.Figure(data=bar_data, layout=basic_layout)
            fig.show()


def organize_table(results):
    x = PrettyTable()
    for data in results:
        data_list = []
        for each in data:
            if isinstance(each, str):
                if len(each)>12:
                    each_new = each[0:12]+'...'
                else:
                    each_new = each
            elif isinstance(each, float) and each<1:
                each_new = format(each,'.0%')
            elif isinstance(each, float) and each>=1:
                each_new = round(each,1)
            elif isinstance(each, int):
                each_new = each
            data_list.append(each_new)
        x.add_row(data_list)
    print(x)


def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue
        try:
            barplot(response)
        except:
            print('Command not recognized: {}'.format(response))


# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()


    
