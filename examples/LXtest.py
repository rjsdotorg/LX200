#!/usr/bin/env python
# Boa:PyApp:main

modules = {}


def main():
    import LX200
    scope = LX200.Telescope()
    print dir(LX200)

    scope.comPort = LX200.LXSerial(scope, debug=True)
    # print scope.comPort.scan_ports()
    # print scope.comPort.test_baud_rates(0)

    scope.comPort.connect_port(0, ptimeout=3)

    print 'Alt', scope.get_Altitude()

    scope.set_site_name(1, "LJ")
    print 'sites', scope.get_site_names()

    # print 'info', scope.version_info()
    print scope.get_AZ()
    print 'sidereal time:', scope.get_sidereal_time()


if __name__ == '__main__':
    main()
