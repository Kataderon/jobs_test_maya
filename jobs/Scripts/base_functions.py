import maya.mel as mel
import maya.cmds as cmds
import datetime
import time
import json
import re
import os.path as path
import os
import fireRender.rpr_material_browser

WORK_DIR = '{work_dir}'
TEST_TYPE = '{testType}'
RENDER_DEVICE = '{render_device}'
RES_PATH = '{res_path}'
PASS_LIMIT = {pass_limit}
RESOLUTION_X = {resolution_x}
RESOLUTION_Y = {resolution_y}
SPU = {SPU}
LOGS_DIR = path.join(WORK_DIR, 'render_tool_logs')


class RPR_report_json:
    def __init__(self, render_color_path='', render_time='', test_case='', difference_color='', test_status='', script_info=[], render_log=''):
        # TODO: render device may be incorrect (if it changes in case)
        self.render_device = cmds.optionVar(q='RPR_DevicesName')[0]
        self.tool = mel.eval('about -iv')
        self.date_time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        self.render_version = mel.eval('getRPRPluginVersion()')
        self.core_version = mel.eval('getRprCoreVersion()')
        self.render_color_path = path.join('Color', 'MAYA_SM_000.jpg')
        self.render_time = 0
        self.scene_name = get_scene_name()
        self.test_group = TEST_TYPE
        self.test_case = test_case
        self.difference_color = difference_color
        self.test_status = test_status
        self.script_info = script_info
        self.render_log = render_log

    def toJSON(self, path_to_file):
        with open(path_to_file, 'r') as file:
            report = json.loads(file.read())[0]

        report['file_name'] = self.test_case + '.jpg'
        report['date_time'] = self.date_time
        report['script_info'] = self.script_info
        report['render_color_path'] = path.join('Color', report['file_name'])
        report['test_case'] = self.test_case
        report['render_version'] = self.render_version
        report['test_status'] = self.test_status
        report['tool'] = self.tool
        report['render_time'] = self.render_time
        report['scene_name'] = self.scene_name
        report['test_group'] = self.test_group
        report['difference_color'] = self.difference_color
        report['core_version'] = self.core_version
        report['render_device'] = self.render_device
        report['render_log'] = path.join(
            'render_tool_logs', self.test_case + '.log')

        with open(path_to_file, 'w') as file:
            file.write(json.dumps([report], indent=4))


def render_tool_log_path(name):
    return path.join(LOGS_DIR, name + '.log')


def get_scene_name():
    scene_name = cmds.file(q=True, sn=True, shn=True)
    if not scene_name:
        print('Problem with scene')
    return scene_name


def validateFiles():
    unresolved_files = cmds.filePathEditor(
        query=True, listFiles='', unresolved=True, attributeOnly=True)
    new_path = RES_PATH
    if unresolved_files:
        for item in unresolved_files:
            cmds.filePathEditor(item, repath=new_path, recursive=True, ra=1)


def check_rpr_load():
    if not cmds.pluginInfo('RadeonProRender', query=True, loaded=True):
        cmds.loadPlugin('RadeonProRender', quiet=True)
    if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
        cmds.loadPlugin('fbxmaya', quiet=True)


def rpr_render(test_case, script_info):
    render_device = RENDER_DEVICE
    cmds.setAttr('RadeonProRenderGlobals.samplesPerUpdate', SPU)
    cmds.optionVar(rm='RPR_DevicesSelected')

    cmds.optionVar(iva=('RPR_DevicesSelected',
                        (render_device in ['gpu', 'dual'])))
    cmds.optionVar(iva=('RPR_DevicesSelected',
                        (render_device in ['cpu', 'dual'])))

    cmds.setAttr('RadeonProRenderGlobals.adaptiveThreshold', 0)
    cmds.setAttr('RadeonProRenderGlobals.completionCriteriaSeconds', 0)

    mel.eval('fireRender -waitForItTwo')
    start_time = time.time()
    mel.eval('renderIntoNewWindow render')
    cmds.sysFile(path.join(WORK_DIR, 'Color'), makeDir=True)
    test_case_path = path.join(WORK_DIR, 'Color', test_case)
    cmds.renderWindowEditor('renderView', edit=1,  dst='color')
    cmds.renderWindowEditor('renderView', edit=1, com=1,
                            writeImage=test_case_path)
    test_time = time.time() - start_time

    report_JSON = path.join(WORK_DIR, test_case + '_RPR.json')

    report = RPR_report_json()
    report.render_time = test_time
    report.test_case = test_case
    report.test_status = 'passed'
    report.script_info = script_info
    if not report.scene_name:
        report.scene_name = case.get('scene', '')

    report.toJSON(report_JSON)


def prerender(case):
    test_case = case['case']
    script_info = case['script_info']
    scene = case.get('scene', '')
    scene_name = cmds.file(q=True, sn=True, shn=True)
    if scene_name != scene:
        try:
            cmds.file(scene, f=True, op='v=0;', prompt=False, iv=True, o=True)
        except:
            cmds.evalDeferred('cmds.quit(abort=True)')

    validateFiles()

    check_rpr_load()

    if RESOLUTION_X and RESOLUTION_Y:
        cmds.setAttr('defaultResolution.width', RESOLUTION_X)
        cmds.setAttr('defaultResolution.height', RESOLUTION_Y)

    cmds.setAttr('defaultRenderGlobals.currentRenderer',
                 type='string' 'FireRender')
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    cmds.setAttr(
        'RadeonProRenderGlobals.completionCriteriaIterations', PASS_LIMIT)

    with open(path.join(WORK_DIR, 'test_cases.json'), 'r') as json_file:
        cases = json.load(json_file)

    for case in cases:
        if case['case'] == test_case:
            try:
                for function in case['functions']:
                    try:
                        if re.match('(^\w+ = |^print)', function):
                            exec(function)
                        else:
                            eval(function)
                    except Exception as e:
                        print('Error {{}} with string {{}}'.format(
                            e, function))
            except Exception as e:
                rpr_render(test_case, script_info)


def rpr_save(case):
    test_case = case['case']
    cmds.sysFile(path.join(WORK_DIR, 'Color'), makeDir=True)
    work_folder = path.join(WORK_DIR, 'Color', test_case + '.jpg')

    if case['status'] == 'inprogress':
        cmds.sysFile(path.join(WORK_DIR, '..', '..', '..', '..',
                               'jobs', 'Tests', 'pass.jpg'), copy=work_folder)
    elif case['status'] == 'error':
        cmds.sysFile(path.join(WORK_DIR, '..', '..', '..', '..',
                               'jobs', 'Tests', 'failed.jpg'), copy=work_folder)
    elif case['status'] == 'skipped':
        cmds.sysFile(path.join(WORK_DIR, '..', '..', '..', '..',
                               'jobs', 'Tests', 'skipped.jpg'), copy=work_folder)

    check_rpr_load()
    report_JSON = path.join(WORK_DIR, (test_case + '_RPR.json'))

    report = RPR_report_json()
    report.test_case = test_case
    report.script_info = case['script_info']
    if not report.scene_name:
        report.scene_name = case.get('scene', '')

    if case['status'] == 'inprogress':
        report.test_status = 'passed'
    else:
        report.test_status = case['status']

    report.toJSON(report_JSON)


def case_function(case):
    functions = {{
        0: prerender,
        1: rpr_save
    }}

    func = 0

    if case['functions'][0] == 'check_test_cases_success_save':
        func = 1

    if case['status'] == 'fail':
        case['status'] = 'error'
        func = 1

    functions[func](case)


def main():

    mel.eval('setProject(\"{{}}\")'.format(RES_PATH))

    cmds.sysFile(LOGS_DIR, makeDir=True)

    with open(path.join(WORK_DIR, 'test_cases.json'), 'r') as json_file:
        cases = json.load(json_file)

    #   Possible case statuses:
    # - Active: Case will be executed.
    # - Inprogress: Case is in progress (if maya was crashed, case will be inprogress).
    # - Fail: Maya was crashed during case. Fail report will be created.
    # - Error: Maya was crashed during case. Fail report is already created.
    # - Done: Case was finished successfully.
    # - Skipped: Case will be skipped. Skip report will be created.

    for case in cases:
        if case['status'] == 'active':
            case['status'] = 'inprogress'
        if case['status'] == 'inprogress' or case['status'] == 'fail':
            with open(path.join(WORK_DIR, 'test_cases.json'), 'w') as file:
                json.dump(cases, file, indent=4)

            if not path.exists(render_tool_log_path(case['case'])):
                with open(render_tool_log_path(case['case']), 'w'):
                    pass

            cmds.scriptEditorInfo(historyFilename=render_tool_log_path(
                case['case']), writeHistory=True)
            print(case['case'])
            case_function(case)

            if case['status'] == 'inprogress':
                case['status'] = 'done'

            with open(path.join(WORK_DIR, 'test_cases.json'), 'w') as file:
                json.dump(cases, file, indent=4)
        if case['status'] == 'skipped':
            rpr_save(case)

    cmds.evalDeferred('cmds.quit(abort=True)')


