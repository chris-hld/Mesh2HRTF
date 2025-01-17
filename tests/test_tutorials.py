import pytest
import os
import shutil
import subprocess
import tempfile
import utils
import matplotlib.pyplot as plt
import mesh2hrtf as m2h

# define and check paths to your Blender versions (only use one blender)
blender_path, addon_path, script_path = utils.blender_paths(2)[0]

# set test parameters
tutorials = ['rigid_sphere_scattering.py',
             'radiation_from_a_vibrating_element.py',
             'non_rigid_boundary_conditions.py',
             'hrtf.py']
run_numcalc = True

base_dir = os.path.dirname(__file__)
install_script = os.path.join(base_dir, 'resources', 'install_addons.py')

# addons to be installed
addons = [
    (os.path.join(base_dir, '..', 'mesh2hrtf', 'Mesh2Input', 'mesh2input.py'),
     'mesh2input')]
scripts = [os.path.join(base_dir, '..', 'mesh2hrtf', 'Mesh2Input', 'Meshes',
                        'AssignMaterials', 'AssignMaterials.py')]

# generate script for installing addons
utils.install_blender_addons_and_scripts(
    blender_path, addon_path, addons, script_path, scripts, install_script)

# Build NumCalc locally to use for testing
tmp = tempfile.TemporaryDirectory()
numcalc = os.path.join(tmp.name, "NumCalc", "bin", "NumCalc")

shutil.copytree(
    os.path.join(base_dir, "..", "mesh2hrtf", "NumCalc"),
    os.path.join(tmp.name, "NumCalc"))

if os.path.isfile(numcalc):
    os.remove(numcalc)

subprocess.run(
    ["make"], cwd=os.path.join(tmp.name, "NumCalc", "src"), check=True)


@pytest.mark.parametrize('tutorial', tutorials)
def test_tutorials(tutorial):

    # directory for testing the tutorial
    tmp = tempfile.TemporaryDirectory()
    print(f"preparing {tutorial} in {tmp.name}")

    # read tutorial file
    tutorial_file = os.path.join(
        base_dir, '..', 'mesh2hrtf', 'Mesh2Input', 'Tutorials', tutorial)
    with open(tutorial_file, 'r') as file:
        script = ''.join(file.readlines())

    # change paths
    script = script.replace(
        "path/to/your/project_folder",
        os.path.join(tmp.name, tutorial[:-3]))
    script = script.replace(
        "path/to/your/Mesh2HRTF/mesh2hrtf",
        os.path.join(base_dir, '..', 'mesh2hrtf'))

    # save tutorial to temp dir
    with open(os.path.join(tmp.name, tutorial), 'w') as file:
        file.write(script)

    # export the project folder
    print("exporting")
    subprocess.run(
        [os.path.join(blender_path, 'blender'), '--background',
         '--python', install_script,
         '--python', os.path.join(tmp.name, tutorial)],
        cwd=tmp.name, check=True, capture_output=True)

    if run_numcalc:
        # run manage_numcalc and process output
        print("running NumCalc")
        m2h.manage_numcalc(os.path.join(tmp.name, tutorial[:-3]), numcalc)

        print("running output2hrtf")
        m2h.output2hrtf(os.path.join(tmp.name, tutorial[:-3]))
        plt.close("all")
