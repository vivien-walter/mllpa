from setuptools import setup

setup(
	name = "mllpa",
	version = "1.0",
	author = "Vivien WALTER",
	author_email = "walter.vivien@gmail.com",
	description = (
	"Machine Learning-assisted Lipid Phase Analysis - Module to analyse a lipid membrane generated using Molecular Dynamics (MD) simulations and predict the thermodynamical phase of the lipids."
	),
	license = "GPL3.0",
	download_url = 'https://github.com/vivien-walter/mllpa/archive/v_1.tar.gz',
	packages=[
	'mllpa',
	'mllpa.configurations']
	,
	install_requires=[
	'cython',
	'h5py',
	'MDAnalysis',
	'numpy',
	'pandas',
	'scikit-learn>=0.22.0',
	'tess',
	'tqdm'
	]
)
