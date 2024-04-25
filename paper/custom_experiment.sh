cd ns3_experiments || exit 1

# Custom Experiment
cd custom_experiment || exit 1
python step_1_generate_runs.py || exit 1
python step_2_run.py || exit 1
python step_3_generate_plots.py || exit 1
cd .. || exit 1
