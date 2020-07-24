from distutils.core import setup
setup(
  name = 'your_project_module',
  packages=[
    'your_project_module',
    'your_project_module.nn',
    'trainer'
  ],
  package_dir = {
    'your_project_module': 'your_project_module',
    'your_project_module.nn': 'your_project_module/nn',
    'trainer': 'trainer' 
  },
  version = '0.0.0.1',
  description = 'todo: your_project_module description',
  author = 'First Last',
  author_email = 'you@email.com',
  url = 'https://github.com/you/your_project_module',
  download_url = 'https://github.com/you/your_project_module/tarball/0.1',
  keywords = ['python','tensorflow','model','keras'],
  include_package_data=False,
  package_data={
    'your_project_module.nn': ['configs/*.yaml'],
    'trainer': ['*.yaml','../*.yaml']
  },
  classifiers = [],
  install_requires=[
    'click>=7.1.1',
    'rasterio>=1.1.5',
    'matplotlib>=3.2.1',
    'geojson>=2.5.0',
    'tensorflow-addons',
    'retrying>=1.3.3',
    'pyproj>=2.6.1',
    'affine>=2.3',
    'tfbox>=0.0.0.6',
  ],
  entry_points={
      'console_scripts': [
      ]
  }
)