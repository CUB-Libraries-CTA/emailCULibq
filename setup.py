from setuptools import setup, find_packages

setup(name='emailCULibq',
      version='0.0',
      packages= find_packages(),
      package_data={"emailCULibq": ["*.j2"]},
      include_package_data=True,
      install_requires=[
          'Jinja2',
      ],
)