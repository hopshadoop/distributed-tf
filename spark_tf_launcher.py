def launch(spark_session, map_fun, args_dict):
    """ Run the wrapper function with each hyperparameter combination as specified by the dictionary

    Args:
      :spark_session: SparkSession object
      :map_fun: The TensorFlow function to run
      :args_dict: A dictionary containing hyperparameter values to insert as arguments for each TensorFlow job
    """

    sc = spark_session.sparkContext

    # Length of the list of the first list of arguments represents the number of Spark tasks
    num_tasks = len(args_dict.values()[0])

    # Create a number of partitions (tasks)
    nodeRDD = sc.parallelize(range(num_tasks), num_tasks)

    # Execute each of the hyperparameter arguments as a task
    nodeRDD.foreachPartition(_do_search(map_fun, args_dict))


def _do_search(map_fun, args_dict):
    
    def _wrapper_fun(iter):

        for i in iter:
            executor_num = i

        argcount = map_fun.func_code.co_argcount
        names = map_fun.func_code.co_varnames

        args = []
        argIndex = 0
        while argcount > 0:
            # Get arguments for hyperparameter combination
            param_name = names[argIndex]
            param_val = args_dict[param_name][executor_num]
            args.append(param_val)
            argcount -= 1
            argIndex += 1
        map_fun(*args)
    return _wrapper_fun
        

