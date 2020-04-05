import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ads-capstone_eurostat",
    version="0.0.1",
    author="Markku Leskinen",
    author_email="mtlesk@gmail.com",
    description="Module to download Eurostat data for large cities in Germany",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mtale/Coursera_Capstone",
    packages=setuptools.find_packages(),
    install_requires=['pyjstat', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)