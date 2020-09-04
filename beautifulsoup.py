from bs4  import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

req = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html')
soup = BeautifulSoup(req.text, 'html.parser')

"""
old version
for rating in ratings:
    try:
        rating_list.append(float(rating.get_text()))
    except ValueError:
        print(f'conversion "{rating.get_text()}" skipped')
print(len(rating_list))
plt.hist(rating_list)
plt.show()
"""
# Ratings
ratings = soup.find_all('td', class_='Rating')
rating_list = [rating.get_text() for rating in ratings]
rating_list = [float(rating) for rating in rating_list[1:]]

# Companies
companies = soup.find_all('td', class_='Company')
company_list = [company.get_text() for company in companies]
company_list = company_list[1:]

# CocoaPercentage
cocoas = soup.find_all('td', class_='CocoaPercent')
cocoa_list = [float(cocoa.get_text().strip("%")) for cocoa in cocoas[1:]]

df = {
    'Company': company_list,
    'Rating': rating_list,
    'Cocoa Percent (%)': cocoa_list
}
df = pd.DataFrame(df)

groupedCompany = df.groupby('Company')['Rating'].mean()
ten_best = groupedCompany.nlargest(10)
print(ten_best)
print(df.head())

#plt.scatter(df['Rating'], df['Cocoa Percent (%)'])
#plt.show()

z = np.polyfit(df['Cocoa Percent (%)'], df['Rating'], 1)
line_function = np.poly1d(z)
plt.plot(df['Cocoa Percent (%)'], line_function(df['Cocoa Percent (%)']), "r--")
plt.show()