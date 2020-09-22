from setuptools import setup

setup(
	name = "mllpa",
	version = "1.0",
	author = "Vivien WALTER",
	author_email = "walter.vivien@gmail.com",
	description = (
	"Machine Learning-assisted Lipid Phase Analysis "
	),
	license = "GPL3.0",
	packages=[
	'mllpa',
	'mllpa.configurations',
	'mllpa.user_interface']
	,
	install_requires=[
	'h5py',
	'MDAnalysis',
	'numpy',
	'pandas',
	'scikit-learn>=0.22.0',
	'tess',
	'tqdm'
	],
	entry_points = {
        'console_scripts': ['mllpa=mllpa.user_interface:main'],
    }
)
