#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 12/septmber/2013

@author: Alessandra Scicchitano

Class for support. The idea is to extend it later if need it

'''
from optparse import OptionParser
import MySQLdb as mdb

class mysql_interface( object ):

  # Default values for the different options and Constants 
  DEFAULT_MYSQL_USER = "python_reader"
  DEFAULT_MYSQL_PASSWORD = "python"
  DEFAULT_MYSQL_HOST = "localhost"
  DEFAULT_PASSWORD = "python"
  DEFAULT_KEYSTONEDB = "keystone"
  DEFAULT_NOVADB = "nova"
  DEFAULT_CINDERDB = "cinder"

  def getDefaultUsername( self ):
    return self.DEFAULT_MYSQL_USER

  def getDefaultHost( self ):
    return self.DEFAULT_MYSQL_HOST

  def getDefaultPassword( self ):
    return self.DEFAULT_PASSWORD

  def getDefaultKeystonedb( self ):
    return self.DEFAULT_KEYSTONEDB

  def getDefaultNovadb( self ):
    return self.DEFAULT_NOVADB

  def getDefaultCinderdb( self ):
    return self.DEFAULT_CINDERDB

  def defaultMysqlUpdateInstancesInUse( self, reference ):
    con = mdb.connect(self.getDefaultHost(), self.getDefaultUsername(), self.getDefaultPassword(), self.getDefaultNovadb());
    with con:
      cur = con.cursor()
      cur.execute(""" UPDATE quota_usages SET in_use = -1 WHERE project_id=%s and resource = 'instances' """, (reference,))


  def mysqlUpdateInstancesInUse( self, localhost, user, password, reference ):
    con = mdb.connect(localhost, user, password , self.getDefaultNovadb());
    with con:
      cur = con.cursor()
      cur.execute(""" UPDATE quota_usages SET in_use = -1 WHERE project_id=%s and resource != 'security_groups' """, (reference,))


