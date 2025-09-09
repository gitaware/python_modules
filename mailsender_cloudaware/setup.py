import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='mailsender_cloudaware',
  version='0.0.4',
  author='Jeroen Hermans',
  author_email='j.hermans@cloudaware.eu',
  description='Python module to send email',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/gitaware/python_modules/mailsender_cloudaware',
  license='MIT',
  packages=['mailsender_cloudaware'],
  install_requires=[],
)
