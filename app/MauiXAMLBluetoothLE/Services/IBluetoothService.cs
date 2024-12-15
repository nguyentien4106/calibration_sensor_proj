using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MauiXAMLBluetoothLE.Services;

public interface IBluetoothService
{
    IDevice[] GetConnectedDevices();

    Task Connect(string deviceName);
    Task Disconnect();
    Task Send(string deviceName, byte[] content);
    Task<byte[]> Receive(string deviceName);
}