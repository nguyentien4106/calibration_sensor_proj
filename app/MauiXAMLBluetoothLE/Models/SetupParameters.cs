namespace MauiXAMLBluetoothLE.Models
{
    public class SetupParameters
    {
        public SetupParameters(string mode, int time_on, string color_on, string color_off, int[] ordering)
        {
            data = new SetupData
            {
                time_on = time_on,
                color_on = color_on,
                color_off = color_off,
                led_mode = new LedMode
                {
                    mode = mode,
                    ordering = ordering
                }
            };
        }
        public string type { get; set; } = "SETUP";

        public SetupData data { get; set; }


    }

    public class SetupData()
    {
        public int time_on { get; set; }

        public string color_on { get; set; }

        public string color_off { get; set; }

        public LedMode led_mode { get; set; }
    }

    public class LedMode
    {
        public string mode { get; set; }

        public int[] ordering { get; set; } = [];
    }
}
