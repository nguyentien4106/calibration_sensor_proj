using Microsoft.Extensions.Logging;
using Shiny;

namespace CalibApp
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .UseShiny()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                    fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                });
                //.UsePrism(
                //    new DryIocContainerExtension(),
                //    prism => prism.CreateWindow("MainPage")
                //);

            builder.Services.AddBluetoothLE();
            builder.Services.AddTransient<MainPage>();

#if DEBUG
            builder.Logging.AddDebug();
#endif

            return builder.Build();
        }

        static MauiAppBuilder RegisterRoutes(this MauiAppBuilder builder)
        {
            var s = builder.Services;

            s.RegisterForNavigation<MainPage>("MainPage");
            // ble client
           
            return builder;
        }
    }
}
