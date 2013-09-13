#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 9/September/2013

@author:Alessandra Scicchitano

Returns the list of existing projects with total instances, active machines and total time used
It's an extension of the calss openstack_accountig which listed the same but on a user base

'''

from openstack_accounting import openstack_accounting

class openstack_accounting_per_project ( openstack_accounting ):

  #constructor
  def __init__( self ):
    openstack_accounting.__init__( self)

  def prepareProjectList( self ):
    project_output = self.mysqlSelect(self.getKeystonedb(), "tenant", ["id"])
    project_list = list()
    for project in project_output:
      project_list.append(project[0])
    return project_list 
  
  def prepareProjectMapping( self ):
    projects = self.mysqlSelect(self.getKeystonedb(), "tenant", ["id","name"])
    projectid_mapping = dict()
    for project in projects:
      projectid_mapping[project[0]] = project[1]
    return projectid_mapping

    return return_data
   
  def formatDict( self, list_to_format):
    formatted_list = dict()
    for row in list_to_format:
      if not bool(row[0]):
        if not row[1] in formatted_list:
          formatted_list[row[1]] = list(row[2:])
        else:
          formatted_list[row[1]]+=list(row[2:])
    return formatted_list

def main():
  reader = openstack_accounting_per_project()
  reader.createParser()
  reader.readOptions()
  project_list = reader.prepareProjectList()
  projectid_mapping = reader.prepareProjectMapping()
  instance_mapping = reader.prepareDict(reader.getNovadb(), "instances", ["project_id","created_at", "deleted_at", "vcpus","deleted"])
  volume_mapping = reader.prepareDict(reader.getCinderdb(), "volumes", ["project_id","created_at", "deleted_at", "size","deleted"])
  reader.writeOutput(project_list, projectid_mapping, instance_mapping, volume_mapping)

if __name__ == '__main__':
  main()

