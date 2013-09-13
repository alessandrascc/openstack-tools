openstack-tools
===============

openstack utilities

Small description of the files:

- mysql_interface.py = Class for support. The idea is to extend it later if need it.
- openstack_accounting = Created by Joel Casutt. A script to read out the OpenStack mysql database 
  and create a report about walltime and volume usage on a per user base.
  To use this script you should create a mysql user that has read-only rights.
  (Slightly modified by me to take in count the stuck VMs)
- openstack_accounting_for_project = Returns the list of existing projects with total instances, 
  active machines and total time used.
  It's an extension of the class openstack_accountig which listed the same but on a user base.
- openstack_update_quotas.py = This script compares the number of active instances per project and compares 
  it with the number registered in quota_usages for all project in the OpenStack cloud.
  If the two numbers are different the value in the column "in_use" of the table quota_usages is set to -1.
  This will force an update of the table as soon as a new VM is created for that project.
  The scope of this script is to correct a well known bug reported in Folsom (might still exist in Grizzly).
  The VMs created by a specific user that are deleted by an amministrator don't trigger 
  the update of the quotas in the database.
  To use this script you should create a mysql user that has read and write rights.

