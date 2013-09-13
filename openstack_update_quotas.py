#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 9/September/2013

@author:Alessandra Scicchitano

This script compares the number of active instances per project and compares it with the number registered in quota_usages for all project in the OpenStack cloud.
If the two numbers are different the value in the column "in_use" of the table quota_usages is set to -1.
This will force an update of the table as soon as a new VM is created for that project.
The scope of this scritp is to correct a well known bug reported in Folsom.
The VMs created by a specific user that are deleted by an amministrator don't trigger the update of the quotas in the database.
To use this script you should create a mysql user that has both read and write rights. 
'''

from openstack_accounting_per_project import openstack_accounting_per_project as o_a_p
from mysql_interface import mysql_interface


def main():
  
  """ Supporting classes """
  _msi = mysql_interface()
  _scanner = o_a_p()
  _scanner.createParser()
  _scanner.readOptions()
 
  """ List of Project IDs associated to their project names """
  projectid_mapping = _scanner.prepareProjectMapping()
  
  """ Collect info on the usage from the table quota_usages in nova database
      The database has a line for each used resource with is corresponding value
      The obtained list needs to be formatted to a dict to be esier to handle
  """
  usage = _scanner.mysqlSelect(_scanner.getNovadb(),"quota_usages",["deleted","project_id","resource","in_use"])
  usage_mapping = _scanner.formatDict(usage)
  
  """ Info on active resources in the cloud """
  instance_mapping = _scanner.prepareDict( _scanner.getNovadb(), "instances", ["project_id","created_at", "deleted_at", "vcpus","deleted"])
  volume_mapping = _scanner.prepareDict( _scanner.getCinderdb(), "volumes", ["project_id","created_at", "deleted_at", "size","deleted"])
  
  """ Comparison """
  for key in instance_mapping:
        quota = usage_mapping[key].index("instances")
        
        """ Other bug: What happens with VM can happen with project as well. The database might return a project listed as active which is instead deleted.
            If that's the case a warning message is generated.
        """
        if key in projectid_mapping:
          instance_index=quota+1

          """ Search for mismatch:
              project[key] != 'admin' : The project 'admin' doesn't need to be checked
              usage_mapping[key][instance_index]!=-1 : It has been reset last time than the script was. No need to be checked
              usage_mapping[key][instance_index]!=instance_mapping[key][1]: returns the mismatch
          """
          if project[key] != 'admin' and usage_mapping[key][instance_index]!=-1 and usage_mapping[key][instance_index]!=instance_mapping[key][1]:
            print 'Attention: Mismatch!! Project ', projectid_mapping[key], ' active machine = ', instance_mapping[key][1],'but instances in use in quota_usage = ', usage_mapping[key][instance_index], '' 
            _msi.mysqlUpdateInstancesInUse(_scanner.host, _scanner.username, _scanner.password, key)
            print 'Problem fixed setting the value of instances in use in the table quota_usages to -1. The first time a VM will be started in the project the table will be updated to the right value. \n'
        else:
          print 'Attention: Project listed that doesn\'t exist in Keystone (project_id = ', key ,' active_machine = ', instance_mapping[key][1],'. The database needs to be cleaned. No action has been executed to fix this problem.)\n'

if __name__ == '__main__':
  main()

