#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

# Reference: Blog post from Jason Dobies
# http://blog.pulpproject.org/2011/05/23/configuring-the-pulp-server-for-ssl/
# http://blog.pulpproject.org/2011/05/18/pulp-protected-repositories/

import os
import sys

from base import add_hostname_option, check_dirs, get_parser, run_command

def create_server_key(server_key):
    check_dirs(server_key)
    cmd = "openssl genrsa -out %s 2048" % (server_key)
    return run_command(cmd)

def create_server_csr(server_key, csr, hostname):
    check_dirs(csr)
    cmd = "openssl req -new -key %s -out %s -subj '/C=US/ST=NC/L=Raleigh/O=Red Hat/OU=Splice/CN=%s'" % (server_key, csr, hostname)
    return run_command(cmd)

def create_server_cert(server_cert, server_csr, ca_cert, ca_key, ca_serial):
    check_dirs(server_cert)
    cmd = "openssl x509 -req -days 10950 -CA %s -CAkey %s -in %s -out %s -CAserial %s" \
            % (ca_cert, ca_key, server_csr, server_cert, ca_serial)
    if not os.path.exists(ca_serial):
        cmd = cmd + " -CAcreateserial"
    return run_command(cmd)

def run():
    parser = get_parser(limit_options=["server_key", "server_cert", "server_csr", "ca_key", "ca_cert", "ca_serial"])
    parser = add_hostname_option(parser)
    (opts, args) = parser.parse_args()

    hostname = opts.hostname
    server_key = opts.server_key
    server_cert = opts.server_cert
    server_csr = opts.server_csr
    ca_key = opts.ca_key
    ca_cert = opts.ca_cert
    ca_serial = opts.ca_serial

    if not create_server_key(server_key):
        print "Failed to create server key"
        sys.exit(1)

    if not create_server_csr(server_key, server_csr, hostname):
        print "Failed to create server csr"
        sys.exit(1)

    if not create_server_cert(server_cert, server_csr, ca_cert, ca_key, ca_serial):
        print "Failed to create server cert"
        sys.exit(1)

    print "Server Cert: %s" % (server_cert)
    print "Server Key: %s" % (server_key)
    return True

if __name__ == "__main__":
    run()
