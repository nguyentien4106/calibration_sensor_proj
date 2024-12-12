using Shiny.BluetoothLE;
using System.Collections.ObjectModel;
using Shiny;
using Shiny.BluetoothLE.Hosting;
using IPeripheral = Shiny.BluetoothLE.IPeripheral;
namespace CalibApp
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        private readonly IBleManager _bleManager;
        private IPeripheral _deviceSelected;
        //private IGattCharacteristic _writeCharacteristic;

        public ObservableCollection<IPeripheral> Devices { get; private set; }

        public MainPage(IBleManager bleManager)
        {
            InitializeComponent();
            _bleManager = bleManager;
            Devices = new ObservableCollection<IPeripheral>();
            DevicesList.ItemsSource = Devices;
        }

        private void OnCounterClicked(object sender, EventArgs e)
        {
            count++;

            //if (count == 1)
            //    CounterBtn.Text = $"Clicked {count} time";
            //else
            //    CounterBtn.Text = $"Clicked {count} times";

            //SemanticScreenReader.Announce(CounterBtn.Text);
        }

        private async void OnScanButtonClicked(object sender, EventArgs e)
        {

            var access = await _bleManager.RequestAccessAsync();

            if(access != AccessState.Available)
            {
                await DisplayAlert("Error", "Bluetooth is not available or turned on.", "OK");
                return;
            }

            Devices.Clear();

            var scanner = _bleManager.Scan().Subscribe(scanResult =>
            {
                Devices.Add(scanResult.Peripheral);
            });

            scanner.Dispose();
        }

        private void OnDeviceSelected(object sender, SelectionChangedEventArgs e)
        {
            _deviceSelected = e.CurrentSelection.FirstOrDefault() as IPeripheral;
            ConnectButton.IsEnabled = _deviceSelected != null;
        }

        private async void OnConnectButtonClicked(object sender, EventArgs e)
        {
            if (_deviceSelected is null)
            {
                await DisplayAlert("Error", "No device selected.", "OK");
                return;
            }

            try
            {
                await _deviceSelected.ConnectAsync();
                //var character = await _deviceSelected.GetCharacteristicAsync(_deviceSelected.Uuid);
            }
            catch (Exception ex) { 
            }
        }

        private void OnSendButtonClicked(object sender, EventArgs e)
        {

        }
    }

}
