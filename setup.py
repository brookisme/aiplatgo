from distutils.core import setup
setup(
  name = 'aiplatgo',
  packages = ['aiplatgo'],
  version = '0.0.0.1',
  description = 'CLI wrapper for `gcloud ai-platform`',
  author = 'Brookie Guzder-Williams',
  author_email = 'brook.williams@gmail.com',
  url = 'https://github.com/brookisme/aiplatgo',
  download_url = 'https://github.com/brookisme/aiplatgo/tarball/0.1',
  keywords = ['python','tensorflow','gcloud','ai-platform','CLI'],
  include_package_data=True,
  data_files=[
    (
      'config',[]
    )
  ],
  classifiers = [],
  entry_points={
    'console_scripts': [
      'aiplatgo=aiplatgo.cli:cli'
    ]
  }
)