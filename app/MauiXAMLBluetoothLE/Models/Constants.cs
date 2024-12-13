using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MauiXAMLBluetoothLE.Models
{
    public static class Constants
    {
        public static ObservableCollection<string> CommonColors => ["RED", "WHITE", "YELLOW", "BLUE"];

        public static string OffColor = "OFF";

        public static ObservableCollection<LedButton> LedButtons => [.. Enumerable.Range(1, 20).Select(i => new LedButton() {
            Value = i,
            RowIndex = ( (i - 1) / 5 ),
            ColumnIndex = (i % 5)
        })];
    }

    public class LedButton
    {
        public int Value { get; set; }

        public int RowIndex { get;set; }

        public int ColumnIndex { get; set; }
    }
}
