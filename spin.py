import argparse
import sys

from twilio.rest import Client
import requests
import datetime
import logging
import schedule
import time
from bs4 import BeautifulSoup

LOCATION = '15391'
GUID = '98fb95e3-c53e-ea11-aa59-d942907bbf75'
API_URL = 'https://www.fitmetrix.io/WebPortal/ajaxScheduleCalendar/'

parser = argparse.ArgumentParser(
    prog="spin-checker",
    description="""Spin Checker verifies whether the next week schedule for \
                   the Stride Spin Studio is available."""
)
parser.add_argument(
    "-l",
    "--loop",
    dest="loop",
    action="store_true",
    help="Run the check in a loop until the schedule is posted."
)
parser.add_argument(
    "-i",
    "--interval",
    default=30,
    dest="loop_interval",
    type=int,
    help="How often to check in seconds (requires loop mode)"
)
parser.add_argument(
    "-s",
    "--sid",
    dest="twilio_sid",
    help="Account SID for Twilio integration"
)
parser.add_argument(
    "-t",
    "--token",
    dest="twilio_token",
    help="Auth token for Twilio integration"
)
parser.add_argument(
    "-f",
    "--from",
    dest="send_from",
    help="Number to use as source for Twilio notifications"
)
parser.add_argument(
    "-n",
    "-- numbers",
    nargs=argparse.REMAINDER,
    dest="send_to",
    help="List of phone numbers to send notifications to."
)

args = parser.parse_args()


def get_daterange():
    today = datetime.date.today()

    # Days till next Sunday
    add_days = 6 - today.weekday()

    start_date = today + datetime.timedelta(add_days)
    end_date = start_date + datetime.timedelta(6)

    return start_date, end_date


def send_text(account_sid, auth_token, send_from, send_to):
    client = Client(account_sid, auth_token)

    for number in send_to:
        client.messages.create(
            body='SPIN CLASSES ARE POSTED!',
            from_=send_from,
            to=number
        )


def run_checker():
    logging.info("Checking lessons schedule")
    start_date, end_date = get_daterange()

    request_url = f"{API_URL}{LOCATION}?datestart={start_date.strftime('%m/%d/%y')}&dateend={end_date.strftime('%m/%d/%y')}&facguid={GUID}&instructorID=&classes=&classtypes=&locationID={LOCATION}"
    r = requests.get(request_url)

    if r.status_code != 200:
        logging.error(f"Could not fetch page. Status code: {r.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")

    days_names_el = soup.select(".wmrh-date")
    days_el = soup.select(".wppc-most-recent-val")
    lessons_el = [day_el.select(".cal-item-link.ct-2") for day_el in days_el]

    if any([True for lesson in lessons_el[1:] if len(lesson) > 0]):
        logging.warning("Lessons are posted!")
        if args.twilio_sid and args.twilio_token and args.send_from and args.send_to:
            logging.info("Twilio integration will now send texts out")
            send_text(args.twilio_sid, args.twilio_token, args.send_from, args.send_to)

        # Break out of the schedule
        sys.exit(0)
    else:
        logging.info("Lessons aren't posted yet.")

        return False


def main():
    logging.basicConfig(level=logging.INFO)

    if args.loop:
        schedule.every(args.loop_interval).seconds.do(run_checker).tag("checker")

        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        result = run_checker()
        sys.exit(int(result))


if __name__ == "__main__":
    main()
