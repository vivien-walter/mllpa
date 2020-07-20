from setuptools import setup

setup(
	name = "mllpa",
	version = "0.1",
	author = "Vivien WALTER",
	author_email = "walter.vivien@gmail.com",
	description = ("Machine learning-assisted lipid memnbrane analysis "),
	license = "BSD",
	packages=['mllpa',
'mllpa.model'],
	install_requires =[
'numpy==1.18.1',
'matplotlib',
'scikit-learn==0.19.1',
'tqdm',
'Pillow',
'imageio',
],
	package_data={'mllpa': ['model/*.sav']},
	include_package_data=True,
	entry_points="""
[console_scripts]
mllpa = mllpa:call_tui
mllpa-readsim = mllpa:call_readsim
mllpa-lpstats = mllpa:call_lpstats
mllpa-getcom = mllpa:call_getcom
mllpa-memview = mllpa:call_memview
"""

)
