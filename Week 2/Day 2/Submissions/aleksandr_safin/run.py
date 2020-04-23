import argparse
from main import main

def set_args(parser):
    parser.add_argument('--C', default=1., type=float,
                        help="regularizer coefficient")
    parser.add_argument('--test_size', type=float,
                        default=0.33, help='test size for data train/test split')
    parser.add_argument('--random_state', type=int,
                        default=42, help='random state seed')
    return parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    set_args(parser)
    args = parser.parse_args()
    
    main(args)
