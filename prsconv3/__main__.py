import cli

args = cli.parser.parse_args()

# Send args to to the engine. It will take things from here.
if args.which_kind:
    cli.engine_dict[args.which_kind].run(args)
