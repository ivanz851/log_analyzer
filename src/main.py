import logging
import sys
from datetime import datetime
from argparse import ArgumentParser
from src.log_workers.log_analyser import LogAnalyser
from src.log_workers.log_parser import LogParser
from src.stats_printer.stats_printer import StatsPrinter
from src.table_printers.adoc_table_printer import AdocTablePrinter
from src.table_printers.markdown_table_printer import MarkdownTablePrinter

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

sources = []
from_date = None
to_date = None

table_printer = MarkdownTablePrinter()  
max_lines_in_table = 5


def main(params):
    global table_printer, from_date, to_date, max_lines_in_table

    parse_params(params)
    
    non_parsed_logs = LogParser().combine_logs(sources)
    if not non_parsed_logs:
        LOGGER.info("No logs passed to program")
        return

    logs = LogParser().parse_logs(non_parsed_logs)
    logs = LogAnalyser().get_date_constrained_logs(logs, from_date, to_date)

    stats_printer = StatsPrinter(table_printer)
    
    stats_printer.print_overall_info(logs, sources, from_date, to_date)
    LOGGER.info("")

    stats_printer.print_most_popular_statuses(logs, max_lines_in_table)
    LOGGER.info("")
    stats_printer.print_most_high_loaded_days(logs, max_lines_in_table)
    LOGGER.info("")
    stats_printer.print_most_active_users(logs, max_lines_in_table)
    LOGGER.info("")
    stats_printer.print_most_popular_statuses(logs, max_lines_in_table)


def parse_params(params):
    global sources, from_date, to_date, table_printer, max_lines_in_table
    
    parser = ArgumentParser(description="Log analysis tool")
    parser.add_argument("--sources", nargs='+', help="Paths to log files")
    parser.add_argument("--from", dest="from_date", type=str, help="Start date (ISO8601)")
    parser.add_argument("--to", dest="to_date", type=str, help="End date (ISO8601)")
    parser.add_argument("--format", choices=["markdown", "adoc"], help="Output format (markdown or adoc)")
    parser.add_argument("--lines", type=int, help="Maximum lines in output tables")

    args = parser.parse_args(params)
    
    if args.sources:
        sources = args.sources
    
    if args.from_date:
        from_date = datetime.fromisoformat(args.from_date).date()
    
    if args.to_date:
        to_date = datetime.fromisoformat(args.to_date).date()

    if args.format == "adoc":
        table_printer = AdocTablePrinter()
    else:
        table_printer = MarkdownTablePrinter()
    
    if args.lines:
        max_lines_in_table = args.lines


if __name__ == "__main__":
    """
    Пример запуска: 
    python -m src.main --sources src/nginx_logs.txt --from 2015-05-17 --to 2015-06-10 --format adoc --lines 10
    """
    main(sys.argv[1:])
