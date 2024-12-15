using System.Collections;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;

namespace MauiXAMLBluetoothLE.ViewModels;

public partial class HeartRatePageViewModel : BaseViewModel, INotifyPropertyChanged
{
    public BluetoothLEService BluetoothLEService { get; private set; }
    public IService HeartRateService { get; private set; }
    public ICharacteristic HeartRateMeasurementCharacteristic { get; private set; }

    #region Command

    public IAsyncRelayCommand ConnectToDeviceCandidateAsyncCommand { get; }
    public IAsyncRelayCommand DisconnectFromDeviceAsyncCommand { get; }
    public IAsyncRelayCommand SetupAsyncCommand { get; }
    public IAsyncRelayCommand ButtonCommand { get; }

    #endregion

    #region Options
    public ObservableCollection<string> Modes { get; set; }

    public ObservableCollection<string> OnColors { get; set; } = Constants.CommonColors;

    public ObservableCollection<string> OffColors { get; set; } = [.. Constants.CommonColors, Constants.OffColor];

    public ObservableCollection<LedButton> LedButtons { get; set; } = Constants.LedButtons;

    #endregion

    public HeartRatePageViewModel(BluetoothLEService bluetoothLEService)
    {
        Title = $"Dashboard";

        Modes = ["RANDOM", "FREQUENTLY"];

        BluetoothLEService = bluetoothLEService;

        ConnectToDeviceCandidateAsyncCommand = new AsyncRelayCommand(ConnectToDeviceCandidateAsync);

        DisconnectFromDeviceAsyncCommand = new AsyncRelayCommand(DisconnectFromDeviceAsync);

        SetupAsyncCommand = new AsyncRelayCommand(SetupParametersAsync);

        ButtonCommand = new AsyncRelayCommand<LedButton>(async button => await CheckedLedButtonAsync(button));
    }

    //public string SelectedColorOn { get; set; }
    //public string SelectedColorOff { get; set; }

    public int TimeOn { get; set; }

    public int TimePlay { get; set; }


    [ObservableProperty]
    string heartRateValue;

    [ObservableProperty]
    bool isConfig;

    [ObservableProperty]
    bool connected;

    public bool IsShowConnectButton { get => !connected && !IsBusy; }

    private int selectedModeIndex;
    private string selectedMode;

    public int SelectedModeIndex 
    { 
        get => selectedModeIndex;
        set
        {
            if (selectedModeIndex != value)
            {
                selectedModeIndex = value;
                OnPropertyChanged();
                OnSelectedIndexChanged();
            }
        }
    }

    public string SelectedMode
    {
        get => selectedMode;
        set
        {
            if (selectedMode != value)
            {
                selectedMode = value;
                OnPropertyChanged();
            }
        }
    }

    public event PropertyChangedEventHandler PropertyChanged;

    protected void OnPropertyChanged([System.Runtime.CompilerServices.CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void OnSelectedIndexChanged()
    {
        if (SelectedModeIndex >= 0 && SelectedModeIndex < Modes.Count)
        {
            SelectedMode = Modes[SelectedModeIndex];
        }

        if(SelectedModeIndex == 2)
        {
            IsConfig = true;
            OnPropertyChanged(nameof(IsConfig));
        }
    }

    #region Functions

    private async Task ConnectToDeviceCandidateAsync()
    {
        if (IsBusy)
        {
            return;
        }

        if (BluetoothLEService.NewDeviceCandidateFromHomePage.Id.Equals(Guid.Empty))
        {
            #region read device id from storage
            var device_name = await SecureStorage.Default.GetAsync("device_name");
            var device_id = await SecureStorage.Default.GetAsync("device_id");
            if (!string.IsNullOrEmpty(device_id))
            {
                BluetoothLEService.NewDeviceCandidateFromHomePage.Name = device_name;
                BluetoothLEService.NewDeviceCandidateFromHomePage.Id = Guid.Parse(device_id);
            }
            #endregion read device id from storage
            else
            {
                await BluetoothLEService.ShowToastAsync($"Select a Bluetooth LE device first. Try again.");
                return;
            }
        }

        if (!BluetoothLEService.BluetoothLE.IsOn)
        {
            await Shell.Current.DisplayAlert($"Bluetooth is not on", $"Please turn Bluetooth on and try again.", "OK");
            return;
        }

        if (BluetoothLEService.Adapter.IsScanning)
        {
            await BluetoothLEService.ShowToastAsync($"Bluetooth adapter is scanning. Try again.");
            return;
        }

        try
        {
            IsBusy = true;
            OnPropertyChanged(nameof(IsBusy));
            if (BluetoothLEService.Device != null)
            {
                if (BluetoothLEService.Device.State == DeviceState.Connected)
                {
                    Connected = true;
                    OnPropertyChanged(nameof(Connected));
                    if (BluetoothLEService.Device.Id.Equals(BluetoothLEService.NewDeviceCandidateFromHomePage.Id))
                    {
                        await BluetoothLEService.ShowToastAsync($"{BluetoothLEService.Device.Name} is already connected.");
                        return;
                    }

                    if (BluetoothLEService.NewDeviceCandidateFromHomePage != null)
                    {
                        #region another device
                        if (!BluetoothLEService.Device.Id.Equals(BluetoothLEService.NewDeviceCandidateFromHomePage.Id))
                        {
                            Title = $"{BluetoothLEService.NewDeviceCandidateFromHomePage.Name}";
                            await DisconnectFromDeviceAsync();
                            await BluetoothLEService.ShowToastAsync($"{BluetoothLEService.Device.Name} has been disconnected.");
                        }
                        #endregion another device
                    }
                }
            }

            BluetoothLEService.Device = await BluetoothLEService.Adapter.ConnectToKnownDeviceAsync(BluetoothLEService.NewDeviceCandidateFromHomePage.Id);

            if (BluetoothLEService.Device.State == DeviceState.Connected)
            {
                Connected = true;
                OnPropertyChanged(nameof(Connected));
                var services = await BluetoothLEService.Device.GetServicesAsync();
                var result = await BluetoothLEService.Device.GetServiceAsync(HeartRateUuids.HeartRateServiceUuid);
                HeartRateService = services[2];
                if (HeartRateService != null)
                {
                    var characteristics = await HeartRateService.GetCharacteristicsAsync();
                    HeartRateMeasurementCharacteristic = characteristics[0]; // await HeartRateService.GetCharacteristicAsync(HeartRateUuids.HeartRateMeasurementCharacteristicUuid);
                    if (HeartRateMeasurementCharacteristic != null)
                    {
                        if (HeartRateMeasurementCharacteristic.CanUpdate)
                        {
                            Title = $"{BluetoothLEService.Device.Name}";

                            #region save device id to storage
                            await SecureStorage.Default.SetAsync("device_name", $"{BluetoothLEService.Device.Name}");
                            await SecureStorage.Default.SetAsync("device_id", $"{BluetoothLEService.Device.Id}");
                            #endregion save device id to storage

                            HeartRateMeasurementCharacteristic.ValueUpdated += HeartRateMeasurementCharacteristic_ValueUpdated;
                            await HeartRateMeasurementCharacteristic.StartUpdatesAsync();
                        }
                        if (HeartRateMeasurementCharacteristic.CanWrite)
                        {
                            var result1 = await HeartRateMeasurementCharacteristic.WriteAsync(Encoding.ASCII.GetBytes("12334423423423423423423423423423423432423424"));
                        }

                    }
                }
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Unable to connect to {BluetoothLEService.NewDeviceCandidateFromHomePage.Name} {BluetoothLEService.NewDeviceCandidateFromHomePage.Id}: {ex.Message}.");
            await Shell.Current.DisplayAlert($"{BluetoothLEService.NewDeviceCandidateFromHomePage.Name}", $"Unable to connect to {BluetoothLEService.NewDeviceCandidateFromHomePage.Name}.", "OK");
        }
        finally
        {
            IsBusy = false;
            OnPropertyChanged(nameof(IsBusy));
        }
    }

    private void HeartRateMeasurementCharacteristic_ValueUpdated(object sender, CharacteristicUpdatedEventArgs e)
    {
        var bytes = e.Characteristic.Value;
        string text = System.Text.Encoding.UTF8.GetString(bytes);
        var messages = text.Split("~");
        HeartRateValue = messages[0] == "score" ? messages[1] : "0";
        OnPropertyChanged(nameof(HeartRateValue));
    }

    private async Task DisconnectFromDeviceAsync()
    {
        if (IsBusy)
        {
            return;
        }

        if (BluetoothLEService.Device == null)
        {
            await BluetoothLEService.ShowToastAsync($"Nothing to do.");
            return;
        }

        if (!BluetoothLEService.BluetoothLE.IsOn)
        {
            await Shell.Current.DisplayAlert($"Bluetooth is not on", $"Please turn Bluetooth on and try again.", "OK");
            return;
        }

        if (BluetoothLEService.Adapter.IsScanning)
        {
            await BluetoothLEService.ShowToastAsync($"Bluetooth adapter is scanning. Try again.");
            return;
        }

        if (BluetoothLEService.Device.State == DeviceState.Disconnected)
        {
            await BluetoothLEService.ShowToastAsync($"{BluetoothLEService.Device.Name} is already disconnected.");
            return;
        }

        try
        {
            IsBusy = true;
            OnPropertyChanged(nameof(IsBusy));


            await HeartRateMeasurementCharacteristic.StopUpdatesAsync();
            await BluetoothLEService.Adapter.DisconnectDeviceAsync(BluetoothLEService.Device);
            HeartRateMeasurementCharacteristic.ValueUpdated -= HeartRateMeasurementCharacteristic_ValueUpdated;
            
            //Connected = false;
            //OnPropertyChanged(nameof(Connected));
            //IsBusy = false;
            //OnPropertyChanged(nameof(IsBusy));
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Unable to disconnect from {BluetoothLEService.Device.Name} {BluetoothLEService.Device.Id}: {ex.Message}.");
            await Shell.Current.DisplayAlert($"{BluetoothLEService.Device.Name}", $"Unable to disconnect from {BluetoothLEService.Device.Name}.", "OK");
        }
        finally
        {
            Title = "Heart rate";
            IsBusy = false;
            Connected = false;
            OnPropertyChanged(nameof(Connected));
            OnPropertyChanged(nameof(IsBusy));

            BluetoothLEService.Device?.Dispose();
            BluetoothLEService.Device = null;
            await Shell.Current.GoToAsync("//HomePage", true);
        }
    }

    async Task SetupParametersAsync()
    {
        if (!(await Validate()))
        {
            return;
        }

        try
        {
            var text = $"{SelectedMode.Substring(0, 1).ToLower()}~{TimePlay}~{TimeOn}";
            var message = Encoding.ASCII.GetBytes(text);
            if (HeartRateMeasurementCharacteristic.CanWrite)
            {
                await SendDataInChunks(message);
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Unable to write from {BluetoothLEService.Device.Name} {BluetoothLEService.Device.Id}: {ex.Message}.");
            await Shell.Current.DisplayAlert($"{BluetoothLEService.Device.Name}", $"Unable to write from {BluetoothLEService.Device.Name}: {ex.Message}", "OK");
        }

    }

    private async Task<bool> Validate()
    {
        if (string.IsNullOrEmpty(SelectedMode))
        {
            await BluetoothLEService.ShowToastAsync("Selected Mode is empty");
            return false;
        }

        //if (string.IsNullOrEmpty(SelectedColorOn))
        //{
        //    await BluetoothLEService.ShowToastAsync("SelectedColorOn is empty");
        //    return false;
        //}

        //if (string.IsNullOrEmpty(SelectedColorOff))
        //{
        //    await BluetoothLEService.ShowToastAsync("SelectedColorOff is empty");
        //    return false;
        //}

        //if (SelectedColorOff == SelectedColorOn)
        //{
        //    await BluetoothLEService.ShowToastAsync("SelectedColorOn is the same with SelectedColorOff");
        //    return false;
        //}

        if(TimeOn <= 0 || TimePlay <= 0)
        {
            await BluetoothLEService.ShowToastAsync("Time must be greater than zero");
            return false;
        }

        return true;
    }

    async Task CheckedLedButtonAsync(LedButton button)
    {

    }
    #endregion

    private async Task SendDataInChunks(byte[] data, int chunkSize = 20)
    {
        for (int i = 0; i < data.Length; i += chunkSize)
        {
            var chunk = data.Skip(i).Take(chunkSize).ToArray();
            await HeartRateMeasurementCharacteristic.WriteAsync(chunk);
            await Task.Delay(100); // Add a small delay to prevent queue overflow
        }
    }
}
