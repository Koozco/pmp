if __name__ == "__main__":
    args_number = len(argv)
    if (args_number == 1 and stdin.isatty()) or args_number > 2 or (args_number > 1 and argv[1] == "-help"):
        print("This scripts runs a single experiment (generates an elections, "
              "\ncomputes the results according to specified rules, and prepares visualizations)")
        print("\nInvocation:")
        print("  python experiment.py [path_to_output_directory] <description.input")
        exit()

    seed()
    data_in = stdin
    data_out = stdout
    generated_dir_path = "generated"
    if args_number > 1:
        generated_dir_path = argv[1]
        if not os.path.isabs(generated_dir_path):
            generated_dir_path = os.path.join(os.path.pardir, generated_dir_path)

    cmd = read_experiment_data(data_in)

    experiment = Experiment()
    experiment.init_from_input(cmd, generated_dir_path)
    experiment.run(visualization=True, save_win=True)