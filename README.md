Run main.py

positional arguments:
  data_file             The name of the JSON file with the data (the .json
                        does not have to be included.)

optional arguments:
  -h, --help            show this help message and exit
  --time_step TIME_STEP, -t TIME_STEP
                        A time step used for numerical integration. Default is
                        20000
  --satelite-data SATELITE_DATA, -s SATELITE_DATA
                        The name of the JSON file with the data for the
                        satelite (the .json does not have to be included.)
  --animation ANIMATION
                        Whether or not to show the animation.
  --energy_graph ENERGY_GRAPH
                        Whether or not to show the energy_graph
  --orbital_periods ORBITAL_PERIODS
                        Whether or not to write the orbutal periods in a file.


Example:
python main.py solar-system-data -t 20000 --energy_graph True -s satelite-data