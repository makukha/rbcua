from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
import sys

from loguru import logger
import lxml.html
import pandas as pd
import requests


URL = 'https://www.rbc.ua/ukr/currency/mb'


@dataclass
class Record:
    timestamp: datetime
    usd_bid: float
    usd_ask: float
    eur_bid: float
    eur_ask: float


def main(datafile: Path):

    logger.info('Scraper started')

    # get last timestamp if any
    last_timestamp = get_last_timestamp(datafile)
    if last_timestamp is None:
        logger.info('No previous data found')
    else:
        logger.info('Last observed timestamp is {}', last_timestamp)

    # get data
    resp = requests.get(URL)
    if not resp.ok:
        logger.critical('Resource unavailable, HTTP status code: {}', resp.status_code)
        sys.exit(1)
    try:
        data = parse(resp.text)
    except:
        logger.critical('Error parsing response')
        sys.exit(1)
    logger.debug('Scraped timestamp is {}', data.timestamp)

    # append if updated
    datafile.parent.mkdir(exist_ok=True, parents=True)  # create parent dir
    if last_timestamp is None or data.timestamp > last_timestamp:
        append(data, datafile)
        logger.success('Added data for timestamp {}', data.timestamp)
    else:
        logger.info('No new data found')


def get_last_timestamp(datafile: Path) -> datetime | None:
    if not datafile.exists():
        return None
    df = pd.read_csv(datafile, usecols=['timestamp'], parse_dates=[0])
    return None if len(df) == 0 else df['timestamp'].max()


def parse(content: str) -> Record:
    doc = lxml.html.fromstring(content).xpath('.//div[@class="currency-page"]')[0]
    dtm = doc.xpath('.//div[@class="news-page-heading"]/text()')[0].removeprefix('Курс межбанка на ')
    rows = doc.xpath('.//table//tr')[1:]
    cells = [r.xpath('./td/text()')[1:] for r in rows]
    return Record(
        timestamp=datetime.strptime(dtm, '%d.%m.%Y (%H:%M)'),
        usd_bid=float(cells[0][0]),
        eur_bid=float(cells[0][1]),
        usd_ask=float(cells[1][0]),
        eur_ask=float(cells[1][1]),
    )


def append(data: Record, datafile: Path) -> None:
    header = None if datafile.exists() else ','.join(asdict(data).keys())
    values = ','.join(str(v) for v in asdict(data).values())
    with datafile.open('at') as f:
        if header:
            f.write(header + '\n')
        f.write(values + '\n')


if __name__ == '__main__':
    datafile = Path(sys.argv[1])
    main(datafile)
