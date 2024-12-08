import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='hetzner_dnsapi',
  version='0.0.1',
  author='Jeroen Hermans',
  author_email='j.hermans@cloudaware.eu',
  description='Python module to communicate with Hetzner DNS API',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/gitaware/python_modules/hetzner_dnsapi',
  license='MIT',
  packages=['hetzner_dnsapi'],
  install_requires=[],
)
