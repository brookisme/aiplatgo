from distutils.core import setup
setup(
  name = 'aiplatgo',
  packages = ['aiplatgo'],
  package_dir = {
    'aiplatgo': 'aiplatgo'
  },
  version = '0.0.0.13',
  description = 'CLI wrapper for `gcloud ai-platform`',
  author = 'Brookie Guzder-Williams',
  author_email = 'brook.williams@gmail.com',
  url = 'https://github.com/brookisme/aiplatgo',
  download_url = 'https://github.com/brookisme/aiplatgo/tarball/0.1',
  keywords = ['python','tensorflow','gcloud','ai-platform','CLI'],
  include_package_data=False,
  package_data={
    'aiplatgo': ['config/*.yaml']
  },
  data_files=[
    (
      'config',[]
    )
  ],
  install_requires=[
    'click',
    'pandas',
    'pyyaml',
    'mproc',
    'gcs_helpers>=0.0.0.22'
  ],
  classifiers = [],
  entry_points={
    'console_scripts': [
      'aiplatgo=aiplatgo.cli:cli'
    ]
  }
)