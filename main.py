import argparse
from solarSystem import Solar

# Getting the arguments
parser = argparse.ArgumentParser(description='Get the details for the road')

parser.add_argument('data_file', type=str,
                    help=("""The name of the JSON file with the data
                    (the .json does not have to be included.)"""))

parser.add_argument('--time_step', '-t', type=int, default=20000,
                    help=("""A time step used for numerical integration.
                    Default is 20000"""))

parser.add_argument('--satelite-data', '-s', default=False,
                    help=("""The name of the JSON file with the data for the satelite
                    (the .json does not have to be included.)"""))

parser.add_argument('--animation', type=bool, default=True,
                    help="""Whether or not to show the animation.""")

parser.add_argument('--energy_graph', type=bool, default=False,
                    help="""Whether or not to show the energy_graph""")

parser.add_argument('--orbital_periods', type=bool, default=True,
                    help="""Whether or not to write the orbutal periods in a file.""")

args = parser.parse_args()

if __name__ == "__main__":

    solar_system = Solar(args.data_file, args.time_step, satelite=args.satelite_data)
    solar_system.run(animation=args.animation, energy_graph=args.energy_graph,
                     orbital_periods=args.orbital_periods)
