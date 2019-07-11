import os
import time
from collections import namedtuple
class DirectoryPal():

    def __init__(self, directory=None):
        """Pass a path to a directory(folder) that needs cleaning or the current one is default """
        if directory == None:
            self.directory = os.getcwd()
        else:
            self.directory = directory
        self.files = list(os.listdir(self.directory))

    def file_deco(func):
        #print('hello')
        def print_dict(x):
            dict_func = func(x)
            print('File Type:  File Quantity: ')
            for key, value in dict_func.items():
                print("{}\t\t{}".format(key,value))
                if key=='':
                    print("{}\t\t{}".format('None',value))
            return dict_func
        return print_dict

    @file_deco
    def file_types(self,):
        """returns a dictionary of file type and counts"""
        """broken"""
        type_count = {}
        for file in self.files:
            file_type = file[file.find('.')::][1::]
            if file_type not in type_count:
                type_count[file_type] = 1
            else:
                type_count[file_type]+=1
        return type_count

    def update_dir(self, path):
        self.directory = path
        self.files = (os.listdir(path))
        print('path successfully updated')

    def correct_directory(func):
        """decorator makes assigns os.chdir() equal to directory of current object"""
        def changing_dir(self, *args,**kwargs):
            os.chdir(self.directory)
            return func(self,*args,**kwargs)
        return changing_dir

    @correct_directory
    def space_to_underscore(self,):
        """replaces all spaces in file names to underscores"""
        #[rename(i,i.replace(' ','_') for i in range(30)]
        for file in self.files:
            new_file = str(file.replace(' ','_'))
            os.rename(file,new_file)
        self.files = os.listdir()
        print('You have been underscored!')

    @correct_directory
    def underscore_to_space(self,):
        """replaces all underscores in file names to space"""
        #[rename(i,i.replace(' ','_') for i in range(30)]
        for file in self.files:
            new_file = str(file.replace('_',' '))
            os.rename(file,new_file)
        self.files = os.listdir()
        print('You have been spaced!')

    @correct_directory
    def filename_str(self, func):
        """takes a str function and uses it on the file names for name customization"""
        if "'str' objects" in str(func):
            for file in self.files:
                print(func(file))
                os.rename(file,func(file))
        else:
            raise ValueError("String function required in str.func format")#TypeError

    @correct_directory
    def dir_info(self):
        """returns FileDescription namedtuple object that records the name, type, date last accessed,
         and size if file of every item in the current directoy"""
        FileDescription = namedtuple('FileDescription', 'name type last_accessed size')
        file_description_list = []
        file_info = (os.scandir(self.directory))
        for file in file_info:
            if file.is_dir():
                print('\n{}   Type: Directory \nLast Accessed: {}'.format(file.name,time.ctime(file.stat().st_atime)))
                file_description_list.append(FileDescription(file.name,'directory',time.ctime(file.stat().st_atime),0))
            else:
                print('\n{}   Type: File \nLast Accessed: {}\nFile Size: {}Kb'.format(file.name,time.ctime(file.stat().st_atime),file.stat().st_size/1000))
                file_description_list.append(FileDescription(file.name,'file',time.ctime(file.stat().st_atime),file.stat().st_size/1000))
        return file_description_list

    def __str__(self):
        return('\nDirectoryPal Object\nCurrently Working in: {}\nWorking With: {}'.format(self.directory, self.files))

b = DirectoryPal()
current_dir_info = b.dir_info()
for tup in current_dir_info:
    print(tup)
