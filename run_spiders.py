import argparse
import logging

from haipproxy.scheduler import crawler_start

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="run spiders")
    parser.add_argument('tasks', type=str, nargs='*', help='task1 task2 ...')
    parser.add_argument("-o",
                        "--one",
                        help="one time run",
                        action="store_true")
    parser.add_argument("-s",
                        "--schedule",
                        help="schedule run",
                        action="store_true")
    args = parser.parse_args()
    logging.info(args)
    if args.one:
        crawler_start(args.tasks)
    elif args.schedule:
        scheduler_start(args.tasks)
    else:
        parser.print_help()
