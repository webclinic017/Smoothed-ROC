import math

def results_func(arr_x=100, arr_y=50, arr_z=100, min_x=1, max_x=1000, min_y=1, max_y=500, min_z=1, max_z=1000, results_density = 20)

    '''
    function to take in parameters relating to the results that will be generated and
    automatically generate the numpy array that will be needed to store those results
    
    tell the function the parameter ranges you are testing and how many results you want in each dimension
    the function calculates how big the array needs to be and how to map each param combination to each array index
    '''

    # size of numpy array to record results
    array_x = arr_x
    array_y = arr_y
    array_z = arr_z

    # range of parameter values for cerebro optimisation to run through
    range_min_x = min_x
    range_max_x = max_x
    range_min_y = min_y
    range_max_y = max_y
    range_min_z = min_z
    range_max_z = max_z

    # how many different values within that range to actually test
    results_amount_x = results_density
    results_amount_y = results_density
    results_amount_z = results_density

    # translate those numbers into step size for python
    step_size_x = math.ceil((range_max_x-range_min_x)/results_amount_x)
    step_size_y = math.ceil((range_max_y-range_min_y)/results_amount_y)
    step_size_z = math.ceil((range_max_z-range_min_z)/results_amount_z)

    # calculate the relationship between param values and position in array
    scale_x = range_max_x/array_x
    scale_y = range_max_y/array_y
    scale_z = range_max_z/array_z

    # example param values
    param_x = 50
    param_y = 50
    param_z = 50

    # calculate array index for given param value
    index_x = param_x/scale_x
    index_y = param_y/scale_y
    index_z = param_z/scale_z

    return index_x, index_y, index_z
    print(f'x steps: {step_size_x}\ny steps: {step_size_y}\nz steps: {step_size_z}')