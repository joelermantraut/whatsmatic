#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Clase para facilitar el uso de archivos.

Pensada para obviar criterios predefinidos, y proveer
funciones depuradas que suelen repetirse en muchos
algoritmos de automatizacion.

"""

import glob, os, re
from datetime import datetime

class FileUse(object):
    """Clase dedicada a facilitar el uso de archivos y directorios"""
    def __init__(self):
        super(FileUse, self).__init__()
        self.dirs = []
        self.files = []

    def list_all(self, path):
        """
        Devuelve todo el contenido recursivamente
        """
        for root, dirs, files in os.walk(path):
            for directorio in dirs:
                    self.dirs.append(os.path.abspath(directorio))
            for file in files:
                    self.files.append(os.path.abspath(file))

        return self.dirs, self.files

    def list_dirs(self, filtro=''):
        """
        Devuelve todos los directorios de un directorio raiz.

         - Si se le pasa filtro como una expresion regular, puede
           filtrar los elementos que la cumplan
        """
        regex = re.compile(filtro)

        return list(filter(regex.search, self.dirs))

    def list_files(self, filtro=''):
        """
        Devuelve todos los archivos de un directorio.

         - Si se le pasa filtro como una expresion regular, puede
           filtrar los elementos que la cumplan
        """
        regex = re.compile(filtro)

        return list(filter(regex.search, self.files))

    def get_files_extensions(self):
        """
        Genera un diccionario con cada extension que se puede
        encontrar en la lista de archivos y las veces que aparecen.
        """
        exts = {}

        for file in self.files:
                ext = re.search(r'\.(.+)$', file).group()
                ext = ext[1:len(ext)]
                if ext not in exts:
                        exts[ext] = 1
                else:
                        exts[ext] += 1

        return exts

    def get_file_info(self, file):
        """
        Recibe el nombre completo de un archivo y devuelve:
         - El path.
         - El nombre del archivo en si mismo.
         - La extension.
        En ese orden.
        """
        path = os.path.dirname(file)

        base = os.path.basename(file)
        name, ext = os.path.splitext(base)

        ext = ext[1:]

        return path, name, ext

    def create_file(self, path="", filename="", extension="", ow=False):
        """
        Crea un archivo vacio.

         - Si ya hay un archivo con ese nombre:
          - ow == False: Busca otro nombre iterativamente
          - ow == True: Lo sobreescribe
         - Retorna el objeto FILE
         - Si no se le pasa nombre, lo genera con la fecha de hoy
        """
        if extension == "":
                extension = "txt"

        if filename == "":
                filename = datetime.now().date().__str__() + "." + extension
                filename = filename.replace(" ", "_")

        if path == "":
                path = os.getcwd()

        name = path + '\\' + filename

        if not(ow):
                filename, ext = filename.split('.')[-2], filename.split('.')[-1]
                if ext == "":
                        ext = extension
                name = path + '\\' + filename + '.' + ext
                i = 1
                while os.path.isfile(name):
                        name = path + '\\' + filename + ' (' + str(i) + ').' + ext
                        i += 1

        return open(name, 'w')

def main():
    file_object = FileUse()

    print(file_object.get_file_info("/home/joel/apps/log.txt"))

if __name__ == "__main__":
    main()
