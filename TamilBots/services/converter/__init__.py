from os import listdir, mkdir

if "raw_files" not in listdir():
    mkdir("raw_files")

from Cyber.services.converter.converter import convert

__all__ = ["convert"]
