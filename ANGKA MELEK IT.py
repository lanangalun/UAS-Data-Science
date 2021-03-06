# import libraries
from bs4 import BeautifulSoup
#import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import cobaa as func

url = 'https://www.bps.go.id/dynamictable/2018/07/12/1526/proporsi-remaja-dan-dewasa-usia-15-59-tahun-dengan-keterampilan-teknologi-informasi-dan-komputer-tik-menurut-provinsi-2015-2016.html'

# The path to where you have your chrome webdriver stored:
webdriver_path = 'C:\Users\8.1\Downloads\Programs\chromedriver'

# Add arguments telling Selenium to not actually open a window
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')

# Fire up the headless browser
browser = webdriver.Chrome(executable_path=webdriver_path,
                           options=chrome_options)

# Load webpage
browser.get(url)

# It can be a good idea to wait for a few seconds before trying to parse the page
# to ensure that the page has loaded completely.
time.sleep(10)

# Parse HTML, close browser
soup = BeautifulSoup(browser.page_source, 'html.parser')
# print(soup)
pretty = soup.prettify()
browser.quit()
# find results within table
results = soup.find('table',attrs={'id':'tableLeftBottom'})
rows = results.find_all('tr')
list_wilayah = []
melek= []

for r in rows:
    # find all columns per result
    data = r.find_all('td',attrs={'id':'th4'})
    # check that columns have data
    if len(data) == 0:
        continue
    # write columns to variables
    wilayah = data[0].getText()
    list_wilayah.append(wilayah)

results2 = soup.find('table',attrs={'id':'tableRightBottom'})
rows2 = results2.find_all('tr')

for r2 in rows2:
    # find all columns per result
    data2 = r2.find_all('td')
    # check that columns have data
    if len(data2) == 0:
        continue
    # write columns to variables
    angka = data2[1].getText()
    angka=float(angka)
    melek.append(angka)

url = 'https://kawalpemilu.org/#pilpres:0'

# The path to where you have your chrome webdriver stored:
webdriver_path = 'C:\Users\8.1\Downloads\Programs\chromedriver'

# Add arguments telling Selenium to not actually open a window
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')

# Fire up the headless browser
browser = webdriver.Chrome(executable_path=webdriver_path,
                           options=chrome_options)

# Load webpage
browser.get(url)

# It can be a good idea to wait for a few seconds before trying to parse the page
# to ensure that the page has loaded completely.
time.sleep(10)

# Parse HTML, close browser
soup = BeautifulSoup(browser.page_source, 'html.parser')
# print(soup)
pretty = soup.prettify()
browser.quit()
# find results within table
results = soup.find('table',{'class':'table'})
rows = results.find_all('tr',{'class':'row'})
array = []
jokowi = []
prabowo = []

# print(rows)
for r in rows:
    # find all columns per result
    data = r.find_all('td')
    print data
    # check that columns have data
    if len(data) == 0:
        continue
# write columns to variables
    wilayah = data[1].find('a').getText()
    satu = data[2].find('span', attrs={'class':'abs'}).getText()
    dua = data[3].find('span', attrs={'class':'abs'}).getText()
    tiga = data[4].find('span', attrs={'class': 'sah'}).getText()
    # Remove decimal point
    satu = satu.replace('.', '')
    dua = dua.replace('.', '')
    tiga = tiga.replace('.', '')

    # Cast Data Type Integer
    satu = float(satu)
    dua = float(dua)

    array.append(wilayah)
    jokowi.append(satu)
    prabowo.append(dua)

del melek[34]
del prabowo[34]
del jokowi[34]
print prabowo
print jokowi
print melek
np_wilayah = np.array(list_wilayah)
np_jokowi= np.array(jokowi)
np_prabowo= np.array(prabowo)
np_melek = np.array(melek)

print pearsonr(np_melek,np_jokowi)
print pearsonr(np_melek,np_prabowo)

def estimate_coefficients(x, y):
    # size of the dataset OR number of observations/points
    n = np.size(x)

    # mean of x and y
    # Since we are using numpy just calling mean on numpy is sufficient
    mean_x, mean_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x - n * mean_y * mean_x)
    SS_xx = np.sum(x * x - n * mean_x * mean_x)

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = mean_y - b_1 * mean_x

    return (b_0, b_1)

    # x,y are the location of points on graph
    # color of the points change it to red blue orange play around


def plot_regression_line(x, y, b):
    # plotting the points as per dataset on a graph
    plt.scatter(x, y, color="green", marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1] * x
    print np.mean(y_pred)
    # plotting the regression line
    plt.plot(x, y_pred, color="yellow")

    # putting labels for x and y axis
    plt.xlabel('tingkat melek teknologi')
    plt.ylabel('perolehan suara')

    # function to show plotted graph
    plt.show()


def main():
    # Datasets which we create
    x = np_melek
    y = np_prabowo
    #y = np_jokowi
    # estimating coefficients
    b = estimate_coefficients(x, y)
    print("Estimated coefficients:\nb_0 = {} \nb_1 = {}".format(b[0], b[1]))

    # plotting regression line
    plot_regression_line(x, y, b)


if __name__ == "__main__":
    main()
