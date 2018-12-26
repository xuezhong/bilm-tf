
import argparse

import numpy as np

from bilm.training import train
from bilm.data import BidirectionalLMDataset, Vocabulary
import os

def main(args):
    # load the vocab
    vocab = Vocabulary(args.vocab_file)

    # define the options
    n_gpus = 1

    # number of tokens in training data (this for 1B Word Benchmark)
    n_train_tokens = 867616283

    options = {
     'bidirectional': True,
     'dropout': args.dropout,
    
     'lstm': {
      'cell_clip': 3,
      'dim': args.lstm_dim,
      'n_layers': args.n_layers,
      'proj_clip': 3,
      'projection_dim': args.projection_dim,
      'use_skip_connections': True},
    
     'all_clip_norm_val': 10.0,
    
     'n_epochs': 10,
     'n_train_tokens': n_train_tokens,
     'batch_size': args.batch_size,
     'n_tokens_vocab': vocab.size,
     'unroll_steps': args.n_steps,
     'para_init':args.para_init,
     'init1':args.init1,
     'debug_rnn':args.debug_rnn,
    }
 
    import random
    random.seed(args.random_seed)
    np.random.seed(args.random_seed)
    import tensorflow as tf
    tf.set_random_seed(args.random_seed)
    import logging
    logger = logging.getLogger("lm")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(str(args))
    logger.info(str(options))

    prefix = args.train_prefix
    data = BidirectionalLMDataset(prefix, vocab, test=True,
                                      shuffle_on_load=False)

    tf_save_dir = args.save_dir
    tf_log_dir = args.save_dir
    train(options, data, n_gpus, tf_save_dir, tf_log_dir, logger, restart_ckpt_file=args.load_dir, args=args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', help='Location of checkpoint files')
    parser.add_argument('--load_dir', help='Location of checkpoint files')
    parser.add_argument('--vocab_file', help='Vocabulary file')
    parser.add_argument('--train_prefix', help='Prefix for train files')
    parser.add_argument('--para_print', action='store_true')
    parser.add_argument('--log_interval', type=int, default=100)
    parser.add_argument('--random_seed', type=int, default=123)
    parser.add_argument('--gpu_num', type=int, default=1)
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--projection_dim', type=int, default=512)
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--lstm_dim', type=int, default=4096)
    parser.add_argument('--n_steps', type=int, default=20)
    parser.add_argument('--dropout', type=float, default=0.0)
    parser.add_argument('--learning_rate', type=float, default=0.2)
    parser.add_argument('--save_para_path', type=str, default='')
    parser.add_argument('--load_para_path', type=str, default='')
    parser.add_argument('--optim', type=str, default='adagrad')
    parser.add_argument('--detail', action='store_true')
    parser.add_argument('--para_init', action='store_true')
    parser.add_argument('--debug_rnn', action='store_true')
    parser.add_argument('--init1', type=float, default=0.1)

    args = parser.parse_args()
    main(args)

