from robot import run


def robot_exec(test_case_file, argument_file, output_directory):
    run(test_case_file, variablefile=argument_file, outputdir=output_directory, console='None')


if __name__ == '__main__':
    robot_exec(
        '/home/diogenoz/PycharmProjects/WebDemo/robotmanager/media/test_cases/case2/runs/30/sources/test_case.robot',
        '/home/diogenoz/PycharmProjects/WebDemo/robotmanager/media/test_cases/case2/runs/30/sources/argument_set.yaml',
        '/home/diogenoz/PycharmProjects/WebDemo/gui_test1/out3')
