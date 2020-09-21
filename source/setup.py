from setuptools import setup

setup(
	name = "mllpa",
	version = "1.0",
	author = "Vivien WALTER",
	author_email = "walter.vivien@gmail.com",
	description = (
	"Machine learning-assisted lipid membrane analysis "
	),
	license = "GPL3.0",
	packages=[
	'mllpa',
	'mllpa.configurations']
	,
	install_requires=[
	'h5py',
	'MDAnalysis',
	'numpy',
	'pandas',
	'scikit-learn>=0.22.0',
	'tess',
	'tqdm'
	]
)
