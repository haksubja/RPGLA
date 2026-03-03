from rpgla.loader import GetLazyData
from rpgla.core import calculate_divines_per_mirror
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import polars as pl


def main():

    args = _parser()

    leagues = [league.strip() for league in args.leagues.split(',')]
    item_types = [item_type.strip() for item_type in args.item_types.split(',')]

    files = [
        f'data/{league}.{item_type}.csv' 
        for league in leagues 
        for item_type in item_types
        ]
    
    print(files)
    lazy_df = GetLazyData(files[0])
    
    print(f'Calculating Divine Orbs per Mirror for {leagues[0]} league...\n')
    result = calculate_divines_per_mirror(lazy_df, leagues[0])

    with pl.Config(tbl_rows=10):
        print(result)


def _parser() -> list[str]:

    parser = ArgumentParser(
        description='Analyze RPG league economic data.',
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--leagues', type=str, 
        default='Settlers',
        help='League names to get data from. String separated by commas (e.g. Settlers, Mercenaries).'
    )
    parser.add_argument(
        '--item_types', type=str,
        default='currency',
        help='Type of items to get data from. String separated by commas (e.g. currency, unique).'
    )
    parser.add_argument(
        '--numeraire', type=str,
        default='Chaos Orb',
        help='Tradable economic entity in terms of whose price the relative prices of all other tradables are expressed.'
    )
    
    return parser.parse_args()


if __name__ == '__main__':
    main()