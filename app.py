#!/usr/bin/env python3
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from pyVim import connect
from pyVmomi import vim
from os import environ, write
import logging
from time import time, sleep

# Get number of VM's powered on
def poweredOn(children):
  list = []
  for child in children:
    summary = child.summary
    state = (summary.runtime.powerState == "poweredOn" and summary.config.template == False)
    list.append(state)
  poweredOn = sum(list)
  print(str(poweredOn) + " virtual machines are powered on")
  return poweredOn
#endDef

# Get number of VM's powered off
def poweredOff(children):
  list = []
  for child in children:
    summary = child.summary
    state = (summary.runtime.powerState == "poweredOff" and summary.config.template == False)
    list.append(state)
  poweredOff = sum(list)
  print(str(poweredOff) + " virtual machines are powered off")
  return poweredOff
#endDef

# Write data to InfluxDB
def writeInflux(client, database, children):
  measurement = {}
  measurement['measurement'] = 'vsphere_cluster_vmcount'
  measurement['tags'] = {}
  measurement['fields'] = {}
  measurement['fields']['poweredOn'] = poweredOn(children)
  measurement['fields']['poweredOff'] = poweredOff(children)
  try:
    client.switch_database(database)
    client.write_points([measurement])
    print("Exported to InfluxDB successfully")
    print("")
  except InfluxDBClientError as e:
    logging.error("Failed to export data to Influxdb: %s" % e)
#endDef

def main():
  print("Starting vCenter powerstate script...")
  
  # Get the variables set within Docker
  vcenterHost = environ['VCENTER_HOST']
  vcenterUsr = environ['VCENTER_USR']
  vcenterPwd = environ['VCENTER_PWD']
  influxHost = environ['INFLUX_HOST']
  influxUsr = environ['INFLUX_USR']
  influxPwd = environ['INFLUX_PWD']
  influxDb = environ['INFLUX_DB']

  # InfluxDB client 
  influx_client = InfluxDBClient(
    host=influxHost, 
    port=8086, 
    username=influxUsr, 
    password=influxPwd
  )

  # vSphere client
  vsphere_client = connect.SmartConnectNoSSL (
    host=vcenterHost,
    user=vcenterUsr,
    pwd=vcenterPwd
  )

  # Get virtual machines
  content = vsphere_client.RetrieveContent()
  container = content.rootFolder
  viewType = [vim.VirtualMachine]
  containerView = content.viewManager.CreateContainerView(
              container, viewType, recursive=True)
  children = containerView.view
  
  # Run every 60 seconds
  while True:
    sleep(60 - time() % 60)
    writeInflux(influx_client, influxDb, children)

if __name__ == "__main__":
  main()