import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ads-capstone",
    version="0.1.0",
    author="Markku Leskinen",
    author_email="mtlesk@gmail.com",
    description="Package to run most of the code behind the scenes instead of notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mtale/Coursera_Capstone",
    packages=setuptools.find_packages(),
    install_requires=['numpy','overpy','pandas','pyjstat','requests','tqdm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)