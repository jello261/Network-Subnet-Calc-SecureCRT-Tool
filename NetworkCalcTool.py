# $language = "Python"
# $interface = "1.0"

import re
import sys

def main():
    ip, subnet = get_input()

    # decimal to binary
    ipBinary = '.'.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    subnetBinary = '.'.join([bin(int(x)+256)[3:] for x in subnet.split('.')])

    hostbits = subnetBinary.count("0")
    cidr = subnetBinary.count("1")

    networkAddress = calNetworkAddress(ipBinary, hostbits)
    broadcastAddress = calBroadcastAddress(ipBinary, hostbits)
    firstIpaddress = calafirst(networkAddress)
    lastIpaddress = calalast(broadcastAddress)

    crt.Dialog.MessageBox(
        "IP Address: " + ip + "/" + str(cidr) + "\n" +
        "Usable IPs: " + firstIpaddress + " - " + lastIpaddress + "\n\n" +
        "Network: " + networkAddress + "\n" +
        "Broadcast: " + broadcastAddress
    )

def calafirst(netAddress):
    netAddresslist = []
    for octet in netAddress.split('.'):
        netAddresslist.append(str(octet))
    netAddresslist.append('0')
    netAddresslist[-1] = int(netAddresslist[-1]) + 1
    firstip = '.'.join(map(str, netAddresslist))
    return firstip

def calalast(castAddress):
    broadcastlist = []
    for octet in castAddress.split('.'):
        broadcastlist.append(str(octet))
    broadcastlist.append('0')
    broadcastlist.pop(-1)
    broadcastlist[-1] = int(broadcastlist[-1]) - 1
    lastip = '.'.join(map(str, broadcastlist))
    return lastip

def get_input():
    # Get IP address and subnet from clipboard
    rawData = crt.Clipboard.Text
    ipv4_regex = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

    try:
        ip, subnet = rawData.split(' ')
        if ipv4_regex.match(ip) and ipv4_regex.match(subnet):
            return ip, subnet
    except:
        try:
            ip, subnet = rawData.split('/')
            if ipv4_regex.match(ip) and int(subnet) in range(8, 33):
                cidr = int(subnet)
                mask_bin = ('1'*cidr) + ('0'*(32-cidr))
                subnetbinary = list(mask_bin)
                subnetbinary.insert(8, '.')
                subnetbinary.insert(17, '.')
                subnetbinary.insert(26, '.')
                subnet = BinaryToDecimal(''.join(subnetbinary))
                if ipv4_regex.match(ip) and ipv4_regex.match(subnet):
                    return ip, subnet
        except:
            ip = crt.Dialog.Prompt("Please enter an IP address:", "IP Address Input", "", False)
            subnet = crt.Dialog.Prompt("Please enter a subnet mask:", "Subnet Mask Input", "", False)
            if ipv4_regex.match(ip) and ipv4_regex.match(subnet):
                return ip, subnet
            else:
                exit()

def calBroadcastAddress(ipBinary, hostbits):
    broadcastipBinary = list(ipBinary.replace('.', ''))

    # add 1's to find the broadcast address in binary
    for x in range(1, (hostbits + 1)):
        index = -abs(x)
        if broadcastipBinary[index] != '.':
            broadcastipBinary[index] = '1'

    # put the periods back
    broadcastipBinary.insert(8, '.')
    broadcastipBinary.insert(17, '.')
    broadcastipBinary.insert(26, '.')

    return BinaryToDecimal(''.join(broadcastipBinary))

def calNetworkAddress(ipBinary, hostbits):
    networkipBinary = list(ipBinary.replace('.', ''))

    # add 0's to find the network address in binary
    for x in range(1, (hostbits + 1)):
        index = -abs(x)
        if networkipBinary[index] != '.':
            networkipBinary[index] = '0'

    # put the periods back
    networkipBinary.insert(8, '.')
    networkipBinary.insert(17, '.')
    networkipBinary.insert(26, '.')

    return BinaryToDecimal(''.join(networkipBinary))

def BinaryToDecimal(inputBinary):
    # convert binary to decimal
    ipoctet = ''
    for binary in inputBinary.split('.'):
        decimal = 0
        i = 0
        while int(binary) != 0:
            dec = int(binary) % 10
            decimal = decimal + dec * pow(2, i)
            binary = int(binary) // 10
            i += 1
        if ipoctet == '':
            ipoctet = str(decimal)
        else:
            ipoctet = ipoctet + '.' + str(decimal)
    return ipoctet

main()
