import os

output_file = './bugscpp/make_dataset/benchmark/libchewing-8/libchewing-buggy-8-1/1.output'
# print(dir_list)
wf = open('./data/bugscpp/libchewing_8/failing_tests', 'w')
with open(output_file) as f:
    for l in f:
        if l.startswith("    Start "):
            test_file = l.split(':')[-1].strip() 
        wf.write(l)
wf.write('End\n')
wf.write('\nLogfile starts\n')

log_file = './bugscpp/make_dataset/benchmark/libchewing/buggy-8/build/test/' + test_file + ".log"
with open(log_file, encoding = 'utf-8', errors='ignore') as lf:
    for l in lf:
        wf.write(l)
wf.close()