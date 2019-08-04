import requests, time, random, os, logging
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.spiegel.de/schlagzeilen/'
sub_dir = 'spiegel_artikel'
sub_dir_logs = 'logs'
log_file_name = 'spiegel_artikel_log'
timeout_duration = 5
num_latest_downloads = 1000
sleep_min = 20
sleep_max = 120
div_headline_identifier = {"class":"schlagzeilen-content schlagzeilen-overview"}

sleeptimes = list(range(sleep_min,sleep_max,1))

abs_path = os.path.join(os.getcwd(),sub_dir)
abs_path_logs = os.path.join(abs_path,sub_dir_logs)
if not os.path.exists(abs_path_logs):
    os.makedirs(abs_path_logs)

latest_downloads = os.listdir(abs_path)
total_downloaded = len(latest_downloads)-1
total_timeouts = 0
total_other = 0
total_unknown_errors = 0
last_batch = 0
while True:
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(abs_path_logs,f'{log_file_name}_{date_str}.log')
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode="a+",
        format="%(asctime)-15s %(message)s"
    )
    sleeptime = random.choice(sleeptimes)
    print(f'Sleeping: {sleeptime} \tLast bach-size: {last_batch}')
    logging.info(f'Sleeping: {sleeptime} \tLast bach-size: {last_batch}')
    time.sleep(sleeptime)
    last_batch = 0
    try:
        response = requests.get(url).content
        soup = BeautifulSoup(response,'html.parser')
        headlines = soup.find('div',attrs=div_headline_identifier)
        for a in headlines.find_all('a'):
            link = a['href']
            if not link.startswith('http') and not link in latest_downloads:
                file_path = os.path.join(abs_path,link.replace('/','.')[1:])
                full_link = urljoin(url, link)
                title = a['title']
                try:
                    article_content = requests.get(full_link, timeout=timeout_duration).content
                    with open(file_path,'wb') as f:
                        f.write(article_content)
                    total_downloaded += 1
                    last_batch += 1
                    print(f'Downloaded ({total_downloaded}): {title}')
                    logging.info(f'Downloaded ({total_downloaded}): {title}')
                    latest_downloads.append(link)
                except requests.exceptions.Timeout:
                    total_timeouts += 1
                    print(f'Timeout ({total_timeouts}): {title}')
                    logging.info(f'Timeout ({total_timeouts}): {title}')
                except:
                    total_other += 1
                    print(f'Other Exception ({total_other}): {title}')
                    logging.info(f'Other Exception ({total_other}): {title}')
        list_pointer = min(len(latest_downloads),num_latest_downloads)
        latest_downloads = latest_downloads[-list_pointer:]
    except:
        total_unknown_errors += 1
        print(f'Unknown Error ({total_unknown_errors})')
        logging.info(f'Unknown Error ({total_unknown_errors})')
