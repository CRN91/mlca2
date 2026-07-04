import os

def save_history():
    dir_name = os.getcwd()
    path = os.path.join(dir_name,'proof_of_work')
    if not os.path.exists(path):
        os.makedirs(path)

    from datetime import datetime  
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fname = 'CA_history_%s.txt'%timestamp
    fname = os.path.join(path,fname)

    import IPython
    profile_hist=IPython.core.history.HistoryAccessor(profile='default')
    session_id = profile_hist.get_last_session_id()

    with open(fname, "w", encoding="utf-8", errors="replace") as file:
        for line in profile_hist.get_tail(n=1000, raw=False, output=False, include_latest=False):
            if session_id ==  line[0]:
                source = line[2]
                if source is None:
                    continue
                source = str(source).replace('\n','\t')
                out = '%s %s %s %s'%(timestamp, line[0],line[1], source)
                file.write('%s\n'%out)
                
                
def check_and_prepare_for_submission():
    try:
        path = 'proof_of_work'
        dir_with_history_exists = os.path.exists(path)
        assert dir_with_history_exists, 'ERROR: The directory <%s> is missing!'%path
        file_count = sum(len(files) for _, _, files in os.walk(path))
        there_are_some_files = file_count > 0
        assert there_are_some_files, 'ERROR: The directory <%s> is empty!'%path
    except:
        print('The submission is NOT valid!')
    else:
        import shutil
        dir_name = os.getcwd()
        os.chdir(os.path.pardir)
        output_filename = 'ecmm422_ca2_ref_def'
        shutil.make_archive(output_filename, 'zip', dir_name)
        os.chdir(dir_name)
        print('The notebook and the history are ready for sumbission.\nThe following archive has been created in the parent directory with name: %s.zip'%output_filename)


def should_run_checkpoint() -> bool:
    """Return True when checkpoint cells should execute.

    The helper reads the environment variable ``ECMM422_DONT_RUN_CHECKPOINTS``.
    When the variable is unset or evaluates to one of {''0'', ''false'', ''no''} (case-insensitive),
    checkpoints will run. Any other non-empty value disables them.
    """
    flag = os.environ.get('ECMM422_DONT_RUN_CHECKPOINTS', '').strip().lower()
    return flag in {'', '0', 'false', 'no'}
