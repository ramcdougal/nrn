"""
do_test.py -- runs a specific test; does not evaluate it

Robert A McDougal
June 23, 2014
"""
def do_test(test_to_run, results_location, num_record=10):
    import os
    # switch to the directory
    initial_path = os.getcwd() + '/'
    the_dir, the_file = os.path.split(test_to_run)
    os.chdir(the_dir)

    from neuron import h, rxd
    import itertools
    

    data = {'record_count': 0, 'data': []}
    do_test.data=data
    record_count = 0

    def collect_data():
        """grabs the membrane potential data, h.t, and the rxd state values"""
        data['record_count'] += 1
        if data['record_count'] > num_record:
            save_and_cleanup()
        
        all_potentials = [seg.v for seg in itertools.chain.from_iterable(h.allsec())]
        all_rxd = list(rxd.node._states)
        local_data = [h.t] + all_potentials + all_rxd

        # remove data before t=0
        if h.t==0:
            data['data']=[]
            data['record_count'] = 1
        # remove previous record if h.t is the same
        if data['record_count']>1 and h.t==data['data'][-len(local_data)]:
            data['record_count'] -= 1
            del data['data'][-len(local_data):]
        # add new data record
        data['data'].extend(local_data)
        # print correct record length
        if data['record_count']==2:
            outstr = "<BAS_RL %i BAS_RL> %s %s" % (len(local_data), repr(h.t), data['record_count'])
            print(outstr)
    
    
    def save_and_cleanup():
        import array
        os.chdir(initial_path)
        # save the data
        with open(results_location, 'wb') as f:
            array.array('d', data['data']).tofile(f)
        
        import sys
        sys.exit(0)

    h.CVode().extra_scatter_gather(0, collect_data)
    
    
    # now run it
    if sys.version_info.major < 3:
        execfile(the_file, globals(), globals())
    else:
        exec(compile(open(the_file).read(), the_file, 'exec'), globals(), globals())

    
    # should only get here if very few steps
    save_and_cleanup()
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('needs two arguments: relative path to python test to run, relative path for results')
        sys.exit()
    do_test(sys.argv[1], sys.argv[2])
