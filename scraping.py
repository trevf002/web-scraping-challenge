from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
  executable_path = {'executable_path': ChromeDriverManager().install()}
  browser = Browser('chrome', **executable_path, headless=False)
  url = 'https://mars.nasa.gov/news/'
  browser.visit(url)
  html=browser.html
  soup=bs(html,'html.parser')
  # Retrieve the latest news title
  news_title=soup.find_all('div', class_='content_title')[0].text
  # Retrieve the latest news paragraph
  news_p=soup.find_all('div', class_='rollover_description_inner')[0].text
  data={
    "news_title":news_title,
    "news_p":news_p,
    "feature_image":feature_image(browser),
    "mars_table":mars_table(),
    "mars_hemi":mars_hemi(browser)
  }
  browser.quit()
  return data

def feature_image(browser):
  url = 'https://spaceimages-mars.com'
  browser.visit(url)
  browser.find_by_css("a.showimg button").click()
  html=browser.html
  soup=bs(html, 'html.parser')
  image_url=soup.find('img', class_='fancybox-image').get('src')
  full_image_url=url+'/'+image_url
  return full_image_url

def mars_table():
  url='https://galaxyfacts-mars.com/'
  mars_df=pd.read_html(url)[1]
  mars_df.columns=['Property', 'Values']
  mars_df.set_index('Property', inplace=True)
  return mars_df.to_html()

def mars_hemi(browser):
  url='https://marshemispheres.com/'
  browser.visit(url)
  hemi_store = []
  all_thumbnails = browser.find_by_css("a.product-item img")

  for current_thumbnail in range(len(all_thumbnails)):
      temp = {}
      
      browser.find_by_css("a.product-item img")[current_thumbnail].click()
      temp["title"] = browser.find_by_css("h2.title").text
      temp["img_url"] = browser.find_by_text("Sample").first["href"]
      hemi_store.append(temp)
      browser.visit(url)

  return hemi_store

if __name__=="__main__":
  print(scrape_all())
