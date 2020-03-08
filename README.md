<h1 align="center">
  sepicker
</h1>

<p align="center">
  📊 Monitoring for the STIEBEL ELTRON Heat Pump
</p>

<p align="center">
  <a href="https://github.com/danielbayerlein/sepicker/actions">
    <img alt="Actions Status" src="https://github.com/danielbayerlein/sepicker/workflows/CI/badge.svg">
  </a>
  <a href="https://dependabot.com">
    <img alt="Dependabot Status" src="https://api.dependabot.com/badges/status?host=github&repo=danielbayerlein/sepicker">
  </a>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/457834/76162079-241b7c80-613a-11ea-9f18-1c380d588635.png" width="600" alt="Dashboard">
</p>

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
  * [Cron Job](#cron-job)
  * [Database](#database)
  * [Grafana <em>(optional)</em>](#grafana-optional)
* [Config](#config)
  * [CAN bus](#can-bus)
    * [Example](#example)
    * [Description](#description)
  * [Data](#data)
    * [Example](#example-1)
    * [Description](#description-1)
  * [Database](#database-1)
* [Resources](#resources)
* [License](#license)

## Requirements

* [Python 3.7](https://www.python.org)
* [MySQL](https://www.mysql.com/)
* [Grafana](https://grafana.com/) *(optional)*
* [Raspberry Pi](https://www.raspberrypi.org) + [CANable](https://canable.io) *(or similar devices)*

## Installation

* Download the [latest release](https://github.com/danielbayerlein/sepicker/releases/latest/download/package.zip)
  ```bash
  wget https://github.com/danielbayerlein/sepicker/releases/latest/download/package.zip
  ```
* Unzip the package
  ```bash
  unzip package.zip
  ```
* Install the dependencies
  ```bash
  pip3 install -r requirements.txt
  ```

### Cron Job

To collect the data every *x* minutes, it's necessary to create a cron job. This is an example to query the data every two minutes:

```
*/2 * * * * /home/pi/sepicker/bin/sepicker
```

### Database

Execute the [seed file](./sepicker/resources/datastore/seed.sql) via MySQL command line or copy the query into your MySQL shell.

### Grafana *(optional)*

With [Grafana](https://grafana.com/) you can create your own dashboard with widgets or use the existing [template](./sepicker/resources/dashboard/grafana.json).

## Config

The configuration for the CAN bus and for the data to be queried is located in [config.yml](./config.yml). The database configuration is located in [.env](./.env.example).

### CAN bus

File: [config.yml](./config.yml)

#### Example

```yaml
can:
  interface: can0
  sender: 680
```

#### Description

* `interface`: CAN bus interface
  * `can0`
* `sender`: Sender ID
  * `680`

### Data

File: [config.yml](./config.yml)

See http://juerg5524.ch/data/ElsterTable.inc for the indexes.

#### Example

```yaml
data:
  - name: AUSSENTEMPERATUR
    index: 180.000c
    format: dec_val
  - name: QUELLENTEMPERATUR
    index: 180.01d4
    format: dec_val
  - name: FEHLER
    index: 180.0001
```

#### Description

* `name`: Name for the data point
  * `AUSSENTEMPERATUR`
* `index`: Receiver and Register separated by a dot
  * `180.000c`
* `format` *(optional)*:
  * `dec_val`
  * `mil_val`
  * `little_endian`

### Database

File: [.env](./.env.example)

Rename the `.env.example` file to `.env` or create it with the following content:

```
DB_DATABASE=heat-pump
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
```

## Resources

* http://juerg5524.ch/list_data.php
* https://github.com/andig/goelster
* https://github.com/Andy2003/heat-pump-api

## License

Copyright (c) 2020-present Daniel Bayerlein. See [LICENSE](./LICENSE) for details.
