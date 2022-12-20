import warnings
warnings.filterwarnings("ignore")
import final_scrapping
city_from = 'MSY'
city_to = 'DEL'
date_start = '2023-01-04'
date_end = '2023-01-06'
final_scrapping.start_kayak(city_from, city_to, date_start, date_end)