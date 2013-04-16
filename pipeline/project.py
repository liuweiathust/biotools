import sys
import os
import os.path

class Project(object):
    def __init__(self, dist="."):
        self.template_path = "/home/liuwei/Project/nextomics/template/project-template/transcriptome/"
        self.dist = dist
    def create(self):
        print("Create project %s" % os.path.basename(self.dist))
        retcode = os.system("cp -r %s %s" % (self.template_path, self.dist))  
        if retcode == 0:
            print("Succeed!")
        else:
            print("Failed!")