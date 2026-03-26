from setuptools import setup, find_packages

setup(
    name="clock-x-overlay",
    version="1.0.0",
    description="OSD clock overlay for Linux X11 desktops",
    author="dewiweb",
    url="https://github.com/dewiweb/clock_X_overlay",
    packages=find_packages(),
    install_requires=["PyQt6>=6.4.0"],
    entry_points={
        "console_scripts": [
            "clock-x-overlay=clock_x_overlay.main:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
)
