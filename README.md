# vcenter-vm-powerstates
Python script and Docker container to gather the amount of VM's turned on and off from vCenter
## Usage
```shell
docker run larsstoker/vcenter-vm-powerstates:latest
```
#### Environment Variables

* `VCENTER_HOST` - vCenter hostname
* `VCENTER_USR` - vCenter username
* `VCENTER_PWD` - vCenter password
* `INFLUX_HOST` - InfluxDB hostname
* `INFLUX_USR` - InfluxDB user
* `INFLUX_PWD` - InfluxDB password
* `INFLUX_DB` - InfluxDB database